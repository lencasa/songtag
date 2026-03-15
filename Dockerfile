FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libasound2-dev \
    libssl-dev \
    pkg-config \
    curl \
    ca-certificates \
    build-essential \
    libglib2.0-dev \
    libsoup-3.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust, then build SongRec from source (no GUI, no GTK — CLI only)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable \
    && . "$HOME/.cargo/env" \
    && cargo install songrec --no-default-features -F ffmpeg \
    && cp "$HOME/.cargo/bin/songrec" /usr/local/bin/songrec \
    && rm -rf "$HOME/.cargo/registry" "$HOME/.cargo/git" "$HOME/.rustup"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py"]
