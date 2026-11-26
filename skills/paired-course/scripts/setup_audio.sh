#!/usr/bin/env bash
# One-time setup for making episode audio on this computer with Kokoro, a free
# open-source voice model that runs locally. Safe to re-run. macOS or Linux.
# Downloads about 120 MB into ~/.cache/kokoro (override with KOKORO_DIR).
set -euo pipefail
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$PATH"
DIR="${KOKORO_DIR:-$HOME/.cache/kokoro}"
mkdir -p "$DIR"

if ! command -v ffmpeg >/dev/null; then
  echo "ffmpeg is missing. Install it first:"
  echo "  macOS:  brew install ffmpeg"
  echo "  Linux:  sudo apt-get install -y ffmpeg"
  exit 1
fi

# kokoro-onnx may have no build for the newest Python, so prefer 3.12 through uv when it is there.
if [ ! -x "$DIR/venv/bin/python" ]; then
  if command -v uv >/dev/null; then
    uv venv --quiet --python 3.12 "$DIR/venv"
  else
    python3 -m venv "$DIR/venv"
  fi
fi
if command -v uv >/dev/null; then
  uv pip install --quiet --python "$DIR/venv/bin/python" kokoro-onnx soundfile numpy
else
  "$DIR/venv/bin/pip" install -q kokoro-onnx soundfile numpy
fi

BASE=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
if [ ! -s "$DIR/kokoro-v1.0.onnx" ]; then
  [ -s "$DIR/kokoro-v1.0.int8.onnx" ] || curl -sSL --fail -o "$DIR/kokoro-v1.0.int8.onnx" "$BASE/kokoro-v1.0.int8.onnx"
fi
[ -s "$DIR/voices-v1.0.bin" ] || curl -sSL --fail -o "$DIR/voices-v1.0.bin" "$BASE/voices-v1.0.bin"

echo "Audio tools ready. Run scripts with: $DIR/venv/bin/python"
