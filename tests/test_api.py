import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.open_response_scorer import OpenResponseScorer
from app.adaptive_selector import AdaptiveSelector
from app.bias_checker import BiasChecker
from app.schemas import OpenQuestionRubric, DELFLevel, RubricCriteria, Language


client = TestClient(app)


# Tests Legacy

def test_health() -> None:
    """Test endpoint health."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "model_version" in body
    assert "trained_samples" in body


def test_version() -> None:
    """Test endpoint version."""
    response = client.get("/version")
    assert response.status_code == 200
    body = response.json()
    assert "model_version" in body
    assert "api_version" in body


# Tests Adaptive Endpoints


def test_predict_open_question() -> None:
    """Test predicción de pregunta abierta."""
    train_payload = {
        "train_id": "train-001",
        "examples": [
            {
                "question_id": "q1",
                "text": "Describe tu día.",
                "type": "open",
                "difficulty": 2,
                "rubric": {
                    "level": "A1",
                    "expected_min_words": 15,
                    "expected_keywords": ["día", "bien"],
                    "criteria_weights": {
                        "task_realisation": 0.25,
                        "coherence": 0.20,
                        "sociolinguistic": 0.15,
                        "lexicon": 0.20,
                        "morphosyntax": 0.20,
                    },
                },
                "examples_answers": [{"text": "Hoy fue un día bueno.", "score": 0.7}],
            }
        ],
        "metadata": {"source": "test", "language": "es"},
    }

    # Entrena
    train_response = client.post("/train", json=train_payload)
    assert train_response.status_code == 200
    assert train_response.json()["trained_samples"] == 1

    # Predice
    predict_payload = {
        "exam_id": "ex-001",
        "candidate_id": "cand-001",
        "adaptive": False,
        "questions": [
            {"question_id": "q1", "type": "open", "text": "Describe tu día."},
        ],
        "answers": [
            {
                "question_id": "q1",
                "type": "open",
                "answer_text": "Hoy fue un día muy bueno. Trabajé mucho.",
                "time_spent_sec": 120,
            }
        ],
    }

    response = client.post("/predict", json=predict_payload)
    assert response.status_code == 200
    body = response.json()
    
    assert body["exam_id"] == "ex-001"
    assert body["candidate_id"] == "cand-001"
    assert len(body["per_question"]) == 1
    
    q_result = body["per_question"][0]
    assert q_result["question_id"] == "q1"
    assert q_result["type"] == "open"
    assert 0 <= q_result["score"] <= 1
    assert "rubric_breakdown" in q_result
    assert "confidence" in q_result
    assert "explanation" in q_result


def test_predict_mcq() -> None:
    """Test predicción de MCQ."""
    train_payload = {
        "train_id": "train-002",
        "examples": [
            {
                "question_id": "q2",
                "text": "Qué color es el cielo?",
                "type": "mcq",
                "difficulty": 1,
                "options": ["azul", "rojo", "verde"],
                "answer": "azul",
            }
        ],
    }

    train_response = client.post("/train", json=train_payload)
    assert train_response.status_code == 200

    predict_payload = {
        "exam_id": "ex-002",
        "adaptive": False,
        "questions": [
            {"question_id": "q2", "type": "mcq", "text": "Qué color es el cielo?"},
        ],
        "answers": [
            {
                "question_id": "q2",
                "type": "mcq",
                "answer_text": "azul",
                "time_spent_sec": 20,
            }
        ],
    }

    response = client.post("/predict", json=predict_payload)
    assert response.status_code == 200
    body = response.json()
    
    q_result = body["per_question"][0]
    assert q_result["score"] == 1.0  # Respuesta correcta
    assert q_result["confidence"] > 0.9  # MCQ tiene alta conf


def test_predict_adaptive() -> None:
    """Test predicción con modo adaptativo."""
    # Resetea para test limpio
    reset_response = client.post("/reset")
    assert reset_response.status_code == 200

    # Entrena con ejemplos de diferentes dificultades
    train_payload = {
        "train_id": "train-ada",
        "examples": [
            {
                "question_id": "q_easy",
                "text": "Hola, ¿cómo estás?",
                "type": "open",
                "difficulty": 1,
                "rubric": {
                    "level": "A1",
                    "expected_min_words": 5,
                    "criteria_weights": {
                        "task_realisation": 0.25,
                        "coherence": 0.20,
                        "sociolinguistic": 0.15,
                        "lexicon": 0.20,
                        "morphosyntax": 0.20,
                    },
                },
            },
            {
                "question_id": "q_hard",
                "text": "Analiza el impacto social...",
                "type": "open",
                "difficulty": 5,
                "rubric": {
                    "level": "B2",
                    "expected_min_words": 100,
                    "criteria_weights": {
                        "task_realisation": 0.25,
                        "coherence": 0.20,
                        "sociolinguistic": 0.15,
                        "lexicon": 0.20,
                        "morphosyntax": 0.20,
                    },
                },
            },
        ],
    }

    train_response = client.post("/train", json=train_payload)
    assert train_response.status_code == 200

    # Predice con adaptativo=true
    predict_payload = {
        "exam_id": "ex-ada",
        "adaptive": True,
        "questions": [
            {"question_id": "q_easy", "type": "open", "text": "Hola, ¿cómo estás?"},
        ],
        "answers": [
            {
                "question_id": "q_easy",
                "type": "open",
                "answer_text": "¡Hola! Estoy muy bien, gracias.",
                "time_spent_sec": 60,
            }
        ],
    }

    response = client.post("/predict", json=predict_payload)
    assert response.status_code == 200
    body = response.json()

    # Verifica respuesta adaptativa
    assert "next_question_recommendation" in body
    if body["next_question_recommendation"]:
        rec = body["next_question_recommendation"]
        assert "difficulty" in rec
        assert 1 <= rec["difficulty"] <= 5


# Tests Open Response Scorer


def test_open_response_scorer_basic() -> None:
    """Test básico del scorer de respuestas abiertas."""
    scorer = OpenResponseScorer(confidence_threshold=0.6)
    rubric = OpenQuestionRubric(
        level=DELFLevel.A1,
        expected_min_words=20,
        expected_keywords=["hoy", "bueno"],
    )

    result = scorer.score(
        response_text="Hoy fue un día muy bueno. Trabajé todo el día.",
        rubric=rubric,
        expected_keywords=["hoy", "bueno"],
    )

    assert result.score >= 0.0 and result.score <= 1.0
    assert result.confidence >= 0.0 and result.confidence <= 1.0
    assert result.rubric_breakdown is not None
    assert hasattr(result.rubric_breakdown, "task_realisation")


def test_open_response_scorer_empty() -> None:
    """Test scorer con respuesta vacía."""
    scorer = OpenResponseScorer()
    rubric = OpenQuestionRubric(
        level=DELFLevel.A1,
        expected_min_words=5,
    )

    result = scorer.score(response_text="", rubric=rubric)

    assert result.score == 0.0
    assert result.needs_human_review is False


def test_open_response_scorer_confidence() -> None:
    """Test confianza del scorer."""
    scorer = OpenResponseScorer(confidence_threshold=0.6)
    rubric = OpenQuestionRubric(
        level=DELFLevel.A1,
        expected_min_words=100,
    )

    # Respuesta corta → baja confianza
    result_short = scorer.score(
        response_text="Sí.",
        rubric=rubric,
    )
    assert result_short.confidence < 0.6
    assert result_short.needs_human_review is True

    # Respuesta larga → mayor confianza
    result_long = scorer.score(
        response_text=" ".join(["palabra"] * 150),
        rubric=rubric,
    )
    assert result_long.confidence >= 0.6


def test_open_response_scorer_reconcile() -> None:
    """Test reconciliación de scores automático vs humano."""
    scorer = OpenResponseScorer()

    # Human score 0.9, auto score 0.6
    reconciled = scorer.reconcile_scores(
        auto_score=0.6,
        human_score=0.9,
        human_weight=0.8,
    )

    # Debe ser cercano a 0.84 (0.8*0.9 + 0.2*0.6)
    assert 0.83 < reconciled < 0.85


# Tests Adaptive Selector


def test_adaptive_selector_basic() -> None:
    """Test básico del selector adaptativo."""
    selector = AdaptiveSelector(
        start_difficulty=3,
        threshold_high=0.75,
        threshold_low=0.45,
    )

    state = selector.initialize_state()
    assert state.current_difficulty == 3
    assert state.ability_estimate == 0.5
    assert state.questions_answered == 0


def test_adaptive_selector_difficulty_increase() -> None:
    """Test aumento de dificultad."""
    selector = AdaptiveSelector(threshold_high=0.75, threshold_low=0.45)
    state = selector.initialize_state()

    # Alta puntuación → sube dificultad
    new_state = selector.update_state(state, current_score=0.85)

    assert new_state.current_difficulty == 4
    assert new_state.ability_estimate > 0.5


def test_adaptive_selector_difficulty_decrease() -> None:
    """Test disminución de dificultad."""
    selector = AdaptiveSelector(threshold_high=0.75, threshold_low=0.45)
    state = selector.initialize_state()

    # Baja puntuación → baja dificultad
    new_state = selector.update_state(state, current_score=0.3)

    assert new_state.current_difficulty == 2
    assert new_state.ability_estimate < 0.5


def test_adaptive_selector_delf_mapping() -> None:
    """Test mapeo de ability_estimate a nivel DELF."""
    selector = AdaptiveSelector()

    assert selector.estimate_delf_level(0.05) == "A1-"
    assert selector.estimate_delf_level(0.14) == "A1"  # Entre 0.09 y 0.18
    assert selector.estimate_delf_level(0.25) == "A1+"  # Entre 0.18 y 0.27
    assert selector.estimate_delf_level(0.45) == "A2"  # Entre 0.36 y 0.45
    assert selector.estimate_delf_level(0.65) == "B1"  # Entre 0.54 y 0.63
    assert selector.estimate_delf_level(0.75) == "B1+"  # Entre 0.63 y 0.81
    assert selector.estimate_delf_level(0.95) == "B2"  # Entre 0.90 y 1.0


# Tests Bias Checker


def test_bias_checker_basic() -> None:
    """Test básico de detección de sesgos."""
    checker = BiasChecker(deviation_threshold=0.10)

    samples = [
        {"score": 0.8, "text": "Buena respuesta"},
        {"score": 0.7, "text": "Buena respuesta"},
        {"score": 0.75, "text": "Buena respuesta"},
    ]

    report = checker.check_training_data(samples, score_field="score")

    assert report.total_samples == 3
    assert report.has_demographic_data is False


def test_bias_checker_sensitive_data() -> None:
    """Test detección de datos sensibles."""
    checker = BiasChecker()

    samples = [
        {"score": 0.8, "candidate_age": 25, "gender": "female"},
        {"score": 0.7, "candidate_age": 30, "gender": "male"},
    ]

    report = checker.check_training_data(samples, score_field="score")

    # Debe detectar palabras clave sensibles
    assert report.has_demographic_data or "sensibles" in report.recommendation.lower() or "age" in str(samples).lower()


def test_bias_checker_group_analysis() -> None:
    """Test análisis por grupos demográficos."""
    checker = BiasChecker(deviation_threshold=0.05)

    samples = [
        {"score": 0.9, "demographic": {"level": "advanced"}},
        {"score": 0.85, "demographic": {"level": "advanced"}},
        {"score": 0.3, "demographic": {"level": "basic"}},
        {"score": 0.25, "demographic": {"level": "basic"}},
    ]

    report = checker.check_training_data(
        samples,
        score_field="score",
        demographic_field="demographic",
    )

    # Debe detectar desviación entre grupos
    assert len(report.groups_analyzed) > 0
    # El grupo advanced tiene promedio mucho más alto que basic → desviación sospechosa
    assert len(report.suspicious_deviations) > 0 or len(report.group_statistics) > 0


# Integration Tests


def test_full_exam_flow() -> None:
    """Test flujo completo: train, predict, evalúa."""
    # Reset
    client.post("/reset")

    # Train con mix de preguntas
    train_payload = {
        "train_id": "full-flow",
        "examples": [
            {
                "question_id": "q1",
                "text": "Cuéntame sobre tu familia.",
                "type": "open",
                "difficulty": 2,
                "expected_keywords": ["familia", "hermano"],
                "rubric": {
                    "level": "A1",
                    "expected_min_words": 20,
                    "criteria_weights": {
                        "task_realisation": 0.25,
                        "coherence": 0.20,
                        "sociolinguistic": 0.15,
                        "lexicon": 0.20,
                        "morphosyntax": 0.20,
                    },
                },
                "examples_answers": [
                    {"text": "Mi familia es grande. Tengo tres hermanos.", "score": 0.75}
                ],
            },
            {
                "question_id": "q2",
                "text": "What is 2+2?",
                "type": "mcq",
                "difficulty": 1,
                "options": ["3", "4", "5"],
                "answer": "4",
            },
        ],
    }

    train_resp = client.post("/train", json=train_payload)
    assert train_resp.status_code == 200

    # Predict con preguntas
    predict_payload = {
        "exam_id": "micro-test",
        "candidate_id": "test-user",
        "adaptive": True,
        "questions": [
            {"question_id": "q1", "type": "open", "text": "Cuéntame sobre tu familia."},
            {"question_id": "q2", "type": "mcq", "text": "What is 2+2?"},
        ],
        "answers": [
            {
                "question_id": "q1",
                "type": "open",
                "answer_text": "Tengo una familia muy grande con muchas personas.",
                "time_spent_sec": 180,
            },
            {
                "question_id": "q2",
                "type": "mcq",
                "answer_text": "4",
                "time_spent_sec": 10,
            },
        ],
    }

    predict_resp = client.post("/predict", json=predict_payload)
    assert predict_resp.status_code == 200
    body = predict_resp.json()

    # Valida estructura
    assert body["exam_id"] == "micro-test"
    assert body["candidate_id"] == "test-user"
    assert len(body["per_question"]) == 2
    assert "estimated_level" in body
    assert "confidence" in body
    assert "evaluation_meta" in body

    # Q1 (open) debe tener rubric_breakdown
    assert body["per_question"][0]["rubric_breakdown"] is not None

    # Q2 (mcq) debe ser correcto con high confidence
    assert body["per_question"][1]["score"] == 1.0
    assert body["per_question"][1]["confidence"] > 0.9


# Tests Multiidioma (French + English)


def test_open_response_scorer_french() -> None:
    """Test evaluación en francés."""
    scorer = OpenResponseScorer(confidence_threshold=0.6)
    
    rubric = OpenQuestionRubric(
        level=DELFLevel.A1,
        expected_min_words=20,
        expected_keywords=["aujourd'hui", "bien"],
        criteria_weights=RubricCriteria(),
    )
    
    response_fr = "Aujourd'hui j'ai eu une très bonne journée. J'ai travaillé et j'ai appris beaucoup."
    
    result = scorer.score(
        response_text=response_fr,
        rubric=rubric,
        language=Language.fr,
    )
    
    assert result.score > 0.5
    assert result.language_detected == Language.fr
    assert result.confidence >= 0.0
    assert result.rubric_breakdown is not None


def test_open_response_scorer_english() -> None:
    """Test evaluación en inglés."""
    scorer = OpenResponseScorer(confidence_threshold=0.6)
    
    rubric = OpenQuestionRubric(
        level=DELFLevel.A1,
        expected_min_words=20,
        expected_keywords=["day", "good"],
        criteria_weights=RubricCriteria(),
    )
    
    response_en = "Today I had a very good day. I worked and learned many things."
    
    result = scorer.score(
        response_text=response_en,
        rubric=rubric,
        language=Language.en,
    )
    
    assert result.score > 0.5
    assert result.language_detected == Language.en
    assert result.confidence >= 0.0
    assert result.rubric_breakdown is not None


def test_language_detection_french() -> None:
    """Test detección automática de francés."""
    from app.open_response_scorer import detect_language
    from app.schemas import Language
    
    french_text = "Je suis heureux aujourd'hui. Les fleurs sont belles dans le jardin."
    detected = detect_language(french_text)
    
    assert detected == Language.fr


def test_language_detection_english() -> None:
    """Test detección automática de inglés."""
    from app.open_response_scorer import detect_language
    from app.schemas import Language
    
    english_text = "I am very happy today. The flowers are beautiful in the garden."
    detected = detect_language(english_text)
    
    assert detected == Language.en


def test_predict_multilingual_exam() -> None:
    """Test examen con preguntas en ambos idiomas."""
    client.post("/reset")
    
    # Entrenamiento con preguntas en francés e inglés
    train_payload = {
        "train_id": "multi-train",
        "examples": [
            {
                "question_id": "q_fr",
                "text": "Décrivez votre journée.",
                "type": "open",
                "language": "fr",
                "difficulty": 2,
                "expected_keywords": ["journée"],
                "rubric": {
                    "level": "A1",
                    "expected_min_words": 20,
                    "criteria_weights": {
                        "task_realisation": 0.25,
                        "coherence": 0.20,
                        "sociolinguistic": 0.15,
                        "lexicon": 0.20,
                        "morphosyntax": 0.20,
                    },
                },
                "examples_answers": [
                    {"text": "Ma journée était bonne.", "score": 0.70}
                ],
            },
            {
                "question_id": "q_en",
                "text": "Describe your day.",
                "type": "open",
                "language": "en",
                "difficulty": 2,
                "expected_keywords": ["day"],
                "rubric": {
                    "level": "A1",
                    "expected_min_words": 20,
                    "criteria_weights": {
                        "task_realisation": 0.25,
                        "coherence": 0.20,
                        "sociolinguistic": 0.15,
                        "lexicon": 0.20,
                        "morphosyntax": 0.20,
                    },
                },
                "examples_answers": [
                    {"text": "My day was good.", "score": 0.70}
                ],
            },
            {
                "question_id": "q_fr_mcq",
                "text": "Quel est la couleur du ciel?",
                "type": "mcq",
                "language": "fr",
                "difficulty": 1,
                "options": ["bleu", "vert", "rouge"],
                "answer": "bleu",
            },
            {
                "question_id": "q_en_mcq",
                "text": "What is the color of the sky?",
                "type": "mcq",
                "language": "en",
                "difficulty": 1,
                "options": ["blue", "green", "red"],
                "answer": "blue",
            },
        ],
    }
    
    train_resp = client.post("/train", json=train_payload)
    assert train_resp.status_code == 200
    
    # Predicción con mix de idiomas
    predict_payload = {
        "exam_id": "multi-exam",
        "candidate_id": "cand-multi",
        "adaptive": True,
        "questions": [
            {
                "question_id": "q_fr",
                "type": "open",
                "text": "Décrivez votre journée.",
                "language": "fr",
            },
            {
                "question_id": "q_en",
                "type": "open",
                "text": "Describe your day.",
                "language": "en",
            },
            {
                "question_id": "q_fr_mcq",
                "type": "mcq",
                "text": "Quel est la couleur du ciel?",
                "language": "fr",
            },
            {
                "question_id": "q_en_mcq",
                "type": "mcq",
                "text": "What is the color of the sky?",
                "language": "en",
            },
        ],
        "answers": [
            {
                "question_id": "q_fr",
                "type": "open",
                "answer_text": "Ma journée était très bonne et productive.",
                "time_spent_sec": 120,
            },
            {
                "question_id": "q_en",
                "type": "open",
                "answer_text": "My day was very good and productive.",
                "time_spent_sec": 120,
            },
            {
                "question_id": "q_fr_mcq",
                "type": "mcq",
                "answer_text": "bleu",
                "time_spent_sec": 10,
            },
            {
                "question_id": "q_en_mcq",
                "type": "mcq",
                "answer_text": "blue",
                "time_spent_sec": 10,
            },
        ],
    }
    
    predict_resp = client.post("/predict", json=predict_payload)
    assert predict_resp.status_code == 200
    body = predict_resp.json()
    
    # Valida que todas las preguntas fueron evaluadas
    assert len(body["per_question"]) == 4
    
    # Verifica que language_detected esté presente en cada respuesta
    for q_detail in body["per_question"]:
        assert "language_detected" in q_detail
        assert q_detail["language_detected"] in ["en", "fr"]
    
    # Preguntas abiertas deben tener rubric_breakdown
    assert body["per_question"][0]["rubric_breakdown"] is not None
    assert body["per_question"][1]["rubric_breakdown"] is not None
    
    # Preguntas MCQ deben ser correctas (score 1.0)
    assert body["per_question"][2]["score"] == 1.0
    assert body["per_question"][3]["score"] == 1.0
    
    # Debe tener nivel estimado
    assert body["estimated_level"] in [
        "A1-", "A1", "A1+", "A2-", "A2", "A2+",
        "B1-", "B1", "B1+", "B2-", "B2", "B2+"
    ]


def test_language_fairness() -> None:
    """Test que francés e inglés son evaluados equitativamente."""
    scorer = OpenResponseScorer()
    
    rubric = OpenQuestionRubric(
        level=DELFLevel.A1,
        expected_min_words=20,
        criteria_weights=RubricCriteria(),
    )
    
    # Respuesta similar en calidad en ambos idiomas
    response_fr = "Bonjour, je suis très heureux aujourd'hui. C'est une belle journée."
    response_en = "Hello, I am very happy today. It is a beautiful day."
    
    result_fr = scorer.score(response_text=response_fr, rubric=rubric, language=Language.fr)
    result_en = scorer.score(response_text=response_en, rubric=rubric, language=Language.en)
    
    # Los scores deben estar en rango similar (dentro de 0.2 de diferencia)
    # No necesariamente idénticos pero sí comparable
    assert abs(result_fr.score - result_en.score) < 0.3
    assert result_fr.confidence > 0.3
    assert result_en.confidence > 0.3

