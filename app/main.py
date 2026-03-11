from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .model import MODEL_PATH, OnlineExamModel
from .schemas import HealthResponse, PredictRequest, PredictResponse, TrainRequest, TrainResponse

app = FastAPI(title="Language Exam Online Trainer", version="1.0.0")
model = OnlineExamModel()
model.load()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model_version=model.version,
        trained_samples=model.trained_samples,
        initialized=model.initialized,
    )


@app.get("/version")
def version() -> dict:
    return {"model_version": model.version, "trained_samples": model.trained_samples}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    artifacts = model.predict(payload)
    return PredictResponse(
        predicted_score=artifacts.score,
        predicted_level=artifacts.level,
        confidence=artifacts.confidence,
        explanation=artifacts.explanation,
    )


@app.post("/train", response_model=TrainResponse)
def train(payload: TrainRequest) -> TrainResponse:
    try:
        model.train_incremental(payload.samples)
        model.save(MODEL_PATH)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc

    return TrainResponse(
        trained_samples=len(payload.samples),
        total_samples_seen=model.trained_samples,
        model_version=model.version,
    )


@app.post("/save")
def save_model() -> dict:
    path = model.save(MODEL_PATH)
    return {"saved": True, "path": str(path)}


@app.post("/load")
def load_model() -> dict:
    loaded = model.load(MODEL_PATH)
    return {"loaded": loaded, "path": str(MODEL_PATH)}


@app.post("/reset")
def reset_model(delete_saved_file: bool = False) -> dict:
    model.reset()
    deleted = False
    if delete_saved_file and MODEL_PATH.exists():
        MODEL_PATH.unlink()
        deleted = True
    return {"reset": True, "deleted_saved_file": deleted}
