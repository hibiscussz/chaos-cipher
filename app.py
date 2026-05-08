# -*- coding: utf-8 -*-
"""
Streamlit UI — Chaos TSL Image Cipher
Full Dark Tech — Zero Light Elements
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math, time, io
from PIL import Image

st.set_page_config(
    page_title="Chaos TSL Cipher",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# FULL DARK CSS — override SEMUA komponen Streamlit
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@300;400;600&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg:      #070c12;
    --bg2:     #0b1219;
    --bg3:     #0f1a24;
    --bg4:     #132030;
    --neon:    #00c8f0;
    --neon2:   #00e896;
    --red:     #ff4060;
    --border:  rgba(0,200,240,0.15);
    --dim:     #2a4a60;
    --text:    #b8d8ec;
    --muted:   #3a5a72;
}

/* ── GLOBAL ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[class*="css"],
.stApp,
.main,
.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── HIDE BRANDING ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] .block-container {
    background-color: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── NUMBER INPUT ── */
[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] > div > div {
    background: var(--bg3) !important;
    border-color: var(--border) !important;
}
input[type="number"],
input[type="text"],
input {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    color: var(--neon) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
}
input:focus {
    border-color: var(--neon) !important;
    box-shadow: 0 0 0 2px rgba(0,200,240,0.12) !important;
    outline: none !important;
}

/* stepper buttons +/- */
[data-testid="stNumberInput"] button {
    background: var(--bg4) !important;
    border: 1px solid var(--border) !important;
    color: var(--neon) !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(0,200,240,0.1) !important;
}

/* ── LABELS ── */
label,
[data-testid="stWidgetLabel"],
.stNumberInput label,
p { color: var(--muted) !important; }

/* ── FILE UPLOADER — full dark override ── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] section > div,
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzoneInstructions"] {
    background: var(--bg3) !important;
    border-color: var(--border) !important;
    color: var(--muted) !important;
}
[data-testid="stFileUploaderDropzone"] {
    border: 1px dashed var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] button {
    background: var(--bg4) !important;
    border: 1px solid var(--border) !important;
    color: var(--neon) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 4px !important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: var(--muted) !important;
}

/* uploaded file pill */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] > div {
    background: var(--bg4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
[data-testid="stFileUploaderFileName"] {
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}
[data-testid="stFileUploaderFileData"] {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
}
[data-testid="stFileUploaderDeleteBtn"] button {
    background: transparent !important;
    border: none !important;
    color: var(--muted) !important;
}

/* ── SUCCESS / INFO / WARNING boxes ── */
[data-testid="stAlert"],
.stAlert,
div[data-baseweb="notification"],
[class*="stSuccess"],
[class*="stInfo"],
[class*="stWarning"],
[class*="stError"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--neon2) !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span { color: var(--neon2) !important; }
[data-testid="stAlert"] svg { fill: var(--neon2) !important; }

/* ── MAIN BUTTONS ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--neon) !important;
    color: var(--neon) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(0,200,240,0.08) !important;
    box-shadow: 0 0 16px rgba(0,200,240,0.2) !important;
    color: #fff !important;
}

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    border: 1px solid var(--neon2) !important;
    color: var(--neon2) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    border-radius: 4px !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(0,232,150,0.08) !important;
    box-shadow: 0 0 12px rgba(0,232,150,0.18) !important;
}

/* ── IMAGES ── */
[data-testid="stImage"] img {
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: var(--neon) !important;
}
[data-testid="stSpinner"] p { color: var(--muted) !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(0,200,240,0.08) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--dim); border-radius: 2px; }

/* ── COLUMNS gap ── */
[data-testid="column"] { gap: 0 !important; }

/* ── Tooltip ── */
[data-testid="stTooltipHoverTarget"] { color: var(--dim) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────
def tsl_step(x, r, mu):
    l_x = r * x * (1 - x)
    s_x = np.sin(np.pi * l_x)
    return mu * s_x if s_x < 0.5 else mu * (1 - s_x)

def generate_tsl_sequence(x0, r, mu, length, warmup=1000):
    x = x0
    for _ in range(warmup): x = tsl_step(x, r, mu)
    seq = np.empty(length)
    for i in range(length):
        x = tsl_step(x, r, mu)
        seq[i] = x
    return seq

def encrypt(img_array, x0, r, mu, C0=125, N0=1000):
    M, N, ch = img_array.shape
    L = M * N * ch
    seq = generate_tsl_sequence(x0, r, mu, L, N0)
    perm_idx = np.argsort(seq)
    flat = img_array.flatten()
    shuffled = flat[perm_idx]
    K_seq = (np.floor(seq * 1e14) % 256).astype(np.uint8)
    cipher_fwd = np.empty(L, dtype=np.uint8)
    cipher_fwd[0] = (int(shuffled[0]) + C0) % 256 ^ K_seq[0]
    for i in range(1, L):
        cipher_fwd[i] = (int(shuffled[i]) + int(cipher_fwd[i-1])) % 256 ^ K_seq[i]
    cipher_flat = np.empty(L, dtype=np.uint8)
    cipher_flat[-1] = (int(cipher_fwd[-1]) + C0) % 256 ^ K_seq[-1]
    for i in range(L-2, -1, -1):
        cipher_flat[i] = (int(cipher_fwd[i]) + int(cipher_flat[i+1])) % 256 ^ K_seq[i]
    return cipher_flat.reshape(M, N, ch), K_seq

def decrypt(cipher_img, x0, r, mu, C0=125, N0=1000):
    M, N, ch = cipher_img.shape
    L = M * N * ch
    seq = generate_tsl_sequence(x0, r, mu, L, N0)
    perm_idx = np.argsort(seq)
    K_seq = (np.floor(seq * 1e14) % 256).astype(np.uint8)
    cipher_flat = cipher_img.flatten()
    cipher_fwd = np.empty(L, dtype=np.uint8)
    val = int(cipher_flat[-1]) ^ int(K_seq[-1])
    cipher_fwd[-1] = (val - C0) % 256
    for i in range(L-2, -1, -1):
        val = int(cipher_flat[i]) ^ int(K_seq[i])
        cipher_fwd[i] = (val - int(cipher_flat[i+1])) % 256
    shuffled = np.empty(L, dtype=np.uint8)
    val = int(cipher_fwd[0]) ^ int(K_seq[0])
    shuffled[0] = (val - C0) % 256
    for i in range(1, L):
        val = int(cipher_fwd[i]) ^ int(K_seq[i])
        shuffled[i] = (val - int(cipher_fwd[i-1])) % 256
    inv_perm = np.empty_like(perm_idx)
    inv_perm[perm_idx] = np.arange(L)
    return shuffled[inv_perm].reshape(M, N, ch)

def hitung_entropi(img):
    hist, _ = np.histogram(img.flatten(), bins=256, range=[0,256])
    hist = hist[hist > 0]; prob = hist / hist.sum()
    return float(-np.sum(prob * np.log2(prob)))

def hitung_mse_psnr(img1, img2):
    a, b = img1.astype(np.float64), img2.astype(np.float64)
    mse = np.mean((a - b) ** 2)
    if mse == 0: return 0.0, float('inf')
    return float(mse), float(20 * math.log10(255.0 / math.sqrt(mse)))

def hitung_korelasi(img, n=5000):
    M, N = img.shape[:2]
    rng = np.random.default_rng(42)
    xi = rng.integers(0, M-1, n); yi = rng.integers(0, N-1, n)
    g = img[:,:,0].astype(np.float64); x_val = g[xi, yi]
    corr = lambda a, b: float(np.corrcoef(a, b)[0,1])
    return corr(x_val, g[xi,yi+1]), corr(x_val, g[xi+1,yi]), corr(x_val, g[xi+1,yi+1])

def hitung_npcr_uaci(c1, c2):
    a, b = c1.astype(np.float64), c2.astype(np.float64)
    L = a.size
    return float((a!=b).sum()/L*100), float(np.abs(a-b).sum()/(255.0*L)*100)

def fig_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=130, bbox_inches='tight',
                facecolor='#070c12', edgecolor='none')
    buf.seek(0); return buf

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div style="padding:2rem 2.4rem 1.7rem;
            background:linear-gradient(135deg,#0b1219,#0a1520);
            border:1px solid rgba(0,200,240,0.18);border-radius:10px;
            margin-bottom:1.6rem;position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,transparent,#00c8f0 45%,#00e896 75%,transparent);"></div>
    <div style="display:flex;align-items:center;gap:1.1rem;">
        <div style="width:48px;height:48px;border-radius:8px;
                    background:rgba(0,200,240,0.08);border:1px solid rgba(0,200,240,0.25);
                    display:flex;align-items:center;justify-content:center;font-size:1.5rem;">⬡</div>
        <div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.65rem;font-weight:700;
                        color:#daeeff;letter-spacing:2.5px;">CHAOS TSL CIPHER</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                        color:#00c8f0;letter-spacing:3px;margin-top:2px;">
                LOGISTIC → SINE → TENT  //  IMAGE ENCRYPTION SYSTEM</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.4rem;">
        <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:700;
                    color:#00c8f0;letter-spacing:3px;">⬡ KEY PARAMETERS</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                    color:#2a4a60;margin-top:2px;letter-spacing:1px;">// cipher configuration</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                color:#2a4a60;letter-spacing:2px;margin-bottom:0.7rem;">[ CHAOS MAP PARAMS ]</div>""",
                unsafe_allow_html=True)

    x0 = st.number_input("x₀  —  Initial Condition",
        min_value=0.000001, max_value=0.999999, value=0.456789,
        step=0.000001, format="%.6f",
        help="Kondisi awal chaos. Kunci utama — ubah sedikit = cipher beda total.")
    r  = st.number_input("r  —  Logistic Rate",
        min_value=2.5, max_value=4.0, value=3.95,
        step=0.01, format="%.4f", help="r > 3.57 = chaos. Ideal mendekati 4.0")
    mu = st.number_input("μ  —  Tent Parameter",
        min_value=1.0, max_value=2.0, value=2.0,
        step=0.01, format="%.4f", help="μ = 2.0 = chaos penuh")

    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                color:#2a4a60;letter-spacing:2px;margin:1rem 0 0.7rem;">[ DIFFUSION PARAMS ]</div>""",
                unsafe_allow_html=True)

    C0 = st.number_input("C₀  —  Diffusion Seed",
        min_value=0, max_value=255, value=125, step=1, format="%d")
    N0 = st.number_input("N₀  —  Warm-up Iterations",
        min_value=100, max_value=5000, value=1000, step=100, format="%d")

    st.markdown("---")
    st.markdown(f"""
    <div style="background:rgba(0,200,240,0.04);border:1px solid rgba(0,200,240,0.15);
                border-radius:7px;padding:0.9rem 1rem;font-family:'JetBrains Mono',monospace;">
        <div style="font-size:0.6rem;color:#2a4a60;letter-spacing:2px;margin-bottom:0.6rem;">
            // ACTIVE KEY</div>
        <div style="font-size:0.73rem;line-height:2;color:#00c8f0;">
            x₀ <span style="color:#b8d8ec;">= {x0:.6f}</span><br>
            r &nbsp;<span style="color:#b8d8ec;">= {r:.4f}</span><br>
            μ &nbsp;<span style="color:#b8d8ec;">= {mu:.4f}</span><br>
            C₀ <span style="color:#b8d8ec;">= {C0}</span> &nbsp;&nbsp;
            N₀ <span style="color:#b8d8ec;">= {N0}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    chaos_ok = r >= 3.57 and mu >= 1.8 and 0.01 < x0 < 0.99
    c = "#00e896" if chaos_ok else "#ff4060"
    bg = f"rgba({'0,232,150' if chaos_ok else '255,64,96'},0.06)"
    bd = f"rgba({'0,232,150' if chaos_ok else '255,64,96'},0.22)"
    lbl = "CHAOS REGIME OPTIMAL" if chaos_ok else "SUBOPTIMAL — CHECK r, μ"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.5rem;padding:0.55rem 0.8rem;
                background:{bg};border:1px solid {bd};border-radius:5px;
                font-family:'JetBrains Mono',monospace;font-size:0.68rem;">
        <div style="width:7px;height:7px;border-radius:50%;background:{c};
                    box-shadow:0 0 5px {c};flex-shrink:0;"></div>
        <span style="color:{c};">{lbl}</span>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
col_up, col_btn = st.columns([3, 1])

with col_up:
    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                color:#2a4a60;letter-spacing:2px;margin-bottom:0.4rem;">// INPUT IMAGE</div>""",
                unsafe_allow_html=True)
    uploaded = st.file_uploader("img", type=["jpg","jpeg","png"], label_visibility="collapsed")

