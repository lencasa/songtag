# SongTag 🎵

Batch audio identifier and MP3 tagger. Drop files → Shazam identifies them → edit metadata → download tagged MP3s.

**Stack:** Streamlit · SongRec · eyeD3

---

## Deploy with Docker Compose (recommended)

**Prerequisites:** Docker + Docker Compose installed on your machine or server.

```bash
# 1. Download the compose file
curl -O https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/songtag/main/docker-compose.yml

# 2. Edit it — replace YOUR_GITHUB_USERNAME with your actual username
#    (or leave build: . to build locally)

# 3. Pull and start
docker compose up -d

# 4. Open in browser
open http://localhost:8501
```

To stop: `docker compose down`  
To update: `docker compose pull && docker compose up -d`

---

## Build and run locally (no Compose)

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/songtag.git
cd songtag
docker build -t songtag .
docker run -p 8501:8501 songtag
```

---

## Run without Docker (dev)

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/songtag.git
cd songtag

# Install SongRec (Linux)
curl -fsSL https://github.com/marin-m/SongRec/releases/latest/download/songrec-linux-x86_64 \
  -o /usr/local/bin/songrec && chmod +x /usr/local/bin/songrec

pip install -r requirements.txt
streamlit run app.py
```

---

## How it works

1. Drop one or more audio files (MP3, WAV, FLAC, M4A, OGG, AAC)
2. Click **Identify All** — SongRec fingerprints each file against Shazam
3. Review identified tracks with album art, year, genre, and album badges
4. Optionally override year/genre globally or per-track
5. Click **Tag & Download All** — eyeD3 writes ID3 tags + embeds Shazam cover art
