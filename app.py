import streamlit as st
import zipfile
import io
import html
import subprocess
import json
import tempfile
import os
import requests
import eyed3
from eyed3.core import Date

st.set_page_config(
    page_title="SongTag",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(100,60,220,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(220,80,120,0.12) 0%, transparent 55%),
        #0a0a0f !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.hero { padding: 3rem 0 2rem; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 2.5rem; }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    background: linear-gradient(135deg, #fff 30%, #a78bfa 70%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(167,139,250,0.35) !important;
    border-radius: 16px !important;
    background: rgba(167,139,250,0.04) !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: rgba(167,139,250,0.65) !important; }

/* Center button containers */
[data-testid="stButton"] { display: flex !important; justify-content: center !important; }
[data-testid="stDownloadButton"] { display: flex !important; justify-content: center !important; }

/* Center button containers */
[data-testid="stButton"] { display: flex !important; justify-content: center !important; }
[data-testid="stDownloadButton"] { display: flex !important; justify-content: center !important; }

.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.06em !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(124,58,237,0.5) !important;
}

.stDownloadButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    border-radius: 8px !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    background: rgba(167,139,250,0.08) !important;
    color: #a78bfa !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(167,139,250,0.18) !important;
    border-color: rgba(167,139,250,0.6) !important;
    color: #c4b5fd !important;
}
.stDownloadButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.7), rgba(168,85,247,0.7)) !important;
    border-color: rgba(167,139,250,0.5) !important;
    color: #fff !important;
}

