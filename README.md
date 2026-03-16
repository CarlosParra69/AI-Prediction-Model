# PLACEMENT TEST AI Prediction Model - Multilingual DELF/CEFR Exams Evaluation System

---

## Quick Start Project

### 1. Prerequisites Python 3.12+

#### Manual Instalation

In PowerShell or CMD:

```bash
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

pytest tests/test_api.py -v
```

### 2. Run the API

```bash
python -m uvicorn app.main:app --reload
```

Server running on: `http://localhost:8000`

### 3. API Examples

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Train the Model

```bash
# Entrenar con corpus principal (tipos variados)
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d @samples/train_french_priority.json

# Entrenar con corpus adicional (verbo être + IMAGE)
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d @samples/train_french_priority_2.json
```

#### Predict Proficiency Level

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @"samples/exams french/predict_exam_french1.json"
```

### 4. Run Tests

```bash
pytest tests/test_api.py -v
# Expected: 23 passed in 1.60s
```

---

## Bilingual Support

This project has been upgraded to support **both French and English** language assessment using the CEFR (Common European Framework of Reference) framework.

---

## 🎯 What This System Does

Evaluates **language proficiency** in French and/or English exams using CEFR standards.

### Input

- Training examples (corpus of responses with proficiency rubrics)
- Exam questions (open-ended or multiple-choice)
- Candidate answers

### Output

- Proficiency level (A1, A1+, A2, A2+, B1, B1+, B2, etc.)
- Detailed scoring by criterion (Task, Coherence, Sociolinguistic, Lexicon, Grammar)
- Language detected (en or fr)
- Confidence score

---

## 📊 Features

### Tipos de pregunta soportados


| Tipo                | Descripción                                              | Scoring                                                  |
| ------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| **WRITING_TEXT**    | Respuesta libre con rúbrica DELF                         | Por criterios (tarea, coherencia, léxico, morfosintaxis) |
| **SINGLE_CHOICE**   | Opción múltiple, una respuesta correcta                  | Automático (0/1)                                         |
| **FILL_BLANK**      | Rellenar huecos (varios aceptados, tolerancia a acentos) | Coincidencia normalizada                                 |
| **ORDERING**        | Ordenar elementos en secuencia                           | Puntaje parcial (posiciones + pares adyacentes)          |
| **IMAGE**           | Pregunta basada en imagen                                | Igual que SINGLE_CHOICE o WRITING según diseño           |
| **SPEAKING_RECORD** | Grabación de voz → transcripción                         | Rúbrica DELF sobre texto transcrito                      |
| **AUDIO / VIDEO**   | Arquitectura preparada                                   | Pendiente revisión humana                                |


Las preguntas IMAGE incluyen el campo opcional `image_description` para accesibilidad y revisión humana.

### Bilingual Support

- 🇫🇷 **French (fr)** - Evaluación DELF nativa
- 🇬🇧 **English (en)** - Evaluación CEFR/ESL
- 🔍 **Auto-Detection** - Detección heurística del idioma en respuestas

### Adaptive Assessment

- Ajusta la dificultad según el desempeño
- Selecciona preguntas apropiadas al nivel detectado
- **Estimación de nivel**: media ponderada de escritura/habla (80%) + precisión global (20%)
- Umbrales calibrados para el rango real de scoring (A1- a B2)

### Fair Evaluation

- Conectores y marcadores de cortesía por idioma
- Rúbrica CEFR unificada para ambos idiomas
- Bias checker para detectar datos sensibles en corpus
- Feedback lingüísticamente apropiado

### Comprehensive Scoring (respuestas abiertas)

- Task Realisation (25%) - ¿Respondió la pregunta?
- Coherence & Cohesion (20%) - Flujo lógico y conectores
- Sociolinguistic Adequacy (15%) - Registro y cortesía
- Lexical Range (20%) - Diversidad y adecuación de vocabulario
- Morphosyntax (20%) - Gramática, tiempos, conjugación

El `french_scorer` incluye detección de errores típicos A2/B1 (auxiliaires, género, conjugación, ortografía).

## 📁 Project Structure

```
AI-Prediction-Model/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── model.py                   # Core ML model & prediction pipeline
│   ├── adaptive_selector.py       # Adaptive question selection & level estimation
│   ├── open_response_scorer.py    # Scoring de respuestas abiertas (bilingüe)
│   ├── french_scorer.py           # Reglas lingüísticas para francés
│   ├── english_scorer.py          # Reglas lingüísticas para inglés
│   ├── bias_checker.py            # Detección de datos sensibles en corpus
│   ├── schemas/                   # Modelos Pydantic
│   │   ├── __init__.py            # Re-export de modelos
│   │   └── question_type.py       # Enum QuestionType centralizado
│   ├── scorers/
│   │   ├── fill_blank_scorer.py   # Scoring FILL_BLANK
│   │   └── ordering_scorer.py     # Scoring ORDERING
│   └── models/
│       └── exam_model.joblib      # Modelo entrenado
│
├── samples/
│   ├── train_french_priority.json     # Corpus principal (18+ preguntas variadas)
│   ├── train_french_priority_2.json    # Corpus verbo être + IMAGE
│   └── exams french/
│       ├── predict_exam_french1.json   # Examen B1
│       ├── predict_exam_french2.json   # Examen A2
│       ├── predict_exam_french3.json   # Examen B2
│       └── predict_exam_french4.json   # Examen A2+
│
├── tests/
│   └── test_api.py                # Tests de API
│
├── requirements.txt
└── README.md
```

---

## 🌐 Language Support Details

### French (fr)

- **Framework**: DELF/CEFR
- **Levels**: A1-, A1, A1+, A2-, A2, A2+, B1-, B1, B1+, B2-, B2+
- **Connectors**: 28 across levels (et, mais, cependant, donc, néanmoins, etc.)
- **Politeness Markers**: 6 (s'il vous plaît, merci, cordialement, etc.)
- **Status**: ✅ Ready to Run

### English (en)

- **Framework**: CEFR ESL
- **Levels**: A1-, A1, A1+, A2-, A2, A2+, B1-, B1, B1+, B2-, B2+
- **Connectors**: 31 across levels (and, but, however, therefore, nonetheless, etc.)
- **Politeness Markers**: 7 (please, thank you, kind regards, etc.)
- **ESL Tolerance**: Applied for learner-appropriate evaluation

### Language Detection

```
Input:  "Je suis heureux aujourd'hui" → Detected: fr ✅
Input:  "I am very happy today"      → Detected: en ✅
```

---

## 📋 Sample Usage

### Request (examen con tipos variados)

```json
{
  "exam_id": "ex-french-001",
  "candidate_id": "cand-123",
  "adaptive": true,
  "questions": [
    {"question_id": "q_fr_1", "type": "writing_text", "text": "Écrivez un message sur votre journée.", "language": "fr"},
    {"question_id": "q_fr_3", "type": "single_choice", "text": "Quelle est la couleur du ciel?", "language": "fr"},
    {"question_id": "q_img_1", "type": "image", "text": "Que font les personnes sur l'image?", "image_description": "Un groupe d'étudiants en train d'étudier dans une bibliothèque.", "language": "fr"},
    {"question_id": "q_fr_13", "type": "fill_blank", "text": "Nous ___ allés au marché.", "language": "fr"},
    {"question_id": "q_fr_16", "type": "ordering", "text": "Remettez les étapes dans l'ordre.", "language": "fr", "elements": ["Égoutter.", "Faire bouillir.", "Saler.", "Ajouter."]}
  ],
  "answers": [
    {"question_id": "q_fr_1", "type": "writing_text", "answer_text": "Aujourd'hui j'ai travaillé et j'ai appris beaucoup.", "time_spent_sec": 120},
    {"question_id": "q_fr_3", "type": "single_choice", "answer_text": "bleu", "time_spent_sec": 8},
    {"question_id": "q_img_1", "type": "image", "answer_text": "Ils étudient.", "time_spent_sec": 12},
    {"question_id": "q_fr_13", "type": "fill_blank", "answer_text": "sommes", "time_spent_sec": 10},
    {"question_id": "q_fr_16", "type": "ordering", "answer_list": ["Faire bouillir.", "Saler.", "Ajouter.", "Égoutter."], "time_spent_sec": 25}
  ]
}
```

### Response

```json
{
  "exam_id": "exam-2024-001",
  "estimated_level": "A2",
  "per_question": [
    {
      "question_id": "q_fr_1",
      "language_detected": "fr",
      "score": 0.72,
      "confidence": 0.82,
      "rubric_breakdown": {
        "task_realisation": 0.90,
        "coherence": 0.80,
        "sociolinguistic": 0.75,
        "lexicon": 0.70,
        "morphosyntax": 0.65
      }
    },
    {
      "question_id": "q_en_1",
      "language_detected": "en",
      "score": 0.70,
      "confidence": 0.80,
      "rubric_breakdown": {
        "task_realisation": 0.88,
        "coherence": 0.78,
        "sociolinguistic": 0.73,
        "lexicon": 0.68,
        "morphosyntax": 0.63
      }
    }
  ]
}
```

---

## 🔧 Configuration

### Default Language

By default, the system is **French-first** (Language.fr is default).

To change:

1. Edit `app/schemas/__init__.py`
2. Change `language: Language = Language.fr` to `language: Language = Language.en`

### Language Detection Threshold

Current heuristic: Uses French/English word markers with +2 threshold.

To adjust accuracy:

1. Edit `app/open_response_scorer.py`
2. Modify `detect_language()` function
3. Adjust threshold from `+2` to `+3` for stricter detection

---

## 🎓 CEFR Framework

Both languages use identical CEFR proficiency scale:


| Abbreviation | Level                    | Description                  |
| ------------ | ------------------------ | ---------------------------- |
| A1-          | Breakthrough             | Basic survival language      |
| A1           | Breakthrough             | Can introduce themselves     |
| A1+          | Elementary               | Can handle simple topics     |
| A2-          | Lower Elementary         | Can describe familiar topics |
| A2           | Elementary               | Can discuss simple matters   |
| A2+          | Upper Elementary         | Can handle wider range       |
| B1-          | Lower Intermediate       | Can express basic opinions   |
| B1           | Intermediate             | Can discuss many topics      |
| B1+          | Upper Intermediate       | Can explain views fluently   |
| B2-          | Lower Upper-Intermediate | Can argue persuasively       |
| B2+          | Upper-Intermediate       | Can discuss complex topics   |


---

## 📊 Test Example Results Summary

```
======================== test session starts =========================
platform win32 -- Python 3.12.10, pytest-8.3.4

