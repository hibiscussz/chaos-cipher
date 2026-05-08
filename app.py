# -*- coding: utf-8 -*-
"""
Streamlit UI — Chaos TSL Image Cipher
Theme: Pastel Sky Blue & Warm White on Dark Blue-Gray
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math, time, io
from PIL import Image

st.set_page_config(
    page_title="Chaos TSL Cipher",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&family=DM+Mono:wght@300;400;500&family=Sora:wght@300;400;600;700&display=swap');

:root {
    --bg:       #f0f6ff;
    --bg2:      #e8f1fb;
    --bg3:      #ddeaf8;
    --bg4:      #d0e1f5;
    --bg5:      #c2d7f0;
    --sky:      #2a6fa8;
    --sky2:     #1d5a8e;
    --sky3:     #3a80bb;
    --cream:    #2d2a26;
    --cream2:   #3a3630;
    --mint:     #1a7a5e;
    --rose:     #c0284a;
    --lavender: #5a3ea0;
    --border:   rgba(42,111,168,0.22);
    --border2:  rgba(42,111,168,0.10);
    --text:     #1a2e42;
    --muted:    #3a6080;
    --dimmer:   #7090aa;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[class*="css"],
.stApp, .main, .block-container,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
}

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
input[type="number"], input[type="text"], input {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--sky2) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
}
input:focus {
    border-color: var(--sky) !important;
    box-shadow: 0 0 0 3px rgba(42,111,168,0.12) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] button {
    background: var(--bg4) !important;
    border: 1px solid var(--border) !important;
    color: var(--sky) !important;
    border-radius: 6px !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(168,216,240,0.12) !important;
}

/* ── LABELS ── */
label, [data-testid="stWidgetLabel"], p {
    color: var(--muted) !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── FILE UPLOADER ── */
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
    border: 1.5px dashed rgba(42,111,168,0.35) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] button {
    background: var(--bg4) !important;
    border: 1px solid var(--border) !important;
    color: var(--sky) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 6px !important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: var(--muted) !important;
}
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] > div {
    background: var(--bg4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploaderFileName"] {
    color: var(--cream) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}
[data-testid="stFileUploaderFileData"] { color: var(--muted) !important; }
[data-testid="stFileUploaderDeleteBtn"] button {
    background: transparent !important;
    border: none !important;
    color: var(--muted) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(42,111,168,0.10) !important;
    border: 1.5px solid rgba(42,111,168,0.45) !important;
    color: var(--sky2) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    padding: 0.55rem 1.2rem !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(42,111,168,0.18) !important;
    border-color: var(--sky) !important;
    box-shadow: 0 4px 20px rgba(42,111,168,0.18) !important;
    color: var(--sky2) !important;
}

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
    background: rgba(26,122,94,0.09) !important;
    border: 1.5px solid rgba(26,122,94,0.40) !important;
    color: var(--mint) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    border-radius: 8px !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(26,122,94,0.16) !important;
    box-shadow: 0 4px 16px rgba(26,122,94,0.18) !important;
}

/* ── IMAGES ── */
[data-testid="stImage"] img {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--sky) !important; }
[data-testid="stSpinner"] p { color: var(--muted) !important; }

/* ── DIVIDER ── */
hr { border-color: var(--border2) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg5); border-radius: 2px; }

/* ── TOOLTIP ── */
[data-testid="stTooltipHoverTarget"] { color: var(--dimmer) !important; }
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
                facecolor='#f0f6ff', edgecolor='none')
    buf.seek(0); return buf

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div style="
    padding: 2rem 2.4rem 1.8rem;
    background: linear-gradient(135deg, #ddeaf8 0%, #e8f1fb 50%, #d8eaf8 100%);
    border: 1px solid rgba(42,111,168,0.25);
    border-radius: 14px;
    margin-bottom: 1.6rem;
    position: relative; overflow: hidden;
">
    <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,transparent,#2a6fa8 40%,#5a3ea0 70%,transparent);"></div>
    <div style="position:absolute;bottom:0;right:0;width:300px;height:300px;
                background:radial-gradient(circle,rgba(42,111,168,0.06) 0%,transparent 70%);
                pointer-events:none;"></div>
    <div style="display:flex;align-items:center;gap:1.2rem;">
        <div style="
            width:52px;height:52px;border-radius:12px;
            background:rgba(42,111,168,0.12);
            border:1px solid rgba(42,111,168,0.30);
            display:flex;align-items:center;justify-content:center;
            font-size:1.5rem; color:#1d5a8e;
        ">◈</div>
        <div>
            <div style="font-family:'Sora',sans-serif;font-size:1.6rem;font-weight:700;
                        color:#1a2e42;letter-spacing:1px;line-height:1.1;">
                Chaos TSL Cipher
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.68rem;
                        color:#2a6fa8;letter-spacing:2px;margin-top:4px;opacity:0.85;">
                Logistic → Sine → Tent  ·  Image Encryption System
            </div>
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
        <div style="font-family:'Sora',sans-serif;font-size:0.95rem;font-weight:600;
                    color:#1d5a8e;letter-spacing:1px;">◈ Key Parameters</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.62rem;
                    color:#5a7a98;margin-top:3px;">cipher configuration</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.62rem;
                color:#5a7a98;letter-spacing:1.5px;margin-bottom:0.7rem;
                text-transform:uppercase;">Chaos Map</div>""", unsafe_allow_html=True)

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

    st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.62rem;
                color:#5a7a98;letter-spacing:1.5px;margin:1rem 0 0.7rem;
                text-transform:uppercase;">Diffusion</div>""", unsafe_allow_html=True)

    C0 = st.number_input("C₀  —  Diffusion Seed",
        min_value=0, max_value=255, value=125, step=1, format="%d")
    N0 = st.number_input("N₀  —  Warm-up Iterations",
        min_value=100, max_value=5000, value=1000, step=100, format="%d")

    st.markdown("---")

    # Key summary
    st.markdown(f"""
    <div style="background:rgba(42,111,168,0.07);
                border:1px solid rgba(42,111,168,0.20);
                border-radius:10px;padding:1rem 1.1rem;
                font-family:'DM Mono',monospace;">
        <div style="font-size:0.6rem;color:#5a7a98;letter-spacing:1.5px;
                    margin-bottom:0.7rem;text-transform:uppercase;">Active Key</div>
        <div style="font-size:0.73rem;line-height:2.1;color:#2a6fa8;">
            x₀ <span style="color:#1a2e42;">= {x0:.6f}</span><br>
            r &nbsp;<span style="color:#1a2e42;">= {r:.4f}</span><br>
            μ &nbsp;<span style="color:#1a2e42;">= {mu:.4f}</span><br>
            C₀ <span style="color:#1a2e42;">= {C0}</span>
            &nbsp;&nbsp;N₀ <span style="color:#1a2e42;">= {N0}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    chaos_ok = r >= 3.57 and mu >= 1.8 and 0.01 < x0 < 0.99
    ok_color  = "#1a7a5e" if chaos_ok else "#c0284a"
    ok_bg     = "rgba(26,122,94,0.08)" if chaos_ok else "rgba(192,40,74,0.08)"
    ok_border = "rgba(26,122,94,0.28)" if chaos_ok else "rgba(192,40,74,0.28)"
    ok_label  = "Chaos regime optimal" if chaos_ok else "Suboptimal — check r, μ"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.6rem;padding:0.6rem 0.9rem;
                background:{ok_bg};border:1px solid {ok_border};border-radius:8px;
                font-family:'DM Mono',monospace;font-size:0.68rem;">
        <div style="width:7px;height:7px;border-radius:50%;
                    background:{ok_color};box-shadow:0 0 6px {ok_color};flex-shrink:0;"></div>
        <span style="color:{ok_color};">{ok_label}</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
col_up, col_btn = st.columns([3, 1])

with col_up:
    st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                color:#5a7a98;letter-spacing:1.5px;margin-bottom:0.5rem;
                text-transform:uppercase;">Input Image</div>""", unsafe_allow_html=True)
    uploaded = st.file_uploader("img", type=["jpg","jpeg","png"], label_visibility="collapsed")

