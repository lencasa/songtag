FROM python:3.11-slim

# System deps: songrec needs Rust audio libs, ffmpeg for format support
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libasound2-dev \
    libssl-dev \
    pkg-config \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install songrec binary from GitHub releases (pre-built, no Rust toolchain needed)
RUN curl -fsSL \
    https://github.com/marin-m/SongRec/releases/latest/download/songrec-linux-x86_64 \
    -o /usr/local/bin/songrec \
    && chmod +x /usr/local/bin/songrec

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Streamlit config — disable telemetry, set port
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py"]
