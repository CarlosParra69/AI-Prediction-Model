"""
Schemas Pydantic para el sistema de evaluación adaptativa de exámenes DELF.

Re-exporta todos los modelos de datos para mantener compatibilidad
con los imports existentes: ``from .schemas import X``.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .question_type import QuestionType


# ============================================================================
# Enums base
# ============================================================================

class Language(str, Enum):
    """Idiomas soportados."""
    en = "en"
    fr = "fr"


class LearnerBackground(str, Enum):
    advanced = "advanced"
    normal = "normal"
    none = "none"


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
        total = (
            self.task_realisation + self.coherence
            + self.sociolinguistic + self.lexicon + self.morphosyntax
        )
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
    """Rúbrica DELF para una pregunta de texto libre."""

    level: DELFLevel = Field(description="Nivel DELF esperado")
    expected_min_words: int = Field(default=20, ge=1)
    expected_keywords: List[str] = Field(default_factory=list)
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
    """Intento de respuesta durante un examen (legacy)."""

    question_id: Optional[str] = None
    question_type: QuestionType
    answer_text: str = Field(default="")
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
    """Pregunta de texto libre para entrenamiento."""

    question_id: str
    text: str
    type: QuestionType = QuestionType.open
    language: Language = Language.fr
    difficulty: int = Field(default=2, ge=1, le=5)
    rubric: OpenQuestionRubric
    expected_keywords: List[str] = Field(default_factory=list)
    examples_answers: List[ExampleAnswer] = Field(default_factory=list)


class QuestionForExam(BaseModel):
    """Pregunta durante un examen de predicción."""

    question_id: str
    type: QuestionType
    text: str
    language: Language = Language.fr
    # Para IMAGE
    image_url: Optional[str] = Field(default=None, description="URL o referencia de imagen (para IMAGE)")
    image_description: Optional[str] = Field(
        default=None,
        description="Descripción textual de la imagen mostrada al candidato (para IMAGE)",
    )
    # Para ORDERING: elementos disponibles en orden aleatorio
    elements: Optional[List[str]] = Field(default=None, description="Elementos a ordenar (para ORDERING)")


class QuestionResponse(BaseModel):
    """Respuesta del candidato a una pregunta."""

    question_id: str
    type: QuestionType
    answer_text: str = Field(default="")
    # Para ORDERING: lista de elementos en el orden que eligió el candidato
    answer_list: Optional[List[str]] = Field(
        default=None,
        description="Respuesta como lista ordenada (para ORDERING)",
    )
    time_spent_sec: float = Field(default=0, ge=0)


# ============================================================================
# Training
# ============================================================================

class TrainSample(BaseModel):
    """Sample de entrenamiento con metadata."""

    question_id: str
    text: str
    type: QuestionType
    language: Language = Language.fr
    difficulty: int = Field(ge=1, le=5)
    expected_keywords: Optional[List[str]] = None
    rubric: Optional[OpenQuestionRubric] = None
    examples_answers: Optional[List[ExampleAnswer]] = None

    # Para SINGLE_CHOICE / MCQ / IMAGE
    options: Optional[List[str]] = None
    answer: Optional[str] = None

    # Para FILL_BLANK
    accepted_answers: Optional[List[str]] = Field(
        default=None,
        description="Lista de respuestas aceptadas como correctas (para FILL_BLANK)",
    )

    # Para ORDERING
    correct_order: Optional[List[str]] = Field(
        default=None,
        description="Orden correcto de los elementos (para ORDERING)",
    )
    elements: Optional[List[str]] = Field(
        default=None,
        description="Elementos disponibles en orden aleatorio (para ORDERING)",
    )

    # Para IMAGE
    image_url: Optional[str] = Field(default=None, description="URL o referencia de imagen")
    image_description: Optional[str] = Field(
        default=None,
        description="Descripción de la imagen mostrada al candidato (para IMAGE)",
    )

    # Para SPEAKING_RECORD
    audio_recording_ref: Optional[str] = Field(
        default=None,
        description="Referencia al archivo de audio del candidato",
    )

    metadata: Optional[Dict[str, str]] = None


class TrainRequest(BaseModel):
    """Request para entrenar el modelo."""

    train_id: Optional[str] = None
    examples: List[TrainSample] = Field(min_length=1)
    metadata: Optional[Dict[str, str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "train_id": "t2026-03-16-01",
                "examples": [
                    {
                        "question_id": "q1",
                        "text": "Écrivez un message sur votre journée.",
                        "type": "writing_text",
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
                        "type": "single_choice",
                        "text": "Quelle est la couleur du ciel?",
                        "options": ["bleu", "vert", "rouge"],
                        "answer": "bleu",
                        "difficulty": 1,
                    },
                    {
                        "question_id": "q3",
                        "type": "fill_blank",
                        "text": "Le chat est ___ la table.",
                        "accepted_answers": ["sur", "sous", "devant"],
                        "difficulty": 1,
                    },
                    {
                        "question_id": "q4",
                        "type": "ordering",
                        "text": "Ordena las estaciones del año.",
                        "elements": ["automne", "hiver", "printemps", "été"],
                        "correct_order": ["printemps", "été", "automne", "hiver"],
                        "difficulty": 2,
                    },
                    {
                        "question_id": "q_img_1",
                        "type": "image",
                        "text": "What are the people doing in the image?",
                        "image_description": "A group of students studying together in a university library.",
                        "options": ["They are studying.", "They are eating.", "They are playing."],
                        "answer": "They are studying.",
                        "difficulty": 2,
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
    language_detected: Language = Language.fr
    # Solo para WRITING_TEXT / open
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
    adaptive: bool = Field(default=False)
    questions: List[QuestionForExam] = Field(min_length=1)
    answers: List[QuestionResponse] = Field(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "exam_id": "ex-001",
                "candidate_id": "cand-123",
                "adaptive": True,
                "questions": [
                    {"question_id": "q1", "type": "writing_text", "text": "Décrivez votre journée."},
                    {"question_id": "q2", "type": "single_choice", "text": "Quelle couleur est le ciel?"},
                    {"question_id": "q3", "type": "fill_blank", "text": "Le chat est ___ la table."},
                    {
                        "question_id": "q4",
                        "type": "ordering",
                        "text": "Ordena las estaciones.",
                        "elements": ["hiver", "printemps", "été", "automne"],
                    },
                    {
                        "question_id": "q_img_1",
                        "type": "image",
                        "text": "Describe what is happening in the image.",
                        "image_description": "A young woman working on a laptop in a coffee shop.",
                        "language": "en",
                    },
                ],
                "answers": [
                    {"question_id": "q1", "type": "writing_text", "answer_text": "Aujourd'hui j'ai travaillé.", "time_spent_sec": 120},
                    {"question_id": "q2", "type": "single_choice", "answer_text": "bleu", "time_spent_sec": 15},
                    {"question_id": "q3", "type": "fill_blank", "answer_text": "sur", "time_spent_sec": 10},
                    {"question_id": "q4", "type": "ordering", "answer_list": ["printemps", "été", "automne", "hiver"], "time_spent_sec": 30},
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


# ── Re-exportación explícita ─────────────────────────────────────────────────
__all__ = [
    "QuestionType",
    "Language",
    "LearnerBackground",
    "DELFLevel",
    "RubricCriteria",
    "RubricBreakdown",
    "OpenQuestionRubric",
    "ExampleAnswer",
    "QuestionAttempt",
    "MCQQuestion",
    "OpenQuestion",
    "QuestionForExam",
    "QuestionResponse",
    "TrainSample",
    "TrainRequest",
    "TrainResponse",
    "QuestionScoreDetail",
    "NextQuestionRecommendation",
    "PredictRequest",
    "PredictResponse",
    "ExamFeatures",
    "HealthResponse",
]
