from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Language(str, Enum):
    """Idiomas soportados: 'en' para inglés, 'fr' para francés."""
    en = "en"
    fr = "fr"


class LearnerBackground(str, Enum):
    advanced = "advanced"
    normal = "normal"
    none = "none"


class QuestionType(str, Enum):
    mcq = "mcq"
    short_answer = "short_answer"
    essay = "essay"
    open = "open"  # Nuevo tipo para preguntas abiertas


class DELFLevel(str, Enum):
    A1_minus = "A1-"
    A1 = "A1"
    A1_plus = "A1+"
    A2_minus = "A2-"
    A2 = "A2"
    A2_plus = "A2+"
    B1_minus = "B1-"
    B1 = "B1"
    B1_plus = "B1+"
    B2_minus = "B2-"
    B2 = "B2"
    B2_plus = "B2+"


# ============================================================================
# DELF Rubric and Scoring
# ============================================================================
class RubricCriteria(BaseModel):
    """Criterios DELF para evaluación de preguntas abiertas."""
    task_realisation: float = Field(default=0.25, ge=0, le=1, description="Réalisation de la tâche")
    coherence: float = Field(default=0.20, ge=0, le=1, description="Cohérence/Cohésion")
    sociolinguistic: float = Field(default=0.15, ge=0, le=1, description="Adéquation sociolinguistique")
    lexicon: float = Field(default=0.20, ge=0, le=1, description="Lexique")
    morphosyntax: float = Field(default=0.20, ge=0, le=1, description="Morphosyntaxe")

    def validate_total(self) -> bool:
        """Asegurar que los pesos sumen 1.0."""
        total = self.task_realisation + self.coherence + self.sociolinguistic + self.lexicon + self.morphosyntax
        return abs(total - 1.0) < 0.001


class RubricBreakdown(BaseModel):
    """Desglose de puntuaciones por criterio DELF."""
    task_realisation: float = Field(ge=0, le=1)
    coherence: float = Field(ge=0, le=1)
    sociolinguistic: float = Field(ge=0, le=1)
    lexicon: float = Field(ge=0, le=1)
    morphosyntax: float = Field(ge=0, le=1)

    def weighted_score(self, weights: RubricCriteria) -> float:
        """Calcula el score ponderado usando los criterios."""
        return (
            self.task_realisation * weights.task_realisation
            + self.coherence * weights.coherence
            + self.sociolinguistic * weights.sociolinguistic
            + self.lexicon * weights.lexicon
            + self.morphosyntax * weights.morphosyntax
        )


class OpenQuestionRubric(BaseModel):
    """Rúbrica DELF para una pregunta abierta."""
    level: DELFLevel = Field(description="Nivel DELF esperado")
    expected_min_words: int = Field(default=20, ge=1)
    expected_keywords: List[str] = Field(default_factory=list, description="Palabras clave esperadas")
    criteria_weights: RubricCriteria = Field(default_factory=RubricCriteria)

    class Config:
        json_schema_extra = {
            "example": {
                "level": "A1",
                "expected_min_words": 20,
                "expected_keywords": ["aujourd'hui", "bien", "travail"],
                "criteria_weights": {
                    "task_realisation": 0.25,
                    "coherence": 0.20,
                    "sociolinguistic": 0.15,
                    "lexicon": 0.20,
                    "morphosyntax": 0.20,
                },
            }
        }


class ExampleAnswer(BaseModel):
    """Ejemplo de respuesta para entrenamiento."""
    text: str = Field(min_length=1)
    score: float = Field(ge=0, le=1)


# ============================================================================
# Questions and Exams
# ============================================================================
class QuestionAttempt(BaseModel):
    """Attempt de una pregunta durante un examen."""
    question_id: Optional[str] = None
    question_type: QuestionType
    answer_text: str = Field(default="", description="Texto de respuesta del usuario")
    time_spent_sec: float = Field(ge=0)
    max_points: float = Field(default=1.0, ge=0)
    obtained_points: Optional[float] = Field(default=None, ge=0)
    is_correct: Optional[bool] = None
    difficulty: int = Field(default=3, ge=1, le=5)


class MCQQuestion(BaseModel):
    """Pregunta de opción múltiple para entrenamiento."""
    question_id: str
    text: str
    type: QuestionType = QuestionType.mcq
    language: Language = Language.fr
    options: List[str]
    answer: str
    difficulty: int = Field(default=1, ge=1, le=5)


class OpenQuestion(BaseModel):
    """Pregunta abierta para entrenamiento."""
    question_id: str
    text: str
    type: QuestionType = QuestionType.open
    language: Language = Language.fr
    difficulty: int = Field(default=2, ge=1, le=5)
    rubric: OpenQuestionRubric
    expected_keywords: List[str] = Field(default_factory=list)
    examples_answers: List[ExampleAnswer] = Field(default_factory=list)


class QuestionForExam(BaseModel):
    """Pregunta durante un examen predicción."""
    question_id: str
    type: QuestionType
    text: str
    language: Language = Language.fr  # Será detectado automáticamente si no se proporciona


class QuestionResponse(BaseModel):
    """Respuesta a una pregunta."""
    question_id: str
    type: QuestionType
    answer_text: str
    time_spent_sec: float = Field(default=0, ge=0)