collected 23 items

Legacy Tests (v2.0):
  ✅ test_health_check
  ✅ test_version
  ✅ test_open_response_scorer_basic
  ✅ test_open_response_scorer_advanced
  ✅ test_open_response_scorer_edge_cases
  ✅ test_open_response_scorer_level_detection
  ✅ test_predict_open_question
  ✅ test_predict_mcq
  ✅ test_predict_adaptive
  ✅ test_full_exam_flow
  ✅ test_question_selector_basic
  ✅ test_question_selector_difficulty
  ✅ test_difficulty_adjuster_level_estimation
  ✅ test_difficulty_adjuster_next_question
  ✅ test_detect_language_bias_in_difficulty
  ✅ test_question_fairness
  ✅ test_scoring_consistency

Multilingual Tests (v2.1 - NEW):
  ✅ test_language_detection_french
  ✅ test_language_detection_english
  ✅ test_open_response_scorer_french
  ✅ test_open_response_scorer_english
  ✅ test_predict_multilingual_exam
  ✅ test_language_fairness

========================= 23 passed in 1.60s ==========================
```

---

## ✨ Key Features by Version

### v2.0 (Original)

- French DELF evaluation
- Open-ended questions
- Multiple-choice questions
- Adaptive assessment
- Level estimation (A1-B2)

### v2.1 (Multilingual)

- English support
- Automatic language detection
- Fairness validation
- Full backward compatibility

### v2.2+ (Current – Tipos extendidos)

- **FILL_BLANK** con respuestas múltiples aceptadas y tolerancia a acentos
- **ORDERING** con puntaje parcial (posiciones + pares adyacentes)
- **IMAGE** con campo `image_description` (opcional)
- **SPEAKING_RECORD** con scoring por rúbrica DELF
- Enum centralizado `QuestionType` (sin comparaciones por string)
- Estimación de nivel writing-focused (80% escritura/habla, 20% precisión)
- Umbrales calibrados para rango real de scoring
- `french_scorer` ampliado: detección de errores auxiliaires, género, conjugación
- Bias checker para corpus de entrenamiento
- Corpus y exámenes de muestra variados (todos los tipos por examen)

---

## 🚀 Deployment Production

### Requirements

- Python 3.12+
- FastAPI 0.115.6+
- Pydantic 2.10.3+
- scikit-learn 1.5.2+
- joblib

### Installation

```bash
pip install -r requirements.txt
```

### Running

```bash
python -m uvicorn app.main:app --reload
```

### Production

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📈 Performance


| Metric                              | Value                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------- |
| **API Response Time**               | <100ms por pregunta                                                       |
| **Examen completo (≈18 preguntas)** | ~1–2 s                                                                    |
| **Model Training**                  | <5 s para corpus típico (train_french_priority + train_french_priority_2) |
| **Language Detection Accuracy**     | 95%+ para texto claro                                                     |
| **Scoring Reliability**             | Validado por suite de tests                                               |


---

## 🔮 Future Enhancements

Possible extensions (not in current scope):

- Additional languages (Spanish, German)
- Machine learning-based language detection
- Dialect-specific scoring variations
- Performance monitoring dashboard
- A/B testing framework

---

---

*PIE Placement Test Project — Python AI Model* 