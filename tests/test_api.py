from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_train_then_predict() -> None:
    train_payload = {
        "samples": [
            {
                "language": "english",
                "learner_background": "normal",
                "final_score": 70,
                "questions": [
                    {"question_type": "mcq", "answer_text": "A", "time_spent_sec": 20, "max_points": 1, "is_correct": True, "difficulty": 2},
                    {"question_type": "essay", "answer_text": "Well structured response", "time_spent_sec": 300, "max_points": 10, "obtained_points": 8, "difficulty": 4},
                ],
            }
        ]
    }

    train_response = client.post("/train", json=train_payload)
    assert train_response.status_code == 200
    assert train_response.json()["trained_samples"] == 1

    predict_payload = {
        "language": "english",
        "learner_background": "normal",
        "questions": [
            {"question_type": "mcq", "answer_text": "A", "time_spent_sec": 22, "max_points": 1, "is_correct": True, "difficulty": 2},
            {"question_type": "essay", "answer_text": "Response with clear ideas", "time_spent_sec": 280, "max_points": 10, "difficulty": 4},
        ],
    }

    predict_response = client.post("/predict", json=predict_payload)
    assert predict_response.status_code == 200
    body = predict_response.json()
    assert 0 <= body["predicted_score"] <= 100
    assert body["predicted_level"] in {"A1", "A2", "B1", "B2", "C1", "C2"}
