from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Iterable, List

import joblib
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

from .schemas import ExamFeatures, LearnerBackground, Language, QuestionType, TrainSample


MODEL_PATH = Path("app/models/exam_model.joblib")


@dataclass
class PredictArtifacts:
    score: float
    level: str
    confidence: float
    explanation: dict


class OnlineExamModel:
    def __init__(self) -> None:
        self._lock = Lock()
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
        self.initialized = False
        self.trained_samples = 0
        self.version = "v0"
        self._rng_seed = 42

    def _encode_background(self, background: LearnerBackground) -> List[float]:
        levels = [LearnerBackground.none, LearnerBackground.normal, LearnerBackground.advanced]
        return [1.0 if background == level else 0.0 for level in levels]

    def _encode_language(self, language: Language) -> List[float]:
        langs = [Language.english, Language.french]
        return [1.0 if language == lang else 0.0 for lang in langs]

    def _build_numeric_features(self, sample: ExamFeatures) -> np.ndarray:
        questions = sample.questions
        n_questions = len(questions)

        q_types = [q.question_type for q in questions]
        mcq_ratio = q_types.count(QuestionType.mcq) / n_questions
        short_ratio = q_types.count(QuestionType.short_answer) / n_questions
        essay_ratio = q_types.count(QuestionType.essay) / n_questions

        total_time = float(sum(q.time_spent_sec for q in questions))
        avg_time = total_time / n_questions
        avg_difficulty = float(sum(q.difficulty for q in questions)) / n_questions

        # Si hay etiquetas parciales, aprovecha exactitud observada en entrenamiento.
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
            if q.question_type == QuestionType.mcq:
                expected_time += 18.0 + (q.difficulty * 6.0)
            elif q.question_type == QuestionType.short_answer:
                expected_time += 45.0 + (q.difficulty * 12.0)
            else:  # essay
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

    def _normalize_target_score(self, sample: TrainSample) -> float:
        # Regla CEFR: el modelo aprende en escala 0-100.
        # Si el usuario envia score en puntos del examen (ej. 0-16), se normaliza automaticamente.
        total_possible = self._max_points(sample)
        raw = float(sample.final_score)

        if total_possible > 0 and raw <= (total_possible + 1e-8):
            return float(np.clip((raw / total_possible) * 100.0, 0.0, 100.0))
        return float(np.clip(raw, 0.0, 100.0))

    def _build_matrix(self, samples: Iterable[ExamFeatures]):
        rows = []
        texts = []
        for sample in samples:
            rows.append(self._build_numeric_features(sample))
            texts.append(self._build_text(sample))

        numeric = csr_matrix(np.vstack(rows))
        text = self.vectorizer.transform(texts)
        return hstack([numeric, text], format="csr")

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
        if score < 20:
            return "A1"
        if score < 40:
            return "A2"
        if score < 60:
            return "B1"
        if score < 75:
            return "B2"
        if score < 90:
            return "C1"
        return "C2"

    def predict(self, sample: ExamFeatures) -> PredictArtifacts:
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
            # Mezcla adaptativa: con pocos datos, prioriza ancla; con mas datos, prioriza modelo.
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

    def train_incremental(self, samples: List[TrainSample]) -> None:
        y = np.array([self._normalize_target_score(s) for s in samples], dtype=np.float64)
        X = self._build_matrix(samples)

        with self._lock:
            self.scaler.partial_fit(X)
            X_scaled = self.scaler.transform(X)
            idx = np.arange(len(y))
            rng = np.random.default_rng(self._rng_seed + self.trained_samples)
            epochs = 40 if len(y) <= 64 else 20
            for _ in range(epochs):
                rng.shuffle(idx)
                self.regressor.partial_fit(X_scaled[idx], y[idx])
            self.initialized = True
            self.trained_samples += len(samples)
            self.version = f"v{self.trained_samples}"

    def reset(self) -> None:
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
            self.initialized = False
            self.trained_samples = 0
            self.version = "v0"

    def save(self, path: Path = MODEL_PATH) -> Path:
        with self._lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            joblib.dump(
                {
                    "regressor": self.regressor,
                    "scaler": self.scaler,
                    "initialized": self.initialized,
                    "trained_samples": self.trained_samples,
                    "version": self.version,
                },
                path,
            )
        return path

    def load(self, path: Path = MODEL_PATH) -> bool:
        if not path.exists():
            return False

        payload = joblib.load(path)
        with self._lock:
            self.regressor = payload["regressor"]
            self.scaler = payload.get("scaler", StandardScaler(with_mean=False))
            self.initialized = bool(payload["initialized"])
            self.trained_samples = int(payload["trained_samples"])
            self.version = str(payload["version"])
        return True