with col_btn:
    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                color:#2a4a60;letter-spacing:2px;margin-bottom:0.4rem;">// EXECUTE</div>""",
                unsafe_allow_html=True)
    run_enc = st.button("⬡  ENCRYPT", use_container_width=True)
    run_dec = st.button("◈  DECRYPT", use_container_width=True)

# ─────────────────────────────────────────
# PROCESS
# ─────────────────────────────────────────
if uploaded:
    img_pil = Image.open(uploaded).convert("RGB")
    plain = np.array(img_pil, dtype=np.uint8)
    M, N, ch = plain.shape

    st.markdown(f"""
    <div style="display:flex;gap:2rem;background:rgba(0,200,240,0.03);
                border:1px solid rgba(0,200,240,0.1);border-radius:5px;
                padding:0.6rem 1.1rem;font-family:'JetBrains Mono',monospace;
                font-size:0.72rem;color:#3a5a72;margin-bottom:0.4rem;">
        <span>SHAPE <span style="color:#00c8f0;">{M}×{N}×{ch}</span></span>
        <span>PIXELS <span style="color:#00c8f0;">{M*N:,}</span></span>
        <span>BYTES <span style="color:#00c8f0;">{M*N*ch:,}</span></span>
    </div>""", unsafe_allow_html=True)

    if run_enc:
        with st.spinner("Generating chaos sequence..."):
            t0 = time.perf_counter()
            cipher, K_seq = encrypt(plain, x0, r, mu, C0, N0)
            t_enc = time.perf_counter() - t0
        with st.spinner("Verifying decryption..."):
            t0 = time.perf_counter()
            decrypted = decrypt(cipher, x0, r, mu, C0, N0)
            t_dec = time.perf_counter() - t0

        # custom success — avoid light alert box
        st.markdown(f"""
        <div style="background:rgba(0,232,150,0.06);border:1px solid rgba(0,232,150,0.22);
                    border-radius:6px;padding:0.6rem 1.1rem;margin-bottom:0.5rem;
                    font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#00e896;">
            ✓ &nbsp;Encryption: {t_enc:.3f}s &nbsp;|&nbsp; Decryption: {t_dec:.3f}s
        </div>""", unsafe_allow_html=True)

        # Images
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#2a4a60;letter-spacing:2px;margin:1.1rem 0 0.5rem;">// VISUAL OUTPUT</div>""",
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        for col, img, lbl, clr in [
            (c1, plain,     "PLAINTEXT",  "#3a5a72"),
            (c2, cipher,    "CIPHERTEXT", "#00c8f0"),
            (c3, decrypted, "DECRYPTED",  "#00e896"),
        ]:
            with col:
                st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:0.68rem;"
                            f"color:{clr};letter-spacing:1px;margin-bottom:4px;'>{lbl}</div>",
                            unsafe_allow_html=True)
                st.image(img, use_container_width=True)

        buf_c = io.BytesIO()
        Image.fromarray(cipher).save(buf_c, format='PNG')
        st.download_button("↓  DOWNLOAD CIPHER IMAGE", data=buf_c.getvalue(),
                           file_name="cipher_tsl.png", mime="image/png")

        # ── Metrics ──
        ent_c = hitung_entropi(cipher)
        mse_v, psnr_v = hitung_mse_psnr(plain, cipher)
        corr_p = hitung_korelasi(plain)
        corr_c = hitung_korelasi(cipher)
        pm = plain.copy(); pm[0,0,0] ^= 1
        cm, _ = encrypt(pm, x0, r, mu, C0, N0)
        npcr, uaci = hitung_npcr_uaci(cipher, cm)

        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#2a4a60;letter-spacing:2px;margin:1.4rem 0 0.7rem;">// SECURITY ANALYSIS</div>""",
                    unsafe_allow_html=True)

        def mcard(col, label, val, sub, ok):
            c = "#00e896" if ok else "#ff4060"
            g = f"rgba({'0,232,150' if ok else '255,64,96'},0.12)"
            col.markdown(f"""
            <div style="background:#0f1a24;border:1px solid {c}28;border-top:2px solid {c};
                        border-radius:7px;padding:1rem 0.9rem 0.8rem;text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                            color:#2a4a60;letter-spacing:1.5px;text-transform:uppercase;">{label}</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.6rem;font-weight:700;
                            color:{c};margin:0.25rem 0 0.1rem;text-shadow:0 0 10px {g};">{val}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:{c}66;">{sub}</div>
            </div>""", unsafe_allow_html=True)

        m1,m2,m3,m4,m5 = st.columns(5)
        mcard(m1, "Entropy", f"{ent_c:.4f}", "> 7.9",       ent_c > 7.9)
        mcard(m2, "PSNR",    f"{psnr_v:.2f}","dB / < 10",   psnr_v < 10)
        mcard(m3, "MSE",     f"{mse_v:.0f}", "> 5000",       mse_v > 5000)
        mcard(m4, "NPCR",    f"{npcr:.3f}%", "> 99.6%",      npcr > 99.6)
        mcard(m5, "UACI",    f"{uaci:.3f}%", "≈ 33.46%",     30 < uaci < 36)

        # ── Correlation ──
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#2a4a60;letter-spacing:2px;margin:1.4rem 0 0.7rem;">// PIXEL CORRELATION</div>""",
                    unsafe_allow_html=True)
        ct1, ct2 = st.columns(2)

        def corr_tbl(col, title, corrs, color):
            rows = ""
            for nm, v in zip(["Horizontal","Vertikal","Diagonal"], corrs):
                ok = abs(v) < 0.05
                ic = "#00e896" if ok else "#ff4060"
                rows += f"""<tr>
                    <td style="padding:0.38rem 0.8rem;color:#3a5a72;font-size:0.7rem;">{nm}</td>
                    <td style="padding:0.38rem 0.8rem;font-family:'JetBrains Mono',monospace;
                               color:{color};font-size:0.78rem;">{v:+.4f}</td>
                    <td style="padding:0.38rem 0.8rem;color:{ic};font-size:0.72rem;">
                        {'✓' if ok else '✗'}</td></tr>"""
            col.markdown(f"""
            <div style="background:#0f1a24;border:1px solid rgba(0,200,240,0.1);border-radius:7px;overflow:hidden;">
                <div style="padding:0.6rem 0.9rem;border-bottom:1px solid rgba(0,200,240,0.08);
                            font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                            color:{color};letter-spacing:1px;">{title}</div>
                <table style="width:100%;border-collapse:collapse;">{rows}</table>
            </div>""", unsafe_allow_html=True)

        corr_tbl(ct1, "// PLAINTEXT",           corr_p, "#3a7a9a")
        corr_tbl(ct2, "// CIPHERTEXT  (≈ 0)", corr_c, "#00c8f0")

        # ── Histograms ──
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#2a4a60;letter-spacing:2px;margin:1.4rem 0 0.6rem;">// HISTOGRAMS</div>""",
                    unsafe_allow_html=True)
        plt.style.use('dark_background')
        fig_h, axes = plt.subplots(1, 2, figsize=(13, 3.8))
        fig_h.patch.set_facecolor('#070c12')
        for ax in axes:
            ax.set_facecolor('#0b1219')
            for sp in ax.spines.values(): sp.set_color('#132030')
            ax.tick_params(colors='#2a4a60', labelsize=8)
            ax.grid(axis='y', color='#0f1a24', linewidth=0.6)
        clrs = ('#ff4060','#00c8f0','#00e896')
        for i,(c,l) in enumerate(zip(clrs,('R','G','B'))):
            h,_ = np.histogram(plain[:,:,i].ravel(),256,[0,256])
            axes[0].plot(h, color=c, alpha=0.75, label=l, linewidth=1)
        axes[0].set_title("Plaintext",  color='#3a7a9a', fontsize=9, pad=8)
        axes[0].legend(labelcolor='#b8d8ec', fontsize=8)
        for i,(c,l) in enumerate(zip(clrs,('R','G','B'))):
            h,_ = np.histogram(cipher[:,:,i].ravel(),256,[0,256])
            axes[1].plot(h, color=c, alpha=0.75, label=l, linewidth=1)
        axes[1].set_title("Ciphertext  [ uniform = secure ]", color='#00c8f0', fontsize=9, pad=8)
        axes[1].legend(labelcolor='#b8d8ec', fontsize=8)
        plt.tight_layout(pad=1.5)
        st.image(fig_bytes(fig_h), use_container_width=True)
        plt.close(fig_h)

        # ── Scatter ──
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#2a4a60;letter-spacing:2px;margin:1rem 0 0.6rem;">// CORRELATION SCATTER</div>""",
                    unsafe_allow_html=True)
        rng = np.random.default_rng(42)
        xi = rng.integers(0, M-1, 2000); yi = rng.integers(0, N-1, 2000)
        gp = plain[:,:,0].astype(np.float64); gc = cipher[:,:,0].astype(np.float64)
        fig_s, axs = plt.subplots(3, 2, figsize=(10, 9))
        fig_s.patch.set_facecolor('#070c12')
        dirs = [
            ("Horizontal", gp[xi,yi], gp[xi,yi+1], gc[xi,yi], gc[xi,yi+1]),
            ("Vertical",   gp[xi,yi], gp[xi+1,yi], gc[xi,yi], gc[xi+1,yi]),
            ("Diagonal",   gp[xi,yi], gp[xi+1,yi+1], gc[xi,yi], gc[xi+1,yi+1]),
        ]
        for i,(nm,px,py,cx,cy) in enumerate(dirs):
            for ax in axs[i]:
                ax.set_facecolor('#0b1219')
                for sp in ax.spines.values(): sp.set_color('#132030')
                ax.tick_params(colors='#2a4a60', labelsize=7)
            axs[i,0].scatter(px, py, s=1.2, alpha=0.3, color='#3a7a9a')
            axs[i,0].set_title(f"Plain — {nm}  r={corr_p[i]:.4f}", color='#3a7a9a', fontsize=8)
            axs[i,1].scatter(cx, cy, s=1.2, alpha=0.3, color='#00c8f0')
            axs[i,1].set_title(f"Cipher — {nm}  r={corr_c[i]:.4f}", color='#00c8f0', fontsize=8)
        plt.tight_layout(pad=1.5)
        st.image(fig_bytes(fig_s), use_container_width=True)
        plt.close(fig_s)

        buf_d = io.BytesIO()
        Image.fromarray(decrypted).save(buf_d, format='PNG')
        st.download_button("↓  DOWNLOAD DECRYPTED IMAGE", data=buf_d.getvalue(),
                           file_name="decrypted_tsl.png", mime="image/png")

    elif run_dec:
        with st.spinner("Decrypting..."):
            t0 = time.perf_counter()
            result = decrypt(plain, x0, r, mu, C0, N0)
            t_dec = time.perf_counter() - t0
        st.markdown(f"""
        <div style="background:rgba(0,232,150,0.06);border:1px solid rgba(0,232,150,0.22);
                    border-radius:6px;padding:0.6rem 1.1rem;margin-bottom:0.5rem;
                    font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#00e896;">
            ✓ &nbsp;Decryption complete: {t_dec:.3f}s
        </div>""", unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        d1.image(plain,  caption="Input (Cipher)", use_container_width=True)
        d2.image(result, caption="Decrypted",      use_container_width=True)
        buf_d2 = io.BytesIO()
        Image.fromarray(result).save(buf_d2, format='PNG')
        st.download_button("↓  DOWNLOAD RESULT", data=buf_d2.getvalue(),
                           file_name="decrypted_tsl.png", mime="image/png")

else:
    st.markdown("""
    <div style="margin-top:0.8rem;padding:2.2rem;background:#0f1a24;
                border:1px solid rgba(0,200,240,0.08);border-radius:9px;text-align:center;">
        <div style="font-size:2rem;opacity:0.2;margin-bottom:0.8rem;">⬡</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600;
                    color:#3a5a72;letter-spacing:2px;">UPLOAD AN IMAGE TO BEGIN</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.67rem;
                    color:#2a4a60;margin-top:0.4rem;">
            // JPG & PNG supported  ·  set key parameters in sidebar</div>
    </div>
    <div style="margin-top:1rem;display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;">
        <div style="padding:1.1rem;background:#0f1a24;border:1px solid rgba(0,200,240,0.08);border-radius:7px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#2a4a60;letter-spacing:1.5px;margin-bottom:0.4rem;">// LOGISTIC MAP</div>
            <div style="font-size:0.82rem;color:#3a7a9a;">r·x·(1−x) — generates chaotic pseudo-random sequence</div>
        </div>
        <div style="padding:1.1rem;background:#0f1a24;border:1px solid rgba(0,200,240,0.08);border-radius:7px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#2a4a60;letter-spacing:1.5px;margin-bottom:0.4rem;">// SINE MAP</div>
            <div style="font-size:0.82rem;color:#3a7a9a;">sin(π·x) — amplifies nonlinearity & unpredictability</div>
        </div>
        <div style="padding:1.1rem;background:#0f1a24;border:1px solid rgba(0,200,240,0.08);border-radius:7px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#2a4a60;letter-spacing:1.5px;margin-bottom:0.4rem;">// TENT MAP</div>
            <div style="font-size:0.82rem;color:#3a7a9a;">μ·min(x, 1−x) — uniform distribution enhancement</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