with col_btn:
    st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                color:#5a7a98;letter-spacing:1.5px;margin-bottom:0.5rem;
                text-transform:uppercase;">Execute</div>""", unsafe_allow_html=True)
    run_enc = st.button("◈  Encrypt", use_container_width=True)
    run_dec = st.button("◇  Decrypt", use_container_width=True)

# ─────────────────────────────────────────
# PROCESS
# ─────────────────────────────────────────
if uploaded:
    img_pil = Image.open(uploaded).convert("RGB")
    plain = np.array(img_pil, dtype=np.uint8)
    M, N, ch = plain.shape

    st.markdown(f"""
    <div style="display:flex;gap:2rem;background:rgba(42,111,168,0.06);
                border:1px solid rgba(42,111,168,0.15);border-radius:8px;
                padding:0.6rem 1.2rem;font-family:'DM Mono',monospace;
                font-size:0.72rem;color:#5a7a98;margin-bottom:0.5rem;">
        <span>shape <span style="color:#1d5a8e;">{M}×{N}×{ch}</span></span>
        <span>pixels <span style="color:#1d5a8e;">{M*N:,}</span></span>
        <span>bytes <span style="color:#1d5a8e;">{M*N*ch:,}</span></span>
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

        st.markdown(f"""
        <div style="background:rgba(26,122,94,0.08);border:1px solid rgba(26,122,94,0.30);
                    border-radius:8px;padding:0.65rem 1.2rem;margin-bottom:0.5rem;
                    font-family:'DM Mono',monospace;font-size:0.75rem;color:#1a7a5e;">
            ✓ &nbsp; Encryption: {t_enc:.3f}s &nbsp;·&nbsp; Decryption: {t_dec:.3f}s
        </div>""", unsafe_allow_html=True)

        # Images
        st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#5a7a98;letter-spacing:1.5px;margin:1.2rem 0 0.6rem;
                    text-transform:uppercase;">Visual Output</div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        for col, img, lbl, clr in [
            (c1, plain,     "Plaintext",  "#3a6080"),
            (c2, cipher,    "Ciphertext", "#2a6fa8"),
            (c3, decrypted, "Decrypted",  "#1a7a5e"),
        ]:
            with col:
                st.markdown(f"""<div style="font-family:'DM Mono',monospace;font-size:0.68rem;
                            color:{clr};letter-spacing:1px;margin-bottom:5px;">{lbl}</div>""",
                            unsafe_allow_html=True)
                st.image(img, use_container_width=True)

        buf_c = io.BytesIO()
        Image.fromarray(cipher).save(buf_c, format='PNG')
        st.download_button("↓  Download Cipher Image", data=buf_c.getvalue(),
                           file_name="cipher_tsl.png", mime="image/png")

        # Metrics
        ent_c = hitung_entropi(cipher)
        mse_v, psnr_v = hitung_mse_psnr(plain, cipher)
        corr_p = hitung_korelasi(plain)
        corr_c = hitung_korelasi(cipher)
        pm = plain.copy(); pm[0,0,0] ^= 1
        cm, _ = encrypt(pm, x0, r, mu, C0, N0)
        npcr, uaci = hitung_npcr_uaci(cipher, cm)

        st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#5a7a98;letter-spacing:1.5px;margin:1.5rem 0 0.8rem;
                    text-transform:uppercase;">Security Analysis</div>""", unsafe_allow_html=True)

        def mcard(col, label, val, sub, ok):
            c  = "#1a7a5e" if ok else "#c0284a"
            bg = "rgba(26,122,94,0.07)" if ok else "rgba(192,40,74,0.07)"
            bd = "rgba(26,122,94,0.22)" if ok else "rgba(192,40,74,0.22)"
            col.markdown(f"""
            <div style="background:var(--bg3,#ddeaf8);border:1px solid {bd};
                        border-top:2px solid {c};border-radius:10px;
                        padding:1rem 0.9rem 0.85rem;text-align:center;">
                <div style="font-family:'DM Mono',monospace;font-size:0.6rem;
                            color:#5a7a98;letter-spacing:1px;text-transform:uppercase;
                            margin-bottom:0.3rem;">{label}</div>
                <div style="font-family:'Sora',sans-serif;font-size:1.55rem;font-weight:700;
                            color:{c};margin:0.1rem 0;">{val}</div>
                <div style="font-family:'DM Mono',monospace;font-size:0.6rem;
                            color:{c};opacity:0.7;">{sub}</div>
            </div>""", unsafe_allow_html=True)

        m1,m2,m3,m4,m5 = st.columns(5)
        mcard(m1, "Entropy", f"{ent_c:.4f}", "target > 7.9",   ent_c > 7.9)
        mcard(m2, "PSNR",    f"{psnr_v:.2f}","dB · < 10",      psnr_v < 10)
        mcard(m3, "MSE",     f"{mse_v:.0f}", "target > 5000",  mse_v > 5000)
        mcard(m4, "NPCR",    f"{npcr:.3f}%", "target > 99.6%", npcr > 99.6)
        mcard(m5, "UACI",    f"{uaci:.3f}%", "≈ 33.46%",       30 < uaci < 36)

        # Correlation
        st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#5a7a98;letter-spacing:1.5px;margin:1.5rem 0 0.7rem;
                    text-transform:uppercase;">Pixel Correlation</div>""", unsafe_allow_html=True)

        ct1, ct2 = st.columns(2)
        def corr_tbl(col, title, corrs, color):
            rows = ""
            for nm, v in zip(["Horizontal","Vertikal","Diagonal"], corrs):
                ok = abs(v) < 0.05
                ic = "#1a7a5e" if ok else "#c0284a"
                rows += f"""<tr>
                    <td style="padding:0.4rem 0.9rem;color:#5a7a98;font-size:0.7rem;">{nm}</td>
                    <td style="padding:0.4rem 0.9rem;font-family:'DM Mono',monospace;
                               color:{color};font-size:0.78rem;">{v:+.4f}</td>
                    <td style="padding:0.4rem 0.9rem;color:{ic};font-size:0.72rem;">
                        {'✓' if ok else '✗'}</td></tr>"""
            col.markdown(f"""
            <div style="background:#ddeaf8;border:1px solid rgba(42,111,168,0.15);
                        border-radius:10px;overflow:hidden;">
                <div style="padding:0.65rem 1rem;border-bottom:1px solid rgba(42,111,168,0.10);
                            font-family:'DM Mono',monospace;font-size:0.65rem;
                            color:{color};letter-spacing:1px;">{title}</div>
                <table style="width:100%;border-collapse:collapse;">{rows}</table>
            </div>""", unsafe_allow_html=True)

        corr_tbl(ct1, "Plaintext",           corr_p, "#3a6080")
        corr_tbl(ct2, "Ciphertext  (ideal ≈ 0)", corr_c, "#2a6fa8")

        # Histograms
        st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#5a7a98;letter-spacing:1.5px;margin:1.5rem 0 0.6rem;
                    text-transform:uppercase;">Histograms</div>""", unsafe_allow_html=True)

        plt.style.use('default')
        fig_h, axes = plt.subplots(1, 2, figsize=(13, 3.8))
        fig_h.patch.set_facecolor('#f0f6ff')
        clrs = ('#c0284a', '#2a6fa8', '#1a7a5e')
        for ax in axes:
            ax.set_facecolor('#e8f1fb')
            for sp in ax.spines.values(): sp.set_color('#c2d7f0')
            ax.tick_params(colors='#3a6080', labelsize=8)
            ax.grid(axis='y', color='#ddeaf8', linewidth=0.6)
        for i,(c,l) in enumerate(zip(clrs,('R','G','B'))):
            h,_ = np.histogram(plain[:,:,i].ravel(), 256, [0,256])
            axes[0].plot(h, color=c, alpha=0.75, label=l, linewidth=1.1)
        axes[0].set_title("Plaintext", color='#3a6080', fontsize=9, pad=8)
        axes[0].legend(labelcolor='#1a2e42', fontsize=8)
        for i,(c,l) in enumerate(zip(clrs,('R','G','B'))):
            h,_ = np.histogram(cipher[:,:,i].ravel(), 256, [0,256])
            axes[1].plot(h, color=c, alpha=0.75, label=l, linewidth=1.1)
        axes[1].set_title("Ciphertext  [ uniform = secure ]", color='#2a6fa8', fontsize=9, pad=8)
        axes[1].legend(labelcolor='#1a2e42', fontsize=8)
        plt.tight_layout(pad=1.5)
        st.image(fig_bytes(fig_h), use_container_width=True)
        plt.close(fig_h)

        # Scatter
        st.markdown("""<div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#5a7a98;letter-spacing:1.5px;margin:1rem 0 0.6rem;
                    text-transform:uppercase;">Correlation Scatter</div>""", unsafe_allow_html=True)

        rng = np.random.default_rng(42)
        xi  = rng.integers(0, M-1, 2000); yi = rng.integers(0, N-1, 2000)
        gp  = plain[:,:,0].astype(np.float64); gc = cipher[:,:,0].astype(np.float64)
        fig_s, axs = plt.subplots(3, 2, figsize=(10, 9))
        fig_s.patch.set_facecolor('#f0f6ff')
        dirs = [
            ("Horizontal", gp[xi,yi], gp[xi,yi+1], gc[xi,yi], gc[xi,yi+1]),
            ("Vertical",   gp[xi,yi], gp[xi+1,yi], gc[xi,yi], gc[xi+1,yi]),
            ("Diagonal",   gp[xi,yi], gp[xi+1,yi+1], gc[xi,yi], gc[xi+1,yi+1]),
        ]
        for i,(nm,px,py,cx,cy) in enumerate(dirs):
            for ax in axs[i]:
                ax.set_facecolor('#e8f1fb')
                for sp in ax.spines.values(): sp.set_color('#c2d7f0')
                ax.tick_params(colors='#3a6080', labelsize=7)
            axs[i,0].scatter(px, py, s=1.2, alpha=0.3, color='#3a6080')
            axs[i,0].set_title(f"Plain — {nm}  r={corr_p[i]:.4f}", color='#3a6080', fontsize=8)
            axs[i,1].scatter(cx, cy, s=1.2, alpha=0.3, color='#2a6fa8')
            axs[i,1].set_title(f"Cipher — {nm}  r={corr_c[i]:.4f}", color='#2a6fa8', fontsize=8)
        plt.tight_layout(pad=1.5)
        st.image(fig_bytes(fig_s), use_container_width=True)
        plt.close(fig_s)

        buf_d = io.BytesIO()
        Image.fromarray(decrypted).save(buf_d, format='PNG')
        st.download_button("↓  Download Decrypted Image", data=buf_d.getvalue(),
                           file_name="decrypted_tsl.png", mime="image/png")

    elif run_dec:
        with st.spinner("Decrypting..."):
            t0 = time.perf_counter()
            result = decrypt(plain, x0, r, mu, C0, N0)
            t_dec = time.perf_counter() - t0
        st.markdown(f"""
        <div style="background:rgba(26,122,94,0.08);border:1px solid rgba(26,122,94,0.30);
                    border-radius:8px;padding:0.65rem 1.2rem;margin-bottom:0.5rem;
                    font-family:'DM Mono',monospace;font-size:0.75rem;color:#1a7a5e;">
            ✓ &nbsp; Decryption complete: {t_dec:.3f}s
        </div>""", unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        d1.image(plain,  caption="Input (Cipher)", use_container_width=True)
        d2.image(result, caption="Decrypted",      use_container_width=True)
        buf_d2 = io.BytesIO()
        Image.fromarray(result).save(buf_d2, format='PNG')
        st.download_button("↓  Download Result", data=buf_d2.getvalue(),
                           file_name="decrypted_tsl.png", mime="image/png")

else:
    st.markdown("""
    <div style="margin-top:0.8rem;padding:2.4rem;background:#e8f1fb;
                border:1px solid rgba(42,111,168,0.15);border-radius:14px;text-align:center;">
        <div style="font-size:2rem;opacity:0.35;margin-bottom:0.8rem;color:#2a6fa8;">◈</div>
        <div style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:600;
                    color:#3a6080;letter-spacing:1px;">Upload an image to begin</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.67rem;
                    color:#7090aa;margin-top:0.4rem;">
            JPG & PNG supported  ·  configure key parameters in sidebar</div>
    </div>

    <div style="margin-top:1rem;display:grid;grid-template-columns:repeat(3,1fr);gap:0.9rem;">
        <div style="padding:1.2rem;background:#e8f1fb;
                    border:1px solid rgba(42,111,168,0.12);border-radius:11px;">
            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#7090aa;
                        letter-spacing:1.5px;margin-bottom:0.5rem;text-transform:uppercase;">
                Logistic Map</div>
            <div style="font-size:0.83rem;color:#2a6fa8;line-height:1.5;">
                r·x·(1−x) — generates chaotic pseudo-random sequence</div>
        </div>
        <div style="padding:1.2rem;background:#e8f1fb;
                    border:1px solid rgba(42,111,168,0.12);border-radius:11px;">
            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#7090aa;
                        letter-spacing:1.5px;margin-bottom:0.5rem;text-transform:uppercase;">
                Sine Map</div>
            <div style="font-size:0.83rem;color:#2a6fa8;line-height:1.5;">
                sin(π·x) — amplifies nonlinearity & unpredictability</div>
        </div>
        <div style="padding:1.2rem;background:#e8f1fb;
                    border:1px solid rgba(42,111,168,0.12);border-radius:11px;">
            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#7090aa;
                        letter-spacing:1.5px;margin-bottom:0.5rem;text-transform:uppercase;">
                Tent Map</div>
            <div style="font-size:0.83rem;color:#2a6fa8;line-height:1.5;">
                μ·min(x, 1−x) — uniform distribution enhancement</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
