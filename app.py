"""VoxGuard — Professional Streamlit interface for voice cloning and deepfake detection."""

import tempfile
from pathlib import Path

import streamlit as st

from src.detector import DeepfakeDetector
from src.generator import VoiceGenerator

# ── Must be the very first Streamlit call ────────────────────────────────────
st.set_page_config(
    page_title="VoxGuard — Clonage Vocal & Détection de Deepfakes",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
for key, val in {"logged_in": False, "user_email": "", "user_name": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Model loaders ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_generator():
    return VoiceGenerator()

@st.cache_resource(show_spinner=False)
def load_detector():
    return DeepfakeDetector()

def save_upload(f, suffix=".wav"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(f.read())
        return tmp.name

# ── Auth dialogs ──────────────────────────────────────────────────────────────
@st.dialog("Se connecter")
def login_dialog():
    st.markdown('<p style="color:#64748B;font-size:14px;margin-bottom:24px">Connectez-vous pour accéder à toutes les fonctionnalités de VoxGuard.</p>', unsafe_allow_html=True)
    email = st.text_input("Adresse e-mail", placeholder="vous@exemple.com")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Se connecter", type="primary", use_container_width=True):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.user_name = email.split("@")[0].capitalize()
            st.rerun()
        else:
            st.error("Veuillez remplir tous les champs.")
    st.markdown('<p style="text-align:center;font-size:12.5px;color:#94A3B8;margin-top:16px">Pas encore de compte ? <a href="#" style="color:#2563EB;text-decoration:none">Créer un compte</a></p>', unsafe_allow_html=True)

@st.dialog("Créer un compte")
def signup_dialog():
    st.markdown('<p style="color:#64748B;font-size:14px;margin-bottom:24px">Créez votre compte VoxGuard gratuitement.</p>', unsafe_allow_html=True)
    name = st.text_input("Nom complet", placeholder="Votre nom")
    email = st.text_input("Adresse e-mail", placeholder="vous@exemple.com")
    password = st.text_input("Mot de passe", type="password", placeholder="8 caractères minimum")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Créer mon compte", type="primary", use_container_width=True):
        if name and email and password:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.user_name = name
            st.rerun()
        else:
            st.error("Veuillez remplir tous les champs.")
    st.markdown('<p style="text-align:center;font-size:12px;color:#94A3B8;margin-top:16px">En créant un compte, vous acceptez la Charte d\'Usage.</p>', unsafe_allow_html=True)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset Streamlit chrome ── */
#MainMenu, footer, [data-testid="stHeader"],
[data-testid="stDecoration"], [data-testid="stToolbar"],
.stDeployButton { display: none !important; }

/* ── Base ── */
html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background: #F8FAFF !important;
    color: #0F172A;
}
[data-testid="stAppViewContainer"] > section.main > div.block-container {
    padding: 0 !important; max-width: 100% !important;
}
[data-testid="stSidebar"] { display: none !important; }

/* ── Hero ── */
.vg-hero {
    background: linear-gradient(135deg, #0B1628 0%, #0F2755 55%, #0B1628 100%);
    padding: 76px 56px 68px; display: flex;
    justify-content: space-between; align-items: flex-start; gap: 56px;
}
.vg-hero-left { max-width: 600px; }
.vg-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(96,165,250,0.1); border: 1px solid rgba(96,165,250,0.2);
    color: #93C5FD; font-size: 11px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 5px 14px; border-radius: 999px; margin-bottom: 24px;
}
.vg-eyebrow-dot { width: 5px; height: 5px; border-radius: 50%; background: #60A5FA; flex-shrink: 0; }
.vg-hero h1 {
    font-size: 44px; font-weight: 800; color: #FFFFFF;
    line-height: 1.1; letter-spacing: -1.5px; margin: 0 0 20px;
}
.vg-hero h1 em { color: #60A5FA; font-style: normal; }
.vg-hero-desc {
    font-size: 16px; color: #94A3B8; line-height: 1.75; margin: 0 0 36px;
}
.vg-hero-checks { display: flex; flex-direction: column; gap: 12px; }
.vg-check-row { display: flex; align-items: center; gap: 12px; font-size: 14px; color: #CBD5E1; }
.vg-check-icon {
    width: 22px; height: 22px; border-radius: 50%; flex-shrink: 0;
    background: rgba(96,165,250,0.12); border: 1px solid rgba(96,165,250,0.25);
    display: flex; align-items: center; justify-content: center;
}
.vg-hero-right { display: flex; flex-direction: column; gap: 14px; flex-shrink: 0; min-width: 240px; padding-top: 10px; }
.vg-stat-card {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px; padding: 22px 26px;
}
.vg-stat-num { font-size: 30px; font-weight: 800; color: #fff; letter-spacing: -1px; }
.vg-stat-em { color: #60A5FA; }
.vg-stat-label { font-size: 12px; color: #475569; margin-top: 5px; line-height: 1.4; }

/* ── Section header ── */
.vg-section-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1.8px;
    text-transform: uppercase; color: #2563EB; margin-bottom: 8px;
}
.vg-section-title {
    font-size: 30px; font-weight: 800; color: #0F172A;
    letter-spacing: -0.8px; margin: 0 0 10px; line-height: 1.2;
}
.vg-section-sub {
    font-size: 15px; color: #64748B; line-height: 1.7; max-width: 520px; margin: 0;
}

/* ── Steps section ── */
.vg-steps-bg { background: #FFFFFF; padding: 72px 56px; }
.vg-steps-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 48px; }
.vg-step {
    background: #F8FAFF; border: 1px solid #E2E8F0;
    border-radius: 16px; padding: 28px 24px 32px;
    transition: box-shadow 0.2s, transform 0.2s;
}
.vg-step:hover { box-shadow: 0 8px 28px rgba(37,99,235,0.08); transform: translateY(-3px); }
.vg-step-n {
    width: 38px; height: 38px; border-radius: 11px;
    background: #EFF6FF; color: #2563EB;
    font-size: 16px; font-weight: 800;
    display: flex; align-items: center; justify-content: center; margin-bottom: 18px;
}
.vg-step h3 { font-size: 14px; font-weight: 700; color: #0F172A; margin: 0 0 8px; line-height: 1.35; }
.vg-step p  { font-size: 13px; color: #64748B; line-height: 1.65; margin: 0; }

/* ── Tool sections ── */
.vg-tools-bg { background: #F8FAFF; padding: 72px 56px; }
.vg-tool-card {
    background: #FFFFFF; border: 1px solid #E2E8F0;
    border-radius: 20px; padding: 36px 36px 40px;
    height: 100%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.vg-tool-chip {
    display: inline-block; font-size: 10px; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase;
    padding: 3px 11px; border-radius: 6px; margin-bottom: 14px;
}
.vg-chip-gen { background: #EFF6FF; color: #2563EB; }
.vg-chip-det { background: #F0FDF4; color: #16A34A; }
.vg-tool-card h2 {
    font-size: 21px; font-weight: 800; color: #0F172A;
    letter-spacing: -0.5px; margin: 0 0 6px;
}
.vg-tool-card .vg-tool-desc {
    font-size: 13.5px; color: #64748B; line-height: 1.65;
    margin: 0 0 24px; padding-bottom: 24px; border-bottom: 1px solid #F1F5F9;
}
.vg-field-label {
    font-size: 12px; font-weight: 600; color: #374151;
    letter-spacing: 0.3px; margin-bottom: 6px; display: block; margin-top: 18px;
}
.vg-tool-step-row { display: flex; gap: 10px; margin-bottom: 24px; }
.vg-tool-step-pill {
    font-size: 11.5px; font-weight: 600; color: #64748B;
    background: #F1F5F9; border-radius: 999px; padding: 4px 12px;
    display: inline-flex; align-items: center; gap: 5px;
}
.vg-tool-step-pill b { color: #2563EB; }
.vg-warn {
    background: #FFFBEB; border: 1px solid #FDE68A;
    border-radius: 10px; padding: 11px 16px;
    font-size: 12.5px; color: #92400E; line-height: 1.55; margin-bottom: 20px;
}
.vg-result-real {
    background: #F0FDF4; border: 1.5px solid #86EFAC;
    border-radius: 12px; padding: 18px 22px;
    display: flex; align-items: center; gap: 14px; margin-top: 16px;
}
.vg-result-fake {
    background: #FFF7ED; border: 1.5px solid #FED7AA;
    border-radius: 12px; padding: 18px 22px;
    display: flex; align-items: center; gap: 14px; margin-top: 16px;
}
.vg-tag-real { background:#16A34A; color:#fff; font-size:12px; font-weight:700; padding:4px 13px; border-radius:7px; white-space:nowrap; }
.vg-tag-fake { background:#EA580C; color:#fff; font-size:12px; font-weight:700; padding:4px 13px; border-radius:7px; white-space:nowrap; }
.vg-result-body { font-size:13.5px; color:#374151; line-height:1.5; }
.vg-result-body strong { color:#0F172A; font-weight:700; }

/* ── Ethics cards ── */
.vg-ethics-bg { background: #FFFFFF; padding: 72px 56px; }
.vg-ethics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 48px; }
.vg-ethics-card {
    background: #F8FAFF; border: 1px solid #E2E8F0;
    border-radius: 16px; padding: 30px 32px;
}
.vg-ethics-card h3 { font-size:15px; font-weight:700; color:#0F172A; margin:0 0 14px; }
.vg-ethics-card p, .vg-ethics-card li { font-size:13.5px; color:#475569; line-height:1.75; }
.vg-ethics-card ul { margin:0; padding-left:18px; }
.vg-ethics-card li { margin-bottom:7px; }

/* ── Footer ── */
.vg-footer {
    background: #0B1628; padding: 44px 56px;
    display: flex; justify-content: space-between; align-items: center; gap: 40px;
}
.vg-footer-logo { font-size: 17px; font-weight: 800; color: #fff; letter-spacing: -0.3px; }
.vg-footer-logo span { color: #60A5FA; }
.vg-footer-text { font-size: 12.5px; color: #334155; max-width: 420px; line-height: 1.65; }

/* ── Divider ── */
.vg-divider { height: 1px; background: #E2E8F0; margin: 0 56px; }

/* ── Header row overrides ── */
.vg-header-row {
    background: #0B1628;
    border-bottom: 1px solid #1E293B;
    padding: 0 56px;
}
.vg-header-row [data-testid="stColumns"] { gap: 0 !important; align-items: center !important; }
.vg-header-row [data-testid="stColumns"] > div { display: flex; align-items: center; }

/* ── Streamlit widget overrides ── */
.stTextArea textarea, .stTextInput input {
    border-radius: 10px !important;
    border: 1.5px solid #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    background: #F8FAFF !important;
    color: #0F172A !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
}
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #E2E8F0 !important;
    background: #F8FAFF !important;
    font-size: 14px !important;
}
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.1px !important;
    transition: all 0.15s !important;
}
.stButton > button[kind="primary"] {
    background: #2563EB !important;
    border: none !important; color: #fff !important;
    padding: 11px 28px !important;
}
.stButton > button[kind="primary"]:hover { background: #1D4ED8 !important; }
.stButton > button[kind="secondary"] {
    background: white !important; border: 1.5px solid #E2E8F0 !important;
    color: #374151 !important; padding: 10px 24px !important;
}
[data-testid="stFileUploaderDropzone"] {
    border-radius: 12px !important; border: 1.5px dashed #CBD5E1 !important;
    background: #F8FAFF !important;
}
[data-testid="stMetric"] {
    background: #F8FAFF !important; border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important; padding: 16px 20px !important;
}
[data-testid="stMetric"] label { color: #64748B !important; font-size: 12px !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #0F172A !important; font-weight: 700 !important; }
.stSlider > div { padding: 0 !important; }
.stSuccess > div, .stError > div, .stWarning > div, .stInfo > div {
    border-radius: 10px !important;
}
/* Dialog (modal) overrides */
[data-testid="stDialog"] h2 { font-family: 'Inter', sans-serif !important; font-weight: 800 !important; font-size: 22px !important; }
[data-testid="stDialogBody"] { font-family: 'Inter', sans-serif !important; }
/* Nav button overrides */
.vg-nav-btn .stButton > button {
    background: transparent !important;
    border: 1.5px solid #1E293B !important;
    color: #94A3B8 !important;
    padding: 7px 18px !important;
    font-size: 13px !important;
}
.vg-nav-btn .stButton > button:hover { border-color: #60A5FA !important; color: #60A5FA !important; }
.vg-nav-signup .stButton > button {
    background: #2563EB !important; border: none !important;
    color: #fff !important; padding: 8px 18px !important; font-size: 13px !important;
}
.vg-nav-signup .stButton > button:hover { background: #1D4ED8 !important; }
.vg-nav-user { font-size: 13px; font-weight: 600; color: #CBD5E1; }
</style>""", unsafe_allow_html=True)

# ── Header / Navbar ───────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="vg-header-row">', unsafe_allow_html=True)
    col_logo, col_nav, col_spacer, col_auth = st.columns([2, 4, 1, 2])

    with col_logo:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:9px;height:66px;">
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
                <rect width="26" height="26" rx="7" fill="#2563EB"/>
                <path d="M13 5v16M9 9v8M17 9v8M5 13h3.5M17.5 13H21"
                      stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            </svg>
            <span style="font-size:18px;font-weight:800;color:#fff;letter-spacing:-0.4px">
                Vox<span style="color:#60A5FA">Guard</span>
            </span>
        </div>""", unsafe_allow_html=True)

    with col_nav:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:32px;height:66px;">
            <span style="font-size:13.5px;font-weight:500;color:#94A3B8;cursor:pointer">Générateur</span>
            <span style="font-size:13.5px;font-weight:500;color:#94A3B8;cursor:pointer">Détecteur</span>
            <span style="font-size:13.5px;font-weight:500;color:#94A3B8;cursor:pointer">Comment ca marche</span>
            <span style="font-size:13.5px;font-weight:500;color:#94A3B8;cursor:pointer">Éthique</span>
        </div>""", unsafe_allow_html=True)

    with col_auth:
        st.markdown('<div style="display:flex;align-items:center;gap:10px;height:66px;justify-content:flex-end">', unsafe_allow_html=True)
        if st.session_state.logged_in:
            st.markdown(f'<span class="vg-nav-user">Bonjour, {st.session_state.user_name}</span>', unsafe_allow_html=True)
            if st.button("Déconnexion", key="logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = ""
                st.session_state.user_name = ""
                st.rerun()
        else:
            auth_l, auth_r = st.columns(2)
            with auth_l:
                st.markdown('<div class="vg-nav-btn">', unsafe_allow_html=True)
                if st.button("Se connecter", key="nav_login"):
                    login_dialog()
                st.markdown("</div>", unsafe_allow_html=True)
            with auth_r:
                st.markdown('<div class="vg-nav-signup">', unsafe_allow_html=True)
                if st.button("S'inscrire", key="nav_signup", type="primary"):
                    signup_dialog()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vg-hero">
    <div class="vg-hero-left">
        <div class="vg-eyebrow">
            <div class="vg-eyebrow-dot"></div>
            Projet pédagogique — IA générative audio
        </div>
        <h1>Clonez une voix.<br>Détectez un <em>deepfake</em>.</h1>
        <p class="vg-hero-desc">
            VoxGuard explore deux faces de l'IA générative audio : la synthèse vocale
            par clonage (XTTS-v2) et la détection de voix synthétiques par embeddings
            (WavLM). Un outil pédagogique conçu avec une approche éthique rigoureuse.
        </p>
        <div class="vg-hero-checks">
            <div class="vg-check-row">
                <div class="vg-check-icon">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M2 6l3 3 5-5" stroke="#60A5FA" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                Clonage vocal multilingue avec XTTS-v2 de Coqui
            </div>
            <div class="vg-check-row">
                <div class="vg-check-icon">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M2 6l3 3 5-5" stroke="#60A5FA" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                Détection par embeddings WavLM (Microsoft)
            </div>
            <div class="vg-check-row">
                <div class="vg-check-icon">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <path d="M2 6l3 3 5-5" stroke="#60A5FA" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                Charte d'usage éthique intégrée
            </div>
        </div>
    </div>
    <div class="vg-hero-right">
        <div class="vg-stat-card">
            <div class="vg-stat-num">XTTS<span class="vg-stat-em">-v2</span></div>
            <div class="vg-stat-label">Modèle de clonage vocal<br>multilingue (Coqui)</div>
        </div>
        <div class="vg-stat-card">
            <div class="vg-stat-num">Wav<span class="vg-stat-em">LM</span></div>
            <div class="vg-stat-label">Modèle de détection<br>par embeddings (Microsoft)</div>
        </div>
        <div class="vg-stat-card">
            <div class="vg-stat-num">6<span class="vg-stat-em">+</span></div>
            <div class="vg-stat-label">Langues supportées par<br>le générateur vocal</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="vg-steps-bg">
    <div class="vg-section-label">Mode d'emploi</div>
    <div class="vg-section-title">Comment utiliser VoxGuard</div>
    <p class="vg-section-sub">
        Quatre étapes simples pour générer ou analyser un audio. Les deux outils
        fonctionnent indépendamment.
    </p>
    <div class="vg-steps-grid">
        <div class="vg-step">
            <div class="vg-step-n">1</div>
            <h3>Enregistrez votre voix de référence</h3>
            <p>Préparez un extrait audio de 10 à 15 secondes, voix claire, pièce silencieuse. Formats acceptés : WAV, MP3.</p>
        </div>
        <div class="vg-step">
            <div class="vg-step-n">2</div>
            <h3>Choisissez votre outil</h3>
            <p>Utilisez le <strong>Générateur</strong> pour synthétiser un texte avec votre voix, ou le <strong>Détecteur</strong> pour analyser un audio existant.</p>
        </div>
        <div class="vg-step">
            <div class="vg-step-n">3</div>
            <h3>Importez vos fichiers et paramétrez</h3>
            <p>Déposez vos fichiers audio, saisissez le texte à synthétiser ou ajustez le seuil de détection selon vos besoins.</p>
        </div>
        <div class="vg-step">
            <div class="vg-step-n">4</div>
            <h3>Obtenez le résultat instantanément</h3>
            <p>Le générateur produit un fichier audio écoutable. Le détecteur retourne un verdict REAL ou DEEPFAKE avec un score de confiance.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="vg-divider"></div>', unsafe_allow_html=True)

# ── Tools section ─────────────────────────────────────────────────────────────
st.markdown('<div class="vg-tools-bg">', unsafe_allow_html=True)
st.markdown("""
    <div class="vg-section-label">Outils</div>
    <div class="vg-section-title">Générateur &amp; Détecteur</div>
    <p class="vg-section-sub" style="margin-bottom:40px">
        Les deux outils sont accessibles directement ci-dessous.
        Chaque traitement peut prendre 1 à 3 minutes sur CPU.
    </p>
""", unsafe_allow_html=True)

tool_l, tool_r = st.columns(2, gap="large")

# ── Generator card ────────────────────────────────────────────────────────────
with tool_l:
    st.markdown("""
    <div class="vg-tool-card">
        <span class="vg-tool-chip vg-chip-gen">Générateur vocal</span>
        <h2>Clonage de voix — XTTS-v2</h2>
        <p class="vg-tool-desc">
            Importez un extrait de votre voix comme référence, saisissez le texte
            que vous souhaitez synthétiser, et le modèle XTTS-v2 génère un audio
            avec votre timbre vocal.
        </p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="background:#fff;border:1px solid #E2E8F0;border-top:none;border-radius:0 0 20px 20px;padding:0 36px 36px">', unsafe_allow_html=True)

    st.markdown('<div class="vg-warn">Clonez uniquement votre propre voix ou une voix avec consentement explicite. Tout audio généré doit être identifié comme produit par IA.</div>', unsafe_allow_html=True)

    st.markdown('<span class="vg-field-label">Audio de référence (10–15 secondes recommandées)</span>', unsafe_allow_html=True)
    ref_file = st.file_uploader("Référence", type=["wav", "mp3"], key="gen_ref", label_visibility="collapsed")

    st.markdown('<span class="vg-field-label">Texte à synthétiser</span>', unsafe_allow_html=True)
    gen_text = st.text_area(
        "Texte",
        value="Bonjour, ceci est un exemple de clonage vocal généré par intelligence artificielle.",
        height=100,
        label_visibility="collapsed",
    )

    st.markdown('<span class="vg-field-label">Langue</span>', unsafe_allow_html=True)
    gen_lang = st.selectbox("Langue", ["fr", "en", "es", "de", "it", "pt"],
                            format_func=lambda x: {"fr":"Français","en":"Anglais","es":"Espagnol","de":"Allemand","it":"Italien","pt":"Portugais"}[x],
                            label_visibility="collapsed")

    if st.button("Générer l'audio", type="primary", use_container_width=True, key="gen_btn"):
        if ref_file is None:
            st.error("Importez un fichier audio de référence.")
        elif not gen_text.strip():
            st.error("Saisissez un texte à synthétiser.")
        else:
            ref_path = save_upload(ref_file, suffix="."+ref_file.name.split(".")[-1])
            output_path = "data/generated/voxguard_output.wav"
            generator = load_generator()
            with st.spinner("Génération en cours — modèle XTTS-v2 sur CPU..."):
                generator.clone_voice(ref_path, gen_text, output_path, language=gen_lang)
            st.success("Audio généré — contenu produit par intelligence artificielle.")
            st.audio(output_path)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Detector card ─────────────────────────────────────────────────────────────
with tool_r:
    st.markdown("""
    <div class="vg-tool-card">
        <span class="vg-tool-chip vg-chip-det">Détecteur deepfake</span>
        <h2>Analyse audio — WavLM</h2>
        <p class="vg-tool-desc">
            Comparez un audio de référence authentique à un audio à analyser.
            Le modèle WavLM extrait des embeddings vocaux et calcule leur similarité
            pour déterminer si les deux audios appartiennent au même locuteur.
        </p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="background:#fff;border:1px solid #E2E8F0;border-top:none;border-radius:0 0 20px 20px;padding:0 36px 36px">', unsafe_allow_html=True)

    det_ref_col, det_test_col = st.columns(2, gap="medium")
    with det_ref_col:
        st.markdown('<span class="vg-field-label">Référence (voix authentique)</span>', unsafe_allow_html=True)
        det_ref = st.file_uploader("Référence", type=["wav", "mp3"], key="det_ref", label_visibility="collapsed")
    with det_test_col:
        st.markdown('<span class="vg-field-label">Audio à analyser</span>', unsafe_allow_html=True)
        det_test = st.file_uploader("Test", type=["wav", "mp3"], key="det_test", label_visibility="collapsed")

    st.markdown('<span class="vg-field-label" style="display:block;margin-top:20px">Seuil de similarité — au-dessus : REAL, en dessous : DEEPFAKE</span>', unsafe_allow_html=True)
    threshold = st.slider("Seuil", 0.0, 1.0, 0.85, 0.01, label_visibility="collapsed")

    if st.button("Analyser l'audio", type="primary", use_container_width=True, key="det_btn"):
        if det_ref is None or det_test is None:
            st.error("Importez les deux fichiers audio.")
        else:
            ref_path  = save_upload(det_ref,  suffix="."+det_ref.name.split(".")[-1])
            test_path = save_upload(det_test, suffix="."+det_test.name.split(".")[-1])
            detector = load_detector()
            with st.spinner("Analyse en cours — extraction des embeddings WavLM..."):
                result = detector.predict(ref_path, test_path, threshold=threshold)

            if result["label"] == "REAL":
                st.markdown(f"""
                <div class="vg-result-real">
                    <span class="vg-tag-real">REAL</span>
                    <div class="vg-result-body">
                        Similarité : <strong>{result['similarity']:.4f}</strong> &nbsp;·&nbsp;
                        Confiance : <strong>{result['confidence']:.1%}</strong><br>
                        <span style="font-size:12px;color:#64748B">Les deux audios présentent des caractéristiques vocales similaires.</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="vg-result-fake">
                    <span class="vg-tag-fake">DEEPFAKE</span>
                    <div class="vg-result-body">
                        Similarité : <strong>{result['similarity']:.4f}</strong> &nbsp;·&nbsp;
                        Confiance : <strong>{result['confidence']:.1%}</strong><br>
                        <span style="font-size:12px;color:#64748B">Les signatures vocales diffèrent significativement.</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("Similarité", f"{result['similarity']:.4f}")
            m2.metric("Confiance", f"{result['confidence']:.1%}")
            m3.metric("Seuil appliqué", f"{result['threshold']:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # vg-tools-bg

# ── Ethics section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="vg-ethics-bg">
    <div class="vg-section-label">Éthique &amp; Usage responsable</div>
    <div class="vg-section-title">Notre approche éthique</div>
    <p class="vg-section-sub" style="margin-bottom:0">
        VoxGuard est un outil pédagogique. Son usage est encadré par une charte d'usage
        et un mémoire éthique détaillant risques, solutions et limites.
    </p>
    <div class="vg-ethics-grid">
        <div class="vg-ethics-card">
            <h3>Principes fondamentaux</h3>
            <ul>
                <li><strong>Consentement</strong> — aucune voix ne peut être clonée sans accord explicite de la personne concernée.</li>
                <li><strong>Transparence</strong> — tout audio généré par IA doit être identifié comme tel.</li>
                <li><strong>Traçabilité</strong> — conserver une trace de chaque génération (qui, quoi, pourquoi).</li>
                <li><strong>Finalité pédagogique</strong> — cet outil est réservé à la recherche et à l'enseignement.</li>
            </ul>
        </div>
        <div class="vg-ethics-card">
            <h3>Usages strictement interdits</h3>
            <ul>
                <li>Cloner la voix d'une personne sans son consentement.</li>
                <li>Usurper l'identité d'un tiers par audio synthétique.</li>
                <li>Diffuser un contenu généré sans mention de son origine artificielle.</li>
                <li>Contourner un système d'authentification vocale.</li>
                <li>Produire des contenus diffamatoires, trompeurs ou frauduleux.</li>
            </ul>
        </div>
        <div class="vg-ethics-card">
            <h3>Limites du détecteur</h3>
            <p>
                Ce détecteur compare deux audios par similarité d'embeddings. Il ne détecte
                pas un deepfake de façon absolue — il mesure si deux audios semblent provenir
                du même locuteur. Le seuil de 0.85 est empirique et peut nécessiter une
                calibration selon les conditions d'enregistrement (qualité du micro, format, codec).
            </p>
        </div>
        <div class="vg-ethics-card">
            <h3>Ressources du projet</h3>
            <p>
                La documentation complète est disponible dans les fichiers du projet :
            </p>
            <ul>
                <li><strong>Memoire_Ethique.md</strong> — analyse des risques, solutions et approche éthique du projet.</li>
                <li><strong>Charte_Usage.md</strong> — règles d'usage, usages autorisés et interdits, bonnes pratiques.</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vg-footer">
    <div class="vg-footer-logo">Vox<span>Guard</span></div>
    <p class="vg-footer-text">
        Projet pédagogique sur l'IA générative audio et ses enjeux éthiques.
        Usage strictement non commercial, encadré par la Charte d'Usage.
        Modèles : XTTS-v2 (Coqui CPML) · WavLM (Microsoft).
    </p>
    <span class="vg-footer-note">2026 — Usage éducatif uniquement</span>
</div>
""", unsafe_allow_html=True)
