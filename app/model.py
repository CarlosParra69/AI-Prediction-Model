"""
Modelo de evaluación adaptativa de exámenes DELF.

Integra:
- OpenResponseScorer: Evaluación de preguntas abiertas con criterios DELF
- AdaptiveSelector: Selección adaptativa de preguntas
- BiasChecker: Detección de sesgos en evaluación
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Dict, List, Optional
from uuid import uuid4

import joblib
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

from .adaptive_selector import AbilityState, AdaptiveSelector
from .bias_checker import BiasChecker
from .open_response_scorer import OpenResponseScorer
from .scorers.fill_blank_scorer import score_fill_blank
from .scorers.ordering_scorer import score_ordering
from .schemas import (
    DELFLevel,
    ExamFeatures,
    LearnerBackground,
    Language,
    NextQuestionRecommendation,
    OpenQuestionRubric,
    PredictRequest,
    PredictResponse,
    QuestionResponse,
    QuestionScoreDetail,
    QuestionType,
    RubricBreakdown,
    TrainRequest,
    TrainResponse,
    TrainSample,
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = Path("app/models/exam_model.joblib")


@dataclass
class PredictArtifacts:
    """Artifacts de predicción (compatibilidad con código anterior)."""
    score: float
    level: str
    confidence: float
    explanation: dict


class OnlineExamModel:
    """
    Modelo principal que integra todos los componentes de evaluación adaptativa.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        
        # Regresión para compatibilidad con features legacy
        self.vectorizer = HashingVectorizer(n_features=512, alternate_sign=False, norm="l2")
        self.scaler = StandardScaler(with_mean=False)
        self.regressor = SGDRegressor(
            loss="huber",
            epsilon=1.35,
            alpha=0.001,
            learning_rate="adaptive",
            eta0=0.001,
            max_iter=1,
            tol=None,
            average=True,
            random_state=42,
        )
        
        # Componentes nuevos
        self.open_response_scorer = OpenResponseScorer(confidence_threshold=0.6)
        self.adaptive_selector = AdaptiveSelector(
            start_difficulty=3,
            threshold_high=0.75,
            threshold_low=0.45,
        )
        self.bias_checker = BiasChecker(deviation_threshold=0.10)
        
        # Almacenamiento de ejemplos de preguntas (para entrenamiento)
        self.question_pool: Dict[str, Dict] = {}
        self.training_history: List[Dict] = []
        
        # Estado
        self.initialized = False
        self.trained_samples = 0
        self.version = "v2.0"  # Nueva versión con soporte adaptativo
        self._rng_seed = 42

    # ========================================================================
    # Legacy Methods (Compatibilidad)
    # ========================================================================

    def _encode_background(self, background: LearnerBackground) -> List[float]:
        levels = [LearnerBackground.none, LearnerBackground.normal, LearnerBackground.advanced]
        return [1.0 if background == level else 0.0 for level in levels]

    def _encode_language(self, language: Language) -> List[float]:
        langs = [Language.en, Language.fr]
        return [1.0 if language == lang else 0.0 for lang in langs]

    def _build_numeric_features(self, sample: ExamFeatures) -> np.ndarray:
        questions = sample.questions
        n_questions = len(questions)

        q_types = [q.question_type for q in questions]
        _mcq_types = {QuestionType.mcq, QuestionType.SINGLE_CHOICE, QuestionType.IMAGE}
        _short_types = {QuestionType.short_answer, QuestionType.FILL_BLANK, QuestionType.ORDERING}
        _essay_types = {QuestionType.essay, QuestionType.open, QuestionType.WRITING_TEXT, QuestionType.SPEAKING_RECORD}
        mcq_ratio = sum(1 for t in q_types if t in _mcq_types) / n_questions
        short_ratio = sum(1 for t in q_types if t in _short_types) / n_questions
        essay_ratio = sum(1 for t in q_types if t in _essay_types) / n_questions

        total_time = float(sum(q.time_spent_sec for q in questions))
        avg_time = total_time / n_questions
        avg_difficulty = float(sum(q.difficulty for q in questions)) / n_questions

        observed_points = 0.0
        total_points = 0.0
        resolved_items = 0
        for q in questions:
            total_points += q.max_points
            if q.obtained_points is not None:
                observed_points += min(max(q.obtained_points, 0.0), q.max_points)
                resolved_items += 1
            elif q.is_correct is not None:
                observed_points += q.max_points if q.is_correct else 0.0
                resolved_items += 1

        observed_accuracy = (observed_points / total_points) if total_points > 0 and resolved_items > 0 else 0.0

        expected_time = 0.0
        for q in questions:
            if q.question_type in {QuestionType.mcq, QuestionType.SINGLE_CHOICE, QuestionType.IMAGE}:
                expected_time += 18.0 + (q.difficulty * 6.0)
            elif q.question_type in {QuestionType.short_answer, QuestionType.FILL_BLANK, QuestionType.ORDERING}:
                expected_time += 45.0 + (q.difficulty * 12.0)
            else:
                expected_time += 160.0 + (q.difficulty * 45.0)
        tempo_efficiency = max(0.0, min(1.0, 1.0 - abs(total_time - expected_time) / max(expected_time, 1.0)))

        values = [
            *self._encode_language(sample.language),
            *self._encode_background(sample.learner_background),
            float(n_questions),
            mcq_ratio,
            short_ratio,
            essay_ratio,
            total_time,
            avg_time,
            avg_difficulty,
            observed_accuracy,
            tempo_efficiency,
        ]
        return np.array(values, dtype=np.float64)

    def _build_text(self, sample: ExamFeatures) -> str:
        return " ".join((q.answer_text or "") for q in sample.questions).strip()

    def _max_points(self, sample: ExamFeatures) -> float:
        return float(sum(q.max_points for q in sample.questions))

    def _fallback_score(self, sample: ExamFeatures) -> PredictArtifacts:
        numeric = self._build_numeric_features(sample)
        observed_accuracy = numeric[-2]
        tempo_efficiency = numeric[-1]
        difficulty = numeric[-3]

        background_bonus = {
            LearnerBackground.none: 0.9,
            LearnerBackground.normal: 1.0,
            LearnerBackground.advanced: 1.05,
        }[sample.learner_background]

        base = (observed_accuracy * 65.0) + (tempo_efficiency * 20.0) + ((difficulty / 5.0) * 15.0)
        score = float(np.clip(base * background_bonus, 0.0, 100.0))

        return PredictArtifacts(
            score=round(score, 2),
            level=self._score_to_level(score),
            confidence=0.45,
            explanation={
                "mode": "fallback-rule",
                "observed_accuracy": round(float(observed_accuracy), 4),
                "tempo_efficiency": round(float(tempo_efficiency), 4),
                "avg_difficulty": round(float(difficulty), 4),
            },
        )

    def _score_to_level(self, score: float) -> str:
        """Mapea score (0-100 o 0-1) a nivel DELF con criterios más rigurosos para B1+."""
        # Normalizar a 0-100 si está entre 0-1
        if score <= 1.0:
            score = score * 100
        
        # Criterios del marco DELF más rigurosos
        # B1 y B2 requieren muy pocos errores gramaticales
        if score < 20:
            return "A1-"
        elif score < 30:
            return "A1"
        elif score < 40:
            return "A1+"
        elif score < 45:
            return "A2-"
        elif score < 50:
            return "A2"
        elif score < 60:
            return "A2+"
        elif score < 68:  # Empezar B1 más arriba (antes era 65)
            return "B1-"
        elif score < 77:  # B1 requiere menos errores que 75
            return "B1"
        elif score < 85:  # B1+ desde 77
            return "B1+"
        elif score < 92:  # B2- desde 85
            return "B2-"
        else:  # B2 solo con scores muy altos
            return "B2"

    # ========================================================================
    # New Methods (Adaptive Testing)
    # ========================================================================

    def predict_adaptive(self, request: PredictRequest) -> PredictResponse:
        """
        Evalúa un examen con soporte para preguntas abiertas y modo adaptativo.

        Args:
            request: PredictRequest con preguntas y respuestas.

        Returns:
            PredictResponse con desglose por pregunta, nivel estimado, y recomendación adaptativa.
        """
        with self._lock:
            # Valida que no hay datos sensibles
            data_dict = request.model_dump()
            if not self.bias_checker.is_data_suitable_for_evaluation(data_dict):
                logger.warning(
                    f"Aviso: Candidato {request.candidate_id} presentado posiblemente contiene datos sensibles."
                )

            # Crea mapa de respuestas por question_id
            answers_by_id = {ans.question_id: ans for ans in request.answers}

            # Procesa cada pregunta
            per_question: List[QuestionScoreDetail] = []
            ability_state = self.adaptive_selector.initialize_state() if request.adaptive else None

            for question in request.questions:
                answer = answers_by_id.get(question.question_id)
                if not answer:
                    continue

                # Evalúa la pregunta
                score_detail = self._evaluate_question(
                    question_id=question.question_id,
                    question_type=question.type,
                    question_text=question.text,
                    answer_text=answer.answer_text,
                    answer_list=answer.answer_list,
                    language=question.language,
                    time_spent_sec=answer.time_spent_sec,
                )
                per_question.append(score_detail)

                # Actualiza ability_state si modo adaptativo
                if request.adaptive and ability_state is not None:
                    ability_state = self.adaptive_selector.update_state(
                        ability_state, score_detail.score
                    )

            # Calcula nivel estimado
            all_scores = [q.score for q in per_question]
            avg_score_normalized = (sum(all_scores) / len(all_scores)) if all_scores else 0.5
            
            if ability_state is not None:
                estimated_level = DELFLevel(self.adaptive_selector.estimate_delf_level(ability_state.ability_estimate))
            else:
                estimated_level = DELFLevel(self._score_to_level(avg_score_normalized * 100))

            # Recomendación para siguiente pregunta
            next_recommendation = None
            if request.adaptive and ability_state is not None:
                rec = self.adaptive_selector.recommend_next_question(ability_state)
                next_recommendation = NextQuestionRecommendation(
                    difficulty=rec["difficulty"],
                    topic=rec.get("topic"),
                    reason=rec.get("reason", ""),
                )

            # Metadata
            evaluation_meta = {
                "model_version": self.version,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request_id": str(uuid4()),
                "adaptive_mode": str(request.adaptive),
                "questions_evaluated": str(len(per_question)),
            }

            # Calcula confianza global
            confidences = [q.confidence for q in per_question]
            global_confidence = sum(confidences) / len(confidences) if confidences else 0.5

            return PredictResponse(
                exam_id=request.exam_id,
                candidate_id=request.candidate_id,
                per_question=per_question,
                estimated_level=estimated_level,
                confidence=float(np.clip(global_confidence, 0.0, 1.0)),
                next_question_recommendation=next_recommendation,
                evaluation_meta=evaluation_meta,
            )

    def _evaluate_question(
        self,
        question_id: str,
        question_type: QuestionType,
        question_text: str,
        answer_text: str,
        answer_list: Optional[List[str]] = None,
        language: Language = Language.fr,
        time_spent_sec: float = 0.0,
    ) -> QuestionScoreDetail:
        """
        Evalúa una pregunta individual según su QuestionType.

        Args:
            question_id:   ID de la pregunta.
            question_type: Tipo de pregunta (QuestionType enum).
            question_text: Texto de la pregunta.
            answer_text:   Texto de la respuesta del candidato.
            answer_list:   Respuesta como lista (solo para ORDERING).
            language:      Idioma de la pregunta (en|fr).
            time_spent_sec: Tiempo gastado (informativo).

        Returns:
            QuestionScoreDetail con puntuación y feedback.
        """
        # ── Texto libre (WRITING_TEXT / open / short_answer / essay) ─────────
        if question_type.is_open_text():
            return self._evaluate_open_text(
                question_id, question_type, answer_text, language
            )

        # ── Opción múltiple (SINGLE_CHOICE / mcq / IMAGE) ────────────────────
        if question_type.is_choice_based():
            return self._evaluate_choice(
                question_id, question_type, answer_text, language
            )

        # ── Rellenar hueco (FILL_BLANK) ───────────────────────────────────────
        if question_type.is_fill_blank():
            return self._evaluate_fill_blank(
                question_id, question_type, answer_text, language
            )

        # ── Ordenar elementos (ORDERING) ──────────────────────────────────────
        if question_type.is_ordering():
            return self._evaluate_ordering(
                question_id, question_type, answer_list or [], language
            )

        # ── Grabación de voz (SPEAKING_RECORD) ───────────────────────────────
        if question_type.is_speaking():
            return self._evaluate_speaking_record(
                question_id, question_type, answer_text, language
            )

        # ── Tipos futuros (AUDIO / VIDEO) → revisión humana ──────────────────
        if question_type.requires_human_review_by_default():
            msg = (
                f"Question type '{question_type.value}' is not yet scored automatically. "
                "Pending human review."
                if language == Language.en
                else f"El tipo '{question_type.value}' no tiene scoring automático aún. "
                "Pendiente de revisión humana."
            )
            return QuestionScoreDetail(
                question_id=question_id,
                type=question_type,
                score=0.0,
                max_score=1.0,
                explanation=msg,
                confidence=0.0,
                needs_human_review=True,
                language_detected=language,
            )

        # ── Fallback genérico ─────────────────────────────────────────────────
        return QuestionScoreDetail(
            question_id=question_id,
            type=question_type,
            score=0.5,
            max_score=1.0,
            explanation="Tipo de pregunta no reconocido.",
            confidence=0.3,
            needs_human_review=True,
            language_detected=language,
        )

    # ── Helpers de evaluación por tipo ───────────────────────────────────────

    def _evaluate_open_text(
        self,
        question_id: str,
        question_type: QuestionType,
        answer_text: str,
        language: Language,
    ) -> QuestionScoreDetail:
        """Evalúa preguntas de texto libre con rúbrica DELF."""
        question_info = self.question_pool.get(question_id, {})
        rubric = question_info.get("rubric")
        expected_keywords = question_info.get("expected_keywords", [])

        if rubric and isinstance(rubric, dict):
            try:
                rubric_obj = OpenQuestionRubric(**rubric)
            except Exception:
                rubric_obj = OpenQuestionRubric(level="A1")
        else:
            rubric_obj = OpenQuestionRubric(level="A1")

        score_result = self.open_response_scorer.score(
            response_text=answer_text,
            rubric=rubric_obj,
            language=language,
            expected_keywords=expected_keywords,
        )
        return QuestionScoreDetail(
            question_id=question_id,
            type=question_type,
            score=score_result.score,
            max_score=1.0,
            explanation=score_result.explanation,
            confidence=score_result.confidence,
            needs_human_review=score_result.needs_human_review,
            rubric_breakdown=score_result.rubric_breakdown,
            language_detected=score_result.language_detected,
        )

    def _evaluate_choice(
        self,
        question_id: str,
        question_type: QuestionType,
        answer_text: str,
        language: Language,
    ) -> QuestionScoreDetail:
        """Evalúa preguntas de opción múltiple (SINGLE_CHOICE / MCQ / IMAGE)."""
        question_info = self.question_pool.get(question_id, {})
        correct_answer = question_info.get("answer", "")

        is_correct = answer_text.strip().lower() == correct_answer.strip().lower()
        score = 1.0 if is_correct else 0.0

        if language == Language.fr:
            explanation = "Réponse correcte." if is_correct else "Réponse incorrecte."
        else:
            explanation = "Correct answer." if is_correct else "Incorrect answer."

        return QuestionScoreDetail(
            question_id=question_id,
            type=question_type,
            score=score,
            max_score=1.0,
            explanation=explanation,
            confidence=0.97,
            needs_human_review=False,
            language_detected=language,
        )

    def _evaluate_fill_blank(
        self,
        question_id: str,
        question_type: QuestionType,
        answer_text: str,
        language: Language,
    ) -> QuestionScoreDetail:
        """Evalúa preguntas de rellenar hueco."""
        question_info = self.question_pool.get(question_id, {})
        accepted_answers: List[str] = question_info.get("accepted_answers") or []

        s, conf, explanation = score_fill_blank(answer_text, accepted_answers, language)
        return QuestionScoreDetail(
            question_id=question_id,
            type=question_type,
            score=s,
            max_score=1.0,
            explanation=explanation,
            confidence=conf,
            needs_human_review=False,
            language_detected=language,
        )

    def _evaluate_ordering(
        self,
        question_id: str,
        question_type: QuestionType,
        answer_list: List[str],
        language: Language,
    ) -> QuestionScoreDetail:
        """Evalúa preguntas de ordenar elementos."""
        question_info = self.question_pool.get(question_id, {})
        correct_order: List[str] = question_info.get("correct_order") or []

        s, conf, explanation = score_ordering(answer_list, correct_order, language)
        return QuestionScoreDetail(
            question_id=question_id,
            type=question_type,
            score=s,
            max_score=1.0,
            explanation=explanation,
            confidence=conf,
            needs_human_review=False,
            language_detected=language,
        )

    def _evaluate_speaking_record(
        self,
        question_id: str,
        question_type: QuestionType,
        answer_text: str,
        language: Language,
    ) -> QuestionScoreDetail:
        """
        Evalúa preguntas de grabación de voz.

        Si hay transcripción disponible (answer_text), usa el OpenResponseScorer.
        Si no, marca para revisión humana.
        """
        question_info = self.question_pool.get(question_id, {})

        # Si se envió transcripción, puntúa como texto libre
        if answer_text and answer_text.strip():
            rubric = question_info.get("rubric")
            expected_keywords = question_info.get("expected_keywords", [])
            if rubric and isinstance(rubric, dict):
                try:
                    rubric_obj = OpenQuestionRubric(**rubric)
                except Exception:
                    rubric_obj = OpenQuestionRubric(level="A1")
            else:
                rubric_obj = OpenQuestionRubric(level="A1")

            score_result = self.open_response_scorer.score(
                response_text=answer_text,
                rubric=rubric_obj,
                language=language,
                expected_keywords=expected_keywords,
            )
            return QuestionScoreDetail(
                question_id=question_id,
                type=question_type,
                score=score_result.score,
                max_score=1.0,
                explanation=score_result.explanation,
                confidence=score_result.confidence * 0.85,  # penalización por transcripción
                needs_human_review=True,
                rubric_breakdown=score_result.rubric_breakdown,
                language_detected=score_result.language_detected,
            )

        # Sin transcripción: revisión humana
        msg = (
            "Speaking record received. Pending human review (no transcript available)."
            if language == Language.en
            else "Grabación recibida. Pendiente de revisión humana (sin transcripción disponible)."
        )
        return QuestionScoreDetail(
            question_id=question_id,
            type=question_type,
            score=0.0,
            max_score=1.0,
            explanation=msg,
            confidence=0.0,
            needs_human_review=True,
            language_detected=language,
        )

    # ========================================================================
    # Training
    # ========================================================================

    def train_from_request(self, request: TrainRequest) -> TrainResponse:
        """
        Entrena el modelo a partir de TrainRequest con ejemplos de preguntas.

        Args:
            request: TrainRequest con ejemplos de preguntas y respuestas.

        Returns:
            TrainResponse con información del entrenamiento.
        """
        with self._lock:
            # Almacena preguntas en el pool
            for example in request.examples:
                self.question_pool[example.question_id] = example.model_dump()

            # Realiza análisis de sesgos
            bias_report = self.bias_checker.check_training_data(
                samples=[s.model_dump() for s in request.examples],
                score_field="score",  # Puede no existir en ejemplos
                demographic_field="metadata",
            )

            # Log bias report
            logger.info(f"Bias report: {bias_report.recommendation}")

            # Almacena training history
            self.training_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "train_id": request.train_id or str(uuid4()),
                "num_examples": len(request.examples),
                "bias_report": {
                    "groups_analyzed": bias_report.groups_analyzed,
                    "suspicious_deviations": bias_report.suspicious_deviations,
                    "recommendation": bias_report.recommendation,
                },
            })

            self.initialized = True
            self.trained_samples += len(request.examples)
            self.version = f"v2.0-{self.trained_samples}ex"

            return TrainResponse(
                trained_samples=len(request.examples),
                total_samples_seen=self.trained_samples,
                model_version=self.version,
            )

    def train_incremental(self, samples: List[TrainSample]) -> None:
        """Legacy: Entrena con muestras legacy."""
        with self._lock:
            # Almacena ejemplos
            for sample in samples:
                self.question_pool[sample.question_id] = sample.model_dump()

            self.initialized = True
            self.trained_samples += len(samples)
            self.version = f"v{self.trained_samples}"

    # ========================================================================
    # Legacy predict (compatibilidad)
    # ========================================================================

    def predict(self, sample: ExamFeatures) -> PredictArtifacts:
        """Legacy: Predice con modelo legacy."""
        with self._lock:
            if not self.initialized:
                return self._fallback_score(sample)

            X = self._build_matrix([sample])
            X_scaled = self.scaler.transform(X)
            raw = float(self.regressor.predict(X_scaled)[0])
            if (not np.isfinite(raw)) or abs(raw) > 200.0:
                fallback = self._fallback_score(sample)
                fallback.explanation["mode"] = "fallback-after-anomaly"
                fallback.explanation["raw_prediction"] = raw
                return fallback

            anchor = self._fallback_score(sample).score
            model_weight = float(np.clip(self.trained_samples / 300.0, 0.15, 0.8))
            anchor_weight = 1.0 - model_weight
            blended = (model_weight * raw) + (anchor_weight * anchor)
            score = float(np.clip(blended, 0.0, 100.0))
            disagreement = abs(raw - anchor)
            confidence_base = 0.4 + min(self.trained_samples, 500) / 1200.0
            confidence_penalty = min(0.25, disagreement / 200.0)
            confidence = max(0.2, min(0.95, confidence_base - confidence_penalty))

            return PredictArtifacts(
                score=round(score, 2),
                level=self._score_to_level(score),
                confidence=round(confidence, 3),
                explanation={
                    "mode": "sgd-regressor",
                    "trained_samples": self.trained_samples,
                    "raw_prediction": round(raw, 3),
                    "anchor_score": round(anchor, 3),
                    "blended_prediction": round(blended, 3),
                    "model_weight": round(model_weight, 3),
                    "anchor_weight": round(anchor_weight, 3),
                },
            )

    def _build_matrix(self, samples):
        rows = []
        texts = []
        for sample in samples:
            rows.append(self._build_numeric_features(sample))
            texts.append(self._build_text(sample))

        numeric = csr_matrix(np.vstack(rows))
        text = self.vectorizer.transform(texts)
        return hstack([numeric, text], format="csr")

    # ========================================================================
    # Persistence
    # ========================================================================

    def reset(self) -> None:
        """Reset del modelo."""
        with self._lock:
            self.scaler = StandardScaler(with_mean=False)
            self.regressor = SGDRegressor(
                loss="huber",
                epsilon=1.35,
                alpha=0.001,
                learning_rate="adaptive",
                eta0=0.001,
                max_iter=1,
                tol=None,
                average=True,
                random_state=42,
            )
            self.question_pool = {}
            self.training_history = []
            self.initialized = False
            self.trained_samples = 0
            self.version = "v2.0"

    def save(self, path: Path = MODEL_PATH) -> Path:
        """Guarda el modelo."""
        with self._lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            joblib.dump(
                {
                    "regressor": self.regressor,
                    "scaler": self.scaler,
                    "initialized": self.initialized,
                    "trained_samples": self.trained_samples,
                    "version": self.version,
                    "question_pool": self.question_pool,
                    "training_history": self.training_history,
                },
                path,
            )
        return path

    def load(self, path: Path = MODEL_PATH) -> bool:
        """Carga el modelo."""
        if not path.exists():
            return False

        payload = joblib.load(path)
        with self._lock:
            self.regressor = payload["regressor"]
            self.scaler = payload.get("scaler", StandardScaler(with_mean=False))
            self.initialized = bool(payload["initialized"])
            self.trained_samples = int(payload["trained_samples"])
            self.version = str(payload["version"])
            self.question_pool = payload.get("question_pool", {})
            self.training_history = payload.get("training_history", [])
        return True
