from __future__ import annotations

import hashlib
from pathlib import Path


def text_to_speech(text: str, output_dir: str = "assets/audio") -> str:
    from gtts import gTTS

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    output_path = Path(output_dir) / f"accessprep-{digest}.mp3"
    if not output_path.exists():
        speech = gTTS(text=text[:4500], lang="en", slow=False)
        speech.save(str(output_path))
    return str(output_path)
