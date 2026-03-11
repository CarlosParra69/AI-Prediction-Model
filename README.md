# Prototipo Python - Modelo IA para examenes de ingles/frances

Este proyecto crea un servicio local en Python (FastAPI) que:

- Recibe datos JSON para entrenamiento incremental (`POST /train`).
- Predice puntaje final y nivel CEFR (`POST /predict`).
- Funciona sin base de datos por ahora (todo en memoria + persistencia opcional a archivo).

## 1) Requisitos

- Python 3.11+
- Windows PowerShell (o terminal equivalente)

## 2) Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Ejecutar API local

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Documentacion Swagger:

- http://127.0.0.1:8000/docs

## 4) Entrenar con JSON

Con PowerShell:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/train" -Method Post -ContentType "application/json" -InFile "samples/train_payload.json"
```

## 5) Predecir con JSON

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -ContentType "application/json" -InFile "samples/predict_payload.json"
```

## 6) Endpoints

- `GET /health`: estado, version del modelo y total de muestras entrenadas.
- `GET /version`: version del modelo actual.
- `POST /train`: entrenamiento incremental con `samples`.
- `POST /predict`: calcula puntaje final y nivel estimado.
- `POST /save`: guarda modelo en `app/models/exam_model.joblib`.
- `POST /load`: recarga modelo guardado.
- `POST /reset`: reinicia el modelo en memoria (opcional borrar archivo guardado con `?delete_saved_file=true`).

## 7) Estructura del JSON

### Train

```json
{
  "samples": [
    {
      "language": "english",
      "learner_background": "normal",
      "final_score": 63,
      "questions": [
        {
          "question_type": "short_answer",
          "answer_text": "Because he was tired",
          "time_spent_sec": 70,
          "max_points": 5,
          "obtained_points": 4,
          "difficulty": 3
        }
      ]
    }
  ]
}
```

Nota CEFR:
- El modelo aplica CEFR en escala `0-100`.
- Si en `final_score` envias puntos del examen (por ejemplo `0-16` cuando tus preguntas suman 16), el entrenamiento lo normaliza automaticamente a porcentaje.
- Si ya envias `final_score` en `0-100`, se usa tal cual.

### Predict

```json
{
  "language": "french",
  "learner_background": "advanced",
  "questions": [
    {
      "question_type": "essay",
      "answer_text": "Texte argumentatif...",
      "time_spent_sec": 320,
      "max_points": 10,
      "difficulty": 4
    }
  ]
}
```

## 8) Pruebas

```bash
pytest -q
```

## 9) Nota de escalabilidad

Este prototipo ya permite aprendizaje incremental en runtime y persistencia local de modelo. El siguiente paso natural para tu caso es mover `samples` a cola + base de datos y ejecutar reentrenamientos por lotes.

## 10) Si aparecen scores anormales (por ejemplo 100 fijo con `raw_prediction` gigante)

1. Reinicia el modelo:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/reset?delete_saved_file=true" -Method Post
```
2. Reentrena con tus JSON desde cero.