.stTextInput > div > div > input {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8e6f0 !important;
    padding: 0.5rem 0.8rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.15) !important;
}
.stTextInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: rgba(255,255,255,0.4) !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Track cards ── */
.track-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.55rem;
    transition: border-color 0.2s, background 0.2s;
}
.track-card:hover {
    border-color: rgba(167,139,250,0.35);
    background: rgba(167,139,250,0.04);
}
.track-card-err { border-color: rgba(248,113,113,0.2) !important; }
.track-card-inner {
    display: flex;
    align-items: center;
    gap: 0.9rem;
}
.card-art { flex-shrink: 0; }
.card-thumb {
    width: 56px; height: 56px;
    border-radius: 8px;
    object-fit: cover;
    display: block;
}
.card-thumb-placeholder {
    width: 56px; height: 56px;
    border-radius: 8px;
    background: rgba(255,255,255,0.06);
}
.card-body { flex: 1; min-width: 0; }
.card-right {
    flex-shrink: 0;
    text-align: right;
    max-width: 260px;
}
.track-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.3;
    margin-bottom: 0.2rem;
    word-break: break-word;
}
.track-artist {
    font-family: 'DM Mono', monospace;
    font-size: 0.73rem;
    color: rgba(255,255,255,0.38);
}
.track-fname {
    font-family: 'DM Mono', monospace;
    font-size: 0.63rem;
    color: rgba(255,255,255,0.18);
    margin-top: 0.45rem;
    word-break: break-all;
    line-height: 1.4;
}
/* ── Badges ── */
.badge-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.4rem; padding-top: 0.1rem; }
.badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 0.18rem 0.55rem;
    border-radius: 20px;
    letter-spacing: 0.04em;
    white-space: nowrap;
}
.badge-green  { background: rgba(52,211,153,0.12);  color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.badge-purple { background: rgba(167,139,250,0.12); color: #a78bfa; border: 1px solid rgba(167,139,250,0.25); }
.badge-gray   { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.45); border: 1px solid rgba(255,255,255,0.12); }
.badge-red    { background: rgba(248,113,113,0.1);  color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
/* ── Per-track row ── */
.per-track-row {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.6rem 0.9rem 0.4rem;
    margin-bottom: 0.5rem;
}
/* ── Sub-labels ── */
.sub-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(167,139,250,0.55);
    margin-bottom: 0.5rem;
}
/* Cover art rounding everywhere */
[data-testid="stImage"] img { border-radius: 8px !important; object-fit: cover !important; }
/* Dividers */
hr { border-color: rgba(255,255,255,0.05) !important; margin: 0.25rem 0 !important; }
    font-size: 0.7rem; padding: 0.18rem 0.55rem; border-radius: 20px;
    background: rgba(167,139,250,0.12); color: #a78bfa;
    border: 1px solid rgba(167,139,250,0.2); letter-spacing: 0.04em;
}
.meta-chip.green { background: rgba(52,211,153,0.1); color: #34d399; border-color: rgba(52,211,153,0.2); }
.meta-chip.pink  { background: rgba(244,114,182,0.1); color: #f472b6; border-color: rgba(244,114,182,0.2); }
.meta-chip.red   { background: rgba(248,113,113,0.08); color: #f87171; border-color: rgba(248,113,113,0.2); }
.meta-chip.gray  { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.4); border-color: rgba(255,255,255,0.1); }

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

hr { border-color: rgba(255,255,255,0.07) !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #7c3aed, #f472b6) !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">SongTag</div>
  <div class="hero-sub">Shazam identify · auto-tag · batch export</div>
</div>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def identify_file(file_bytes, ext):
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            ["songrec", "audio-file-to-recognized-song", tmp_path],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode != 0:
            return None, f"SongRec error: {result.stderr.strip()}"
        data  = json.loads(result.stdout)
        track = data.get("track", {})
        if not track or not track.get("title"):
            return None, "No match found"

        title  = track.get("title", "Unknown Title")
        artist = track.get("subtitle", "Unknown Artist")
        sections  = track.get("sections", [{}])
        meta_list = sections[0].get("metadata", []) if sections else []
        album     = next((m.get("text","") for m in meta_list if m.get("title")=="Album"), "")
        year_str  = next((m.get("text","") for m in meta_list if m.get("title")=="Released"), "")
        detected_year = year_str if year_str.isdigit() and len(year_str)==4 else ""
        shazam_genre  = track.get("genres", {}).get("primary", "")

        cover_url = track.get("images", {}).get("coverart")
        if not cover_url and sections:
            for page in reversed(sections[0].get("metapages", [])):
                img = page.get("image")
                if img and "mzstatic.com" in img:
                    cover_url = img
                    break

        return {
            "title": title, "artist": artist, "album": album,
            "year": detected_year, "shazam_genre": shazam_genre,
            "cover_url": cover_url,
            "safe_base": f"{artist} - {title}".strip()
        }, None
    except Exception as e:
        return None, str(e)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def tag_file(file_bytes, track_meta, year_val, genre_str):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        audiofile = eyed3.load(tmp_path)
        if audiofile is None:
            raise Exception("Failed to load MP3")
        if audiofile.tag is None:
            audiofile.initTag(version=eyed3.id3.ID3_V2_4)
        tag = audiofile.tag
        tag.title        = track_meta["title"]
        tag.artist       = track_meta["artist"]
        tag.album        = track_meta["album"] or None
        tag.album_artist = track_meta["artist"]

        if year_val:
            d = Date(year_val)
            tag.original_release_date = d
            tag.recording_date        = d
            tag.release_date          = d

        if genre_str.strip():
            tag.genre = genre_str.strip()

        if track_meta.get("cover_url"):
            try:
                r = requests.get(track_meta["cover_url"], timeout=10)
                r.raise_for_status()
                for img in list(tag.images):
                    tag.images.remove(img.description)
                tag.images.set(3, r.content, "image/jpeg", "Front Cover")
            except Exception:
                pass

        tag.save(version=eyed3.id3.ID3_V2_4, encoding='utf-8')
        with open(tmp_path, "rb") as f:
            return f.read(), None
    except Exception as e:
        return None, str(e)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def safe_name(s):
    return "".join(c for c in s if c.isalnum() or c in " -_().&")


# ── Upload ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">01 — Drop your files</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drag & drop audio files — MP3, WAV, M4A, FLAC, OGG, AAC",
    type=["mp3","wav","m4a","ogg","flac","aac"],
    accept_multiple_files=True,
    label_visibility="visible"
)

if uploaded_files:
    st.markdown('<div class="section-label" style="margin-top:2rem">02 — Identify</div>', unsafe_allow_html=True)
    _, col_id, _ = st.columns([2, 3, 2])
    with col_id:
        run_id = st.button("🔍  Identify All", type="primary", use_container_width=True)

    if run_id:
        results = {}
        prog = st.progress(0, text="Starting…")
        for i, uf in enumerate(uploaded_files):
            prog.progress(i / len(uploaded_files), text=f"Identifying {uf.name}…")
            meta, err = identify_file(uf.getvalue(), os.path.splitext(uf.name)[1].lower())
            results[uf.name] = {
                "file_bytes": uf.getvalue(),
                "ext": os.path.splitext(uf.name)[1].lower(),
                "meta": meta,
                "error": err,
            }
        prog.progress(1.0, text="Done!")
        st.session_state["results"]     = results
        st.session_state["files_order"] = [uf.name for uf in uploaded_files]


# ── Results ───────────────────────────────────────────────────────────────────
if "results" in st.session_state and st.session_state["results"]:
    results = st.session_state["results"]
    order   = st.session_state.get("files_order", list(results.keys()))
    found    = [n for n in order if results[n]["meta"]]
    notfound = [n for n in order if not results[n]["meta"]]

    st.markdown('<div class="section-label" style="margin-top:2rem">03 — Results</div>', unsafe_allow_html=True)

    # Summary row
    chips = f'<span class="meta-chip green">✓ {len(found)} identified</span>'
    if notfound:
        chips += f'<span class="meta-chip red">✗ {len(notfound)} not found</span>'
    chips += f'<span class="meta-chip gray">{len(order)} total</span>'
    st.markdown(f'<div style="display:flex;gap:0.6rem;margin-bottom:1.5rem;flex-wrap:wrap">{chips}</div>', unsafe_allow_html=True)

    for name in found:
        m = results[name]["meta"]
        import html as _html
        t  = _html.escape(m["title"])
        ar = _html.escape(m["artist"])
        nm = _html.escape(name)
        badges = ""
        if m["year"]:         badges += f'<span class="badge badge-green">{_html.escape(m["year"])}</span>'
        if m["shazam_genre"]: badges += f'<span class="badge badge-purple">{_html.escape(m["shazam_genre"])}</span>'
        if m["album"]:        badges += f'<span class="badge badge-gray">{_html.escape(m["album"])}</span>'
        thumb = f'<img src="{_html.escape(m["cover_url"])}" class="card-thumb">' if m.get("cover_url") else '<div class="card-thumb-placeholder"></div>'
        st.markdown(f'''
<div class="track-card">
  <div class="track-card-inner">
    <div class="card-art">{thumb}</div>
    <div class="card-body">
      <div class="track-title">{t}</div>
      <div class="track-artist">{ar}</div>
    </div>
    <div class="card-right">
      <div class="badge-row">{badges}</div>
      <div class="track-fname">{nm}</div>
    </div>
  </div>
</div>''', unsafe_allow_html=True)

    for name in notfound:
        err = results[name]["error"] or "No match"
        import html as _html
        st.markdown(f'''
<div class="track-card track-card-err">
  <div class="track-card-inner">
    <div class="card-body"><div class="track-artist">{_html.escape(name)}</div></div>
    <div class="card-right"><span class="badge badge-red">{_html.escape(err)}</span></div>
  </div>
</div>''', unsafe_allow_html=True)

    # ── Tag options ────────────────────────────────────────────────────────
    if found:
        st.markdown('<div class="section-label" style="margin-top:2.5rem">04 — Tag options</div>', unsafe_allow_html=True)
        st.caption("Global overrides apply to all tracks. Per-track fields take priority. Leave blank to use each track's Shazam-detected value.")

        # Genre prefix checkboxes
        st.markdown('<div class="sub-label">Genre prefix</div>', unsafe_allow_html=True)
        cp1, cp2, cp3, cp4 = st.columns([2, 2, 2, 3])
        with cp1:
            pfx_russian = st.checkbox("Russian", key="pfx_russian")
        with cp2:
            pfx_latin = st.checkbox("Latin", key="pfx_latin")
        with cp3:
            pfx_intl = st.checkbox("International", key="pfx_intl")

        # Build prefix string — only one should be ticked but handle multiples gracefully
        genre_prefixes = []
        if pfx_russian:    genre_prefixes.append("Russian")
        if pfx_latin:      genre_prefixes.append("Latin")
        if pfx_intl:       genre_prefixes.append("International")
        genre_prefix = " ".join(genre_prefixes)

        # Global overrides
        st.markdown('<div class="sub-label" style="margin-top:1rem">Global overrides</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            global_year = st.text_input("Year — all tracks", value="", placeholder="e.g. 1994", key="global_year")
        with col2:
            global_genre = st.text_input("Genre — all tracks", value="", placeholder="e.g. Hip-Hop", key="global_genre")

        # Per-track overrides (only when >1 identified track)
        per_track = {}
        if len(found) > 1:
            st.markdown('<div class="sub-label" style="margin-top:1.2rem">Per-track overrides</div>', unsafe_allow_html=True)
            for name in found:
                m = results[name]["meta"]
                with st.container():
                    st.markdown('<div class="per-track-row">', unsafe_allow_html=True)
                    pa, pb, pc, pd = st.columns([2, 5, 3, 3])
                    with pa:
                        if m.get("cover_url"):
                            st.image(m["cover_url"], width=40)
                    with pb:
                        st.markdown('<div class="track-title" style="font-size:0.82rem">' + m["title"] + '</div>', unsafe_allow_html=True)
                        st.markdown('<div class="track-artist">' + m["artist"] + '</div>', unsafe_allow_html=True)
                    slug = name.replace(" ","_").replace(".","_")
                    with pc:
                        py = st.text_input("Year", value="", placeholder=m["year"] or "—", key=f"py_{slug}", label_visibility="visible")
                    with pd:
                        pg = st.text_input("Genre", value="", placeholder=m.get("shazam_genre","") or "—", key=f"pg_{slug}", label_visibility="visible")
                    st.markdown('</div>', unsafe_allow_html=True)
                per_track[name] = {"year": py.strip(), "genre": pg.strip()}

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        _, col_tag, _ = st.columns([2, 3, 2])
        with col_tag:
            do_tag = st.button("⬇  Tag & Download All", type="primary", use_container_width=True)

        if do_tag:
            tagged_files = []
            prog2 = st.progress(0, text="Tagging…")
            for i, name in enumerate(found):
                prog2.progress(i / len(found), text=f"Tagging {name}…")
                r    = results[name]
                meta = r["meta"]
                pt   = per_track.get(name, {})
                year_str  = pt.get("year","")  or global_year.strip()  or meta["year"]
                base_genre = pt.get("genre","") or global_genre.strip() or meta.get("shazam_genre","")
                genre_str  = (genre_prefix + " " + base_genre).strip() if genre_prefix else base_genre
                year_val  = int(year_str) if year_str.isdigit() and len(year_str)==4 else None
                tagged_bytes, err = tag_file(r["file_bytes"], meta, year_val, genre_str)
                if err:
                    st.warning(f"Could not tag **{name}**: {err}")
                else:
                    tagged_files.append((safe_name(meta["safe_base"]) + ".mp3", tagged_bytes))
            prog2.progress(1.0, text="All done!")
            if tagged_files:
                st.session_state["tagged_files"] = tagged_files

        # ── Download section — persists after any button click ──
        if st.session_state.get("tagged_files"):
            tagged_files = st.session_state["tagged_files"]
            st.markdown('<div class="section-label" style="margin-top:1.5rem">05 — Download</div>', unsafe_allow_html=True)

            # Zip download (only shown when >1 file)
            if len(tagged_files) > 1:
                zip_buf = io.BytesIO()
                with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                    for out_name, tagged_bytes in tagged_files:
                        zf.writestr(out_name, tagged_bytes)
                zip_buf.seek(0)
                _, col_zip, _ = st.columns([2, 3, 2])
                with col_zip:
                    st.download_button(
                        label="⬇  Download All as ZIP",
                        data=zip_buf.getvalue(),
                        file_name="songtag_export.zip",
                        mime="application/zip",
                        key="dl_zip",
                        type="primary",
                        use_container_width=True,
                    )
                st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

            # Individual file downloads
            for out_name, tagged_bytes in tagged_files:
                _, col_dl, _ = st.columns([2, 3, 2])
                with col_dl:
                    st.download_button(
                        label=f"⬇  {out_name}",
                        data=tagged_bytes,
                        file_name=out_name,
                        mime="audio/mpeg",
                        key=f"dl_{out_name}",
                        use_container_width=True,
                    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:4rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.06);
     display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem">
  <span style="font-size:0.72rem;color:rgba(255,255,255,0.2);font-family:'DM Mono',monospace">
    SongTag · 100% local · SongRec + eyeD3
  </span>
  <span style="font-size:0.72rem;color:rgba(167,139,250,0.4);font-family:'DM Mono',monospace">
    ♫ identify · tag · export
  </span>
</div>
""", unsafe_allow_html=True)
