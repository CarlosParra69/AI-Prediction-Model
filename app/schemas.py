from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Language(str, Enum):
    english = "english"
    french = "french"


class LearnerBackground(str, Enum):
    advanced = "advanced"
    normal = "normal"
    none = "none"


class QuestionType(str, Enum):
    mcq = "mcq"
    short_answer = "short_answer"
    essay = "essay"


class QuestionAttempt(BaseModel):
    question_id: Optional[str] = None
    question_type: QuestionType
    answer_text: str = Field(default="", description="Texto de respuesta del usuario")
    time_spent_sec: float = Field(ge=0)
    max_points: float = Field(default=1.0, ge=0)
    obtained_points: Optional[float] = Field(default=None, ge=0)
    is_correct: Optional[bool] = None
    difficulty: int = Field(default=3, ge=1, le=5)


class ExamFeatures(BaseModel):
    language: Language
    learner_background: LearnerBackground
    questions: List[QuestionAttempt] = Field(min_length=1)


class TrainSample(ExamFeatures):
    final_score: float = Field(ge=0, le=100)


class TrainRequest(BaseModel):
    samples: List[TrainSample] = Field(min_length=1)


class TrainResponse(BaseModel):
    trained_samples: int
    total_samples_seen: int
    model_version: str


class PredictRequest(ExamFeatures):
    pass


class PredictResponse(BaseModel):
    predicted_score: float
    predicted_level: str
    confidence: float
    explanation: dict


class HealthResponse(BaseModel):
    status: str
    model_version: str
    trained_samples: int
    initialized: bool
