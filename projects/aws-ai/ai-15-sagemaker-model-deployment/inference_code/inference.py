import json
from typing import Any, Dict, List

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


LABELS = {
    0: "negative",
    1: "neutral",
    2: "positive",
}


def model_fn(model_dir: str) -> Dict[str, Any]:
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    return {
        "model": model,
        "tokenizer": tokenizer,
    }


def input_fn(request_body: str, request_content_type: str) -> Dict[str, List[str]]:
    if request_content_type != "application/json":
        raise ValueError(f"Unsupported content type: {request_content_type}")

    payload = json.loads(request_body)
    if isinstance(payload, dict) and isinstance(payload.get("text"), str):
        return {"texts": [payload["text"]]}
    if isinstance(payload, dict) and isinstance(payload.get("texts"), list):
        return {"texts": [str(text) for text in payload["texts"]]}

    raise ValueError("Request must contain either 'text' or 'texts'.")


def predict_fn(input_data: Dict[str, List[str]], model_bundle: Dict[str, Any]) -> Dict[str, Any]:
    tokenizer = model_bundle["tokenizer"]
    model = model_bundle["model"]

    encoded = tokenizer(
        input_data["texts"],
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )

    with torch.no_grad():
        outputs = model(**encoded)
        probabilities = torch.softmax(outputs.logits, dim=-1)
        predicted_ids = torch.argmax(probabilities, dim=-1)

    predictions = []
    for index, predicted_id in enumerate(predicted_ids.tolist()):
        scores = probabilities[index].tolist()
        predictions.append(
            {
                "label_id": predicted_id,
                "label": LABELS.get(predicted_id, str(predicted_id)),
                "score": scores[predicted_id],
            }
        )

    return {"predictions": predictions}


def output_fn(prediction: Dict[str, Any], response_content_type: str) -> str:
    if response_content_type != "application/json":
        raise ValueError(f"Unsupported response content type: {response_content_type}")
    return json.dumps(prediction)
