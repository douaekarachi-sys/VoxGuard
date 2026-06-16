"""Deepfake voice detector based on WavLM speaker embeddings."""

import torch
from transformers import Wav2Vec2FeatureExtractor, WavLMModel

from src.utils import cosine_similarity, load_audio

MODEL_NAME = "microsoft/wavlm-base-plus-sd"

# Above this similarity, the test audio is considered the same voice as the reference.
DEFAULT_THRESHOLD = 0.85


class DeepfakeDetector:
    """Compare a test audio against a reference voice using WavLM embeddings."""

    def __init__(self, model_name=MODEL_NAME, device="cpu"):
        self.device = device
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
        self.model = WavLMModel.from_pretrained(model_name).to(device)
        self.model.eval()

    def extract_embedding(self, audio_path):
        """Return a single embedding vector summarizing the audio's voice characteristics."""
        audio = load_audio(audio_path, sr=self.feature_extractor.sampling_rate)
        inputs = self.feature_extractor(
            audio, sampling_rate=self.feature_extractor.sampling_rate, return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mean-pool over time to get a fixed-size embedding.
        embedding = outputs.last_hidden_state.squeeze(0).mean(dim=0)
        return embedding.cpu().numpy()

    def predict(self, reference_audio, test_audio, threshold=DEFAULT_THRESHOLD):
        """Compare `test_audio` to `reference_audio` and classify it as REAL or DEEPFAKE."""
        ref_embedding = self.extract_embedding(reference_audio)
        test_embedding = self.extract_embedding(test_audio)

        similarity = cosine_similarity(ref_embedding, test_embedding)
        is_real = similarity >= threshold
        confidence = similarity if is_real else (1 - similarity)

        return {
            "label": "REAL" if is_real else "DEEPFAKE",
            "similarity": similarity,
            "confidence": min(max(confidence, 0.0), 1.0),
            "threshold": threshold,
        }


if __name__ == "__main__":
    detector = DeepfakeDetector()

    reference = "data/voice_ref/reference.wav"
    test = "data/generated/clone_1.wav"

    result = detector.predict(reference, test)

    print(f"Référence : {reference}")
    print(f"Test       : {test}")
    print(f"Résultat   : {result['label']}")
    print(f"Similarité : {result['similarity']:.4f}")
    print(f"Confiance  : {result['confidence']:.1%}")
