"""Voice cloning generator based on Coqui XTTS-v2."""

from pathlib import Path

import soundfile as sf
import torch
import torchaudio

# XTTS loads/saves audio via torchaudio, which defaults to torchcodec (needs FFmpeg
# shared DLLs that aren't available on this Windows setup). Redirect torchaudio's
# load/save to soundfile, which handles our WAV files without FFmpeg.


def _sf_load(filepath, *args, **kwargs):
    data, sr = sf.read(str(filepath), dtype="float32", always_2d=True)
    return torch.from_numpy(data.T.copy()), sr


def _sf_save(filepath, src, sample_rate, *args, **kwargs):
    data = src.detach().cpu().numpy()
    if data.ndim == 2:
        data = data.T
    sf.write(str(filepath), data, sample_rate)


torchaudio.load = _sf_load
torchaudio.save = _sf_save

from TTS.api import TTS

from src.utils import ensure_dir

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"


class VoiceGenerator:
    """Clone a reference voice and synthesize new speech with it."""

    def __init__(self, model_name=MODEL_NAME, device="cpu"):
        self.tts = TTS(model_name).to(device)

    def clone_voice(self, reference_audio, text, output_path, language="fr"):
        """Synthesize `text` using the voice from `reference_audio`."""
        ensure_dir(str(Path(output_path).parent))
        self.tts.tts_to_file(
            text=text,
            speaker_wav=reference_audio,
            language=language,
            file_path=output_path,
        )
        return output_path

    def generate_phrases(self, reference_audio, phrases, output_dir="data/generated", language="fr"):
        """Clone `reference_audio`'s voice for each phrase, one file per phrase."""
        ensure_dir(output_dir)
        outputs = []
        for i, phrase in enumerate(phrases, start=1):
            output_path = str(Path(output_dir) / f"clone_{i}.wav")
            self.clone_voice(reference_audio, phrase, output_path, language=language)
            outputs.append(output_path)
        return outputs


if __name__ == "__main__":
    PHRASES = [
        "Bonjour, je suis une voix générée par intelligence artificielle.",
        "Ce projet explore les enjeux éthiques des deepfakes audio.",
        "Merci d'avoir écouté cet exemple de clonage vocal.",
    ]

    generator = VoiceGenerator()
    generated_files = generator.generate_phrases("data/voice_ref/reference.wav", PHRASES)

    print("Fichiers générés :")
    for f in generated_files:
        print(f" - {f}")
