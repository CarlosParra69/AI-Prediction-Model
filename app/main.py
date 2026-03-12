from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .model import MODEL_PATH, OnlineExamModel
from .schemas import (
    HealthResponse,
    PredictRequest,
    PredictResponse,
    TrainRequest,
    TrainResponse,
)

app = FastAPI(
    title="Language Exam Online Trainer (Adaptive)",
    version="2.0.0",
    description="API para evaluación adaptativa de exámenes DELF con preguntas abiertas y cerradas.",
)
model = OnlineExamModel()
model.load()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Verifica el estado de la API y el modelo."""
    return HealthResponse(
        status="ok",
        model_version=model.version,
        trained_samples=model.trained_samples,
        initialized=model.initialized,
    )


@app.get("/version")
def version() -> dict:
    """Retorna información de versión del modelo."""
    return {
        "model_version": model.version,
        "trained_samples": model.trained_samples,
        "api_version": "2.0.0",
        "features": ["adaptive_testing", "open_questions", "delf_rubrics", "bias_checking"],
    }


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    """
    Endpoint principal de predicción/evaluación adaptativa.
    
    Soporta:
    - Preguntas abiertas (open) y de opción múltiple (mcq)
    - Evaluación con criterios DELF
    - Modo adaptativo que ajusta dificultad según desempeño
    - Revisión humana cuando confianza es baja
    
    Returns:
        PredictResponse con desglose por pregunta, nivel estimado, y recomendación adaptativa.
    """
    try:
        response = model.predict_adaptive(payload)
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Error en predicción: {str(exc)}",
        ) from exc


@app.post("/train", response_model=TrainResponse)
def train(payload: TrainRequest) -> TrainResponse:
    """
    Endpoint de entrenamiento con ejemplos de preguntas.
    
    Acepta:
    - Preguntas abiertas con rúbricas DELF
    - Preguntas de opción múltiple
    - Ejemplos de respuestas para referencia
    - Metadata sobre el corpus de entrenamiento
    
    Realiza:
    - Validación de estructuras
    - Análisis de sesgos
    - Almacenamiento de ejemplos para evaluación
    
    Returns:
        TrainResponse con información del entrenamiento.
    """
    try:
        response = model.train_from_request(payload)
        model.save(MODEL_PATH)
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {exc}",
        ) from exc


@app.post("/save")
def save_model() -> dict:
    """Guarda el modelo a disco."""
    try:
        path = model.save(MODEL_PATH)
        return {
            "saved": True,
            "path": str(path),
            "version": model.version,
            "trained_samples": model.trained_samples,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Save failed: {exc}",
        ) from exc


@app.post("/load")
def load_model() -> dict:
    """Carga el modelo desde disco."""
    try:
        loaded = model.load(MODEL_PATH)
        return {
            "loaded": loaded,
            "path": str(MODEL_PATH),
            "version": model.version if loaded else "not-loaded",
            "trained_samples": model.trained_samples if loaded else 0,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Load failed: {exc}",
        ) from exc


@app.post("/reset")
def reset_model(delete_saved_file: bool = False) -> dict:
    """Resetea el modelo a estado inicial."""
    try:
        model.reset()
        deleted = False
        if delete_saved_file and MODEL_PATH.exists():
            MODEL_PATH.unlink()
            deleted = True
        return {
            "reset": True,
            "deleted_saved_file": deleted,
            "version": model.version,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Reset failed: {exc}",
        ) from exc


@app.get("/info")
def info() -> dict:
    """Retorna información detallada del modelo y estado."""
    return {
        "version": model.version,
        "trained_samples": model.trained_samples,
        "initialized": model.initialized,
        "questions_in_pool": len(model.question_pool),
        "training_sessions": len(model.training_history),
        "features": {
            "adaptive_testing": True,
            "open_questions": True,
            "delf_rubrics": True,
            "bias_checking": True,
            "human_review": True,
        },
        "recent_training": model.training_history[-3:] if model.training_history else [],
    }