# ============================================================================
# Training
# ============================================================================
class TrainSample(BaseModel):
    """Sample de entrenamiento con metadata."""
    question_id: str
    text: str
    type: QuestionType
    language: Language = Language.fr  # Idioma de la pregunta
    difficulty: int = Field(ge=1, le=5)
    expected_keywords: Optional[List[str]] = None
    rubric: Optional[OpenQuestionRubric] = None
    examples_answers: Optional[List[ExampleAnswer]] = None
    # Para MCQ
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    # Metadata
    metadata: Optional[Dict[str, str]] = None


class TrainRequest(BaseModel):
    """Request para entrenar el modelo."""
    train_id: Optional[str] = None
    examples: List[TrainSample] = Field(min_length=1)
    metadata: Optional[Dict[str, str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "train_id": "t2026-03-11-01",
                "examples": [
                    {
                        "question_id": "q1",
                        "text": "Write a short message about your day.",
                        "type": "open",
                        "difficulty": 2,
                        "expected_keywords": ["aujourd'hui", "bien", "travail"],
                        "rubric": {
                            "level": "A1",
                            "expected_min_words": 20,
                            "expected_keywords": ["aujourd'hui", "bien", "travail"],
                            "criteria_weights": {
                                "task_realisation": 0.25,
                                "coherence": 0.20,
                                "sociolinguistic": 0.15,
                                "lexicon": 0.20,
                                "morphosyntax": 0.20,
                            },
                        },
                        "examples_answers": [{"text": "Aujourd'hui j'ai travaillé.", "score": 0.6}],
                    },
                    {
                        "question_id": "q2",
                        "type": "mcq",
                        "text": "Quelle est la couleur du ciel?",
                        "options": ["bleu", "vert", "rouge"],
                        "answer": "bleu",
                        "difficulty": 1,
                    },
                ],
                "metadata": {"source": "corpusX", "language": "fr"},
            }
        }


class TrainResponse(BaseModel):
    trained_samples: int
    total_samples_seen: int
    model_version: str


# ============================================================================
# Prediction and Adaptive Testing
# ============================================================================
class QuestionScoreDetail(BaseModel):
    """Detalles de puntuación para una pregunta."""
    question_id: str
    type: QuestionType
    score: float = Field(ge=0, le=1)
    max_score: float = Field(default=1.0)
    explanation: str = Field(default="")
    confidence: float = Field(ge=0, le=1)
    needs_human_review: bool = Field(default=False)
    language_detected: Language = Language.fr  # Idioma detectado/usado
    # Solo para preguntas abiertas
    rubric_breakdown: Optional[RubricBreakdown] = None
    human_score: Optional[float] = Field(default=None, ge=0, le=1)


class NextQuestionRecommendation(BaseModel):
    """Recomendación de siguiente pregunta para examen adaptativo."""
    difficulty: int = Field(ge=1, le=5)
    topic: Optional[str] = None
    reason: str = Field(default="")


class PredictRequest(BaseModel):
    """Request para predicción/evaluación."""
    exam_id: str = Field(description="Identificador único del examen")
    candidate_id: Optional[str] = None
    adaptive: bool = Field(default=False, description="Activar examen adaptativo")
    questions: List[QuestionForExam] = Field(min_length=1)
    answers: List[QuestionResponse] = Field(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "exam_id": "ex-001",
                "candidate_id": "cand-123",
                "adaptive": True,
                "questions": [
                    {"question_id": "q1", "type": "open", "text": "Describe tu día."},
                    {"question_id": "q2", "type": "mcq", "text": "Qué color es el cielo?"},
                ],
                "answers": [
                    {"question_id": "q1", "type": "open", "answer_text": "Hoy fue un buen día.", "time_spent_sec": 120},
                    {"question_id": "q2", "type": "mcq", "answer_text": "azul", "time_spent_sec": 15},
                ],
            }
        }


class PredictResponse(BaseModel):
    """Response de predicción/evaluación."""
    exam_id: str
    candidate_id: Optional[str] = None
    per_question: List[QuestionScoreDetail]
    estimated_level: DELFLevel
    confidence: float = Field(ge=0, le=1)
    next_question_recommendation: Optional[NextQuestionRecommendation] = None
    evaluation_meta: Dict[str, str] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "exam_id": "ex-001",
                "candidate_id": "cand-123",
                "per_question": [
                    {
                        "question_id": "q1",
                        "type": "open",
                        "score": 0.62,
                        "max_score": 1.0,
                        "rubric_breakdown": {
                            "task_realisation": 0.6,
                            "coherence": 0.7,
                            "sociolinguistic": 0.5,
                            "lexicon": 0.6,
                            "morphosyntax": 0.6,
                        },
                        "confidence": 0.58,
                        "needs_human_review": True,
                        "explanation": "Falta detalle; hay conectores básicos; vocabulario limitado.",
                    }
                ],
                "estimated_level": "A2",
                "confidence": 0.72,
                "next_question_recommendation": {"difficulty": 3, "topic": "habits", "reason": "Score moderado, aumentar dificultad"},
                "evaluation_meta": {"model_version": "v2.0", "timestamp": "2026-03-11T10:30:00Z"},
            }
        }


# ============================================================================
# Legacy Compatibility
# ============================================================================
class ExamFeatures(BaseModel):
    """Legacy: para mantener compatibilidad con código existente."""
    language: Language
    learner_background: LearnerBackground
    questions: List[QuestionAttempt] = Field(min_length=1)


# ============================================================================
# API Status
# ============================================================================
class HealthResponse(BaseModel):
    status: str
    model_version: str
    trained_samples: int
    initialized: bool
