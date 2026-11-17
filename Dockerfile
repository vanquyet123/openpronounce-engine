FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860

# System deps: ffmpeg (audio decode), espeak-ng (phonemizer), build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        espeak-ng \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install torch CPU first (smaller wheels), then openpronounce + app extras
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
        torch>=2.0 torchaudio>=2.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server + patched entrypoint
COPY server.py .
COPY entrypoint.py .

# Pre-download models is optional; they will download on first request (~1.2GB each).
# To speed up cold start, uncomment the next line (adds ~5 min to build):
# RUN python -c "from openpronounce import speech; speech.transcribe.__wrapped__ if hasattr(speech.transcribe,'__wrapped__') else None" || true

EXPOSE 7860

CMD ["python", "entrypoint.py"]
