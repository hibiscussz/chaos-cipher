# -*- coding: utf-8 -*-
"""
Streamlit UI — Chaos TSL Image Cipher
Dark Tech Edition: Biru Neon & Abu Gelap
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math, time, io
from PIL import Image

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Chaos TSL Cipher",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS — DARK TECH
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@300;400;600&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg-base:    #080d14;
    --bg-panel:   #0d1520;
    --bg-card:    #111d2e;
    --bg-hover:   #162438;
    --neon:       #00d4ff;
    --neon-dim:   #0099bb;
    --neon-glow:  rgba(0,212,255,0.15);
    --neon2:      #00ff9d;
    --accent:     #ff4d6d;
    --border:     rgba(0,212,255,0.18);
    --border2:    rgba(0,212,255,0.08);
    --text-main:  #cde8f5;
    --text-dim:   #5a7a99;
    --text-bright:#e8f4ff;
}

html, body, [class*="css"] {
    background-color: var(--bg-base) !important;
    font-family: 'Outfit', sans-serif;
    color: var(--text-main);
}

#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon), transparent);
}

input[type="number"] {
    background: #0a1520 !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--neon) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.4rem 0.6rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input[type="number"]:focus {
    border-color: var(--neon) !important;
    box-shadow: 0 0 0 2px var(--neon-glow), 0 0 12px var(--neon-glow) !important;
    outline: none !important;
}

label, .stNumberInput label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: var(--text-dim) !important;
}

.stButton > button {
    width: 100%;
    background: transparent !important;
    border: 1px solid var(--neon) !important;
    color: var(--neon) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.2rem !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--neon-glow) !important;
    box-shadow: 0 0 20px var(--neon-glow), inset 0 0 20px var(--neon-glow) !important;
    color: #fff !important;
}

[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

[data-testid="stImage"] img {
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
}

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
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(0,255,157,0.1) !important;
    box-shadow: 0 0 12px rgba(0,255,157,0.2) !important;
}

hr { border-color: var(--border2) !important; margin: 1.2rem 0 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--neon-dim); border-radius: 2px; }
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
    hist = hist[hist > 0]
    prob = hist / hist.sum()
    return float(-np.sum(prob * np.log2(prob)))

def hitung_mse_psnr(img1, img2):
    a, b = img1.astype(np.float64), img2.astype(np.float64)
    mse = np.mean((a - b) ** 2)
    if mse == 0: return 0.0, float('inf')
    return float(mse), float(20 * math.log10(255.0 / math.sqrt(mse)))

def hitung_korelasi(img, n=5000):
    M, N = img.shape[:2]
    rng = np.random.default_rng(42)
    xi = rng.integers(0, M-1, n)
    yi = rng.integers(0, N-1, n)
    g = img[:,:,0].astype(np.float64)
    x_val = g[xi, yi]
    corr = lambda a, b: float(np.corrcoef(a, b)[0,1])
    return corr(x_val, g[xi, yi+1]), corr(x_val, g[xi+1, yi]), corr(x_val, g[xi+1, yi+1])

def hitung_npcr_uaci(c1, c2):
    a, b = c1.astype(np.float64), c2.astype(np.float64)
    L = a.size
    D = (a != b).astype(np.float64)
    return float(D.sum()/L*100), float(np.abs(a-b).sum()/(255.0*L)*100)

def fig_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=130, bbox_inches='tight',
                facecolor='#080d14', edgecolor='none')
    buf.seek(0)
    return buf

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div style="
    padding: 2.2rem 2.5rem 1.8rem;
    background: linear-gradient(135deg, #0d1520 0%, #091622 50%, #0d1a28 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 10px;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,transparent 0%,#00d4ff 40%,#00ff9d 70%,transparent 100%);"></div>
    <div style="display:flex; align-items:center; gap:1.2rem;">
        <div style="width:52px;height:52px;border-radius:8px;
                    background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);
                    display:flex;align-items:center;justify-content:center;font-size:1.6rem;">⬡</div>
        <div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.75rem;font-weight:700;
                        color:#e8f4ff;letter-spacing:2px;line-height:1.1;">
                CHAOS TSL CIPHER
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;
                        color:#00d4ff;letter-spacing:3px;margin-top:3px;">
                LOGISTIC → SINE → TENT  //  IMAGE ENCRYPTION SYSTEM
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
    <div style="padding:1.2rem 0 0.5rem;">
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#00d4ff;letter-spacing:3px;text-transform:uppercase;">⬡ Key Parameters</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#3a6080;letter-spacing:1px;margin-top:2px;">// cipher configuration</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                color:#3a6080;letter-spacing:2px;margin-bottom:0.8rem;">[ CHAOS MAP PARAMS ]</div>""",
                unsafe_allow_html=True)

    x0 = st.number_input("x₀  —  Initial Condition",
        min_value=0.000001, max_value=0.999999, value=0.456789,
        step=0.000001, format="%.6f",
        help="Kondisi awal chaos map. Kunci utama — beda sedikit = cipher beda total.")

    r = st.number_input("r  —  Logistic Rate",
        min_value=2.5, max_value=4.0, value=3.95,
        step=0.01, format="%.4f",
        help="r > 3.57 = chaos. Ideal: mendekati 4.0")

    mu = st.number_input("μ  —  Tent Parameter",
        min_value=1.0, max_value=2.0, value=2.0,
        step=0.01, format="%.4f",
        help="μ = 2.0 menghasilkan chaos penuh.")

    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                color:#3a6080;letter-spacing:2px;margin:1rem 0 0.8rem;">[ DIFFUSION PARAMS ]</div>""",
                unsafe_allow_html=True)

    C0 = st.number_input("C₀  —  Diffusion Seed",
        min_value=0, max_value=255, value=125, step=1, format="%d",
        help="Seed difusi XOR berantai.")

    N0 = st.number_input("N₀  —  Warm-up Iterations",
        min_value=100, max_value=5000, value=1000, step=100, format="%d",
        help="Iterasi pembuangan transien chaos.")

    st.markdown("---")

    st.markdown(f"""
    <div style="background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.2);
                border-radius:8px;padding:1rem 1.1rem;font-family:'JetBrains Mono',monospace;">
        <div style="font-size:0.62rem;color:#3a6080;letter-spacing:2px;margin-bottom:0.7rem;">
            // ACTIVE KEY
        </div>
        <div style="font-size:0.75rem;line-height:1.9;color:#00d4ff;">
            x₀ <span style="color:#cde8f5;">= {x0:.6f}</span><br>
            r &nbsp;<span style="color:#cde8f5;">= {r:.4f}</span><br>
            μ &nbsp;<span style="color:#cde8f5;">= {mu:.4f}</span><br>
            C₀ <span style="color:#cde8f5;">= {C0}</span><br>
            N₀ <span style="color:#cde8f5;">= {N0}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    chaos_ok = r >= 3.57 and mu >= 1.8 and 0.01 < x0 < 0.99
    color_ind = "#00ff9d" if chaos_ok else "#ff4d6d"
    bg_ind = "rgba(0,255,157,0.07)" if chaos_ok else "rgba(255,77,109,0.07)"
    border_ind = "rgba(0,255,157,0.25)" if chaos_ok else "rgba(255,77,109,0.25)"
    label_ind = "CHAOS REGIME OPTIMAL" if chaos_ok else "SUBOPTIMAL — CHECK r, μ"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.6rem;padding:0.6rem 0.8rem;
                background:{bg_ind};border:1px solid {border_ind};border-radius:6px;
                font-family:'JetBrains Mono',monospace;font-size:0.7rem;">
        <div style="width:8px;height:8px;border-radius:50%;background:{color_ind};
                    box-shadow:0 0 6px {color_ind};flex-shrink:0;"></div>
        <span style="color:{color_ind};">{label_ind}</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
col_up, col_btn = st.columns([3, 1])

with col_up:
    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                color:#3a6080;letter-spacing:2px;margin-bottom:0.5rem;">// INPUT IMAGE</div>""",
                unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload gambar (JPG / PNG)", type=["jpg","jpeg","png"],
                                label_visibility="collapsed")

with col_btn:
    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                color:#3a6080;letter-spacing:2px;margin-bottom:0.5rem;">// EXECUTE</div>""",
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
    <div style="display:flex;gap:2rem;align-items:center;
                background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.12);
                border-radius:6px;padding:0.7rem 1.2rem;
                font-family:'JetBrains Mono',monospace;font-size:0.75rem;
                color:#5a7a99;margin-bottom:0.5rem;">
        <span>SHAPE <span style="color:#00d4ff;">{M} × {N} × {ch}</span></span>
        <span>PIXELS <span style="color:#00d4ff;">{M*N:,}</span></span>
        <span>TOTAL BYTES <span style="color:#00d4ff;">{M*N*ch:,}</span></span>
    </div>
    """, unsafe_allow_html=True)

    if run_enc:
        with st.spinner("Generating chaos sequence..."):
            t0 = time.perf_counter()
            cipher, K_seq = encrypt(plain, x0, r, mu, C0, N0)
            t_enc = time.perf_counter() - t0

        with st.spinner("Verifying decryption..."):
            t0 = time.perf_counter()
            decrypted = decrypt(cipher, x0, r, mu, C0, N0)
            t_dec = time.perf_counter() - t0

        st.success(f"✓  Encryption: {t_enc:.3f}s   |   Decryption: {t_dec:.3f}s")

        # Images
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                    color:#3a6080;letter-spacing:2px;margin:1.2rem 0 0.6rem;">// VISUAL OUTPUT</div>""",
                    unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a7a99;letter-spacing:1px;margin-bottom:4px;'>PLAINTEXT</div>", unsafe_allow_html=True)
            st.image(plain, use_container_width=True)
        with c2:
            st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#00d4ff;letter-spacing:1px;margin-bottom:4px;'>CIPHERTEXT</div>", unsafe_allow_html=True)
            st.image(cipher, use_container_width=True)
        with c3:
            st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#00ff9d;letter-spacing:1px;margin-bottom:4px;'>DECRYPTED</div>", unsafe_allow_html=True)
            st.image(decrypted, use_container_width=True)

        buf_c = io.BytesIO()
        Image.fromarray(cipher).save(buf_c, format='PNG')
        st.download_button("↓  DOWNLOAD CIPHER IMAGE", data=buf_c.getvalue(),
                           file_name="cipher_tsl.png", mime="image/png")

        # Metrics
        ent_cipher  = hitung_entropi(cipher)
        mse_val, psnr_val = hitung_mse_psnr(plain, cipher)
        corr_plain  = hitung_korelasi(plain)
        corr_cipher = hitung_korelasi(cipher)
        plain_mod = plain.copy(); plain_mod[0,0,0] ^= 1
        cipher_mod, _ = encrypt(plain_mod, x0, r, mu, C0, N0)
        npcr, uaci = hitung_npcr_uaci(cipher, cipher_mod)

        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                    color:#3a6080;letter-spacing:2px;margin:1.5rem 0 0.8rem;">// SECURITY ANALYSIS</div>""",
                    unsafe_allow_html=True)

        def metric_card(col, label, val_str, sub, ok):
            color = "#00ff9d" if ok else "#ff4d6d"
            glow  = "rgba(0,255,157,0.15)" if ok else "rgba(255,77,109,0.15)"
            col.markdown(f"""
            <div style="background:#111d2e;border:1px solid {color}33;border-top:2px solid {color};
                        border-radius:8px;padding:1.1rem 1rem 0.9rem;text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                            color:#3a6080;letter-spacing:1.5px;text-transform:uppercase;">{label}</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.7rem;font-weight:700;
                            color:{color};margin:0.3rem 0 0.1rem;text-shadow:0 0 12px {glow};">{val_str}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:{color}88;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

        m1,m2,m3,m4,m5 = st.columns(5)
        metric_card(m1, "Entropy",  f"{ent_cipher:.4f}", "target > 7.9",   ent_cipher > 7.9)
        metric_card(m2, "PSNR",     f"{psnr_val:.2f}",   "dB  /  < 10",    psnr_val < 10)
        metric_card(m3, "MSE",      f"{mse_val:.0f}",    "target > 5000",  mse_val > 5000)
        metric_card(m4, "NPCR",     f"{npcr:.3f}%",      "target > 99.6%", npcr > 99.6)
        metric_card(m5, "UACI",     f"{uaci:.3f}%",      "target ≈ 33.46%",30 < uaci < 36)

        # Correlation table
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                    color:#3a6080;letter-spacing:2px;margin:1.5rem 0 0.8rem;">// PIXEL CORRELATION</div>""",
                    unsafe_allow_html=True)

        ct1, ct2 = st.columns(2)
        def corr_table(col, title, corrs, color):
            rows = ""
            for arah, val in zip(["Horizontal","Vertikal","Diagonal"], corrs):
                ok = abs(val) < 0.05
                ind_color = "#00ff9d" if ok else "#ff4d6d"
                rows += f"""<tr>
                    <td style="padding:0.4rem 0.8rem;color:#5a7a99;font-size:0.72rem;">{arah}</td>
                    <td style="padding:0.4rem 0.8rem;font-family:'JetBrains Mono',monospace;
                               color:{color};font-size:0.8rem;">{val:+.4f}</td>
                    <td style="padding:0.4rem 0.8rem;color:{ind_color};font-size:0.75rem;">
                        {'✓' if ok else '✗'}</td></tr>"""
            col.markdown(f"""
            <div style="background:#111d2e;border:1px solid rgba(0,212,255,0.12);
                        border-radius:8px;overflow:hidden;">
                <div style="padding:0.7rem 1rem;border-bottom:1px solid rgba(0,212,255,0.1);
                            font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                            color:{color};letter-spacing:1px;">{title}</div>
                <table style="width:100%;border-collapse:collapse;">{rows}</table>
            </div>""", unsafe_allow_html=True)

        corr_table(ct1, "// PLAINTEXT", corr_plain,  "#5a9fd4")
        corr_table(ct2, "// CIPHERTEXT  (ideal ≈ 0)", corr_cipher, "#00d4ff")

        # Histograms
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                    color:#3a6080;letter-spacing:2px;margin:1.5rem 0 0.8rem;">// HISTOGRAMS</div>""",
                    unsafe_allow_html=True)

        plt.style.use('dark_background')
        fig_h, axes = plt.subplots(1, 2, figsize=(13, 4))
        fig_h.patch.set_facecolor('#080d14')
        colors = ('#ff4d6d', '#00d4ff', '#00ff9d')
        for ax in axes:
            ax.set_facecolor('#0d1520')
            for sp in ax.spines.values(): sp.set_color('#162438')
            ax.tick_params(colors='#3a6080', labelsize=8)
            ax.grid(axis='y', color='#162438', linewidth=0.5, alpha=0.5)
        for i, (c, lbl) in enumerate(zip(colors, ('R','G','B'))):
            h, _ = np.histogram(plain[:,:,i].ravel(), 256, [0,256])
            axes[0].plot(h, color=c, alpha=0.8, label=lbl, linewidth=1.1)
        axes[0].set_title("Plaintext Histogram", color='#5a9fd4', fontsize=10, pad=10)
        axes[0].legend(labelcolor='#cde8f5', fontsize=8)
        for i, (c, lbl) in enumerate(zip(colors, ('R','G','B'))):
            h, _ = np.histogram(cipher[:,:,i].ravel(), 256, [0,256])
            axes[1].plot(h, color=c, alpha=0.8, label=lbl, linewidth=1.1)
        axes[1].set_title("Ciphertext Histogram  [ uniform = secure ]", color='#00d4ff', fontsize=10, pad=10)
        axes[1].legend(labelcolor='#cde8f5', fontsize=8)
        plt.tight_layout(pad=2)
        st.image(fig_bytes(fig_h), use_container_width=True)
        plt.close(fig_h)

        # Scatter
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                    color:#3a6080;letter-spacing:2px;margin:1rem 0 0.8rem;">// CORRELATION SCATTER</div>""",
                    unsafe_allow_html=True)

        rng = np.random.default_rng(42)
        xi  = rng.integers(0, M-1, 2000); yi = rng.integers(0, N-1, 2000)
        gp  = plain[:,:,0].astype(np.float64); gc = cipher[:,:,0].astype(np.float64)
        fig_s, axs = plt.subplots(3, 2, figsize=(10, 10))
        fig_s.patch.set_facecolor('#080d14')
        dirs = [
            ("Horizontal", gp[xi,yi], gp[xi,yi+1], gc[xi,yi], gc[xi,yi+1]),
            ("Vertical",   gp[xi,yi], gp[xi+1,yi], gc[xi,yi], gc[xi+1,yi]),
            ("Diagonal",   gp[xi,yi], gp[xi+1,yi+1], gc[xi,yi], gc[xi+1,yi+1]),
        ]
        for i, (nm, px, py, cx, cy) in enumerate(dirs):
            for j, ax in enumerate(axs[i]):
                ax.set_facecolor('#0d1520')
                for sp in ax.spines.values(): sp.set_color('#162438')
                ax.tick_params(colors='#3a6080', labelsize=7)
            axs[i,0].scatter(px, py, s=1.5, alpha=0.35, color='#5a9fd4')
            axs[i,0].set_title(f"Plain — {nm}  r={corr_plain[i]:.4f}", color='#5a9fd4', fontsize=8)
            axs[i,1].scatter(cx, cy, s=1.5, alpha=0.35, color='#00d4ff')
            axs[i,1].set_title(f"Cipher — {nm}  r={corr_cipher[i]:.4f}", color='#00d4ff', fontsize=8)
        plt.tight_layout(pad=2)
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
        st.success(f"✓  Decryption complete: {t_dec:.3f}s")
        d1, d2 = st.columns(2)
        d1.image(plain,  caption="Input (Cipher)", use_container_width=True)
        d2.image(result, caption="Decrypted",      use_container_width=True)
        buf_d2 = io.BytesIO()
        Image.fromarray(result).save(buf_d2, format='PNG')
        st.download_button("↓  DOWNLOAD RESULT", data=buf_d2.getvalue(),
                           file_name="decrypted_tsl.png", mime="image/png")

else:
    st.markdown("""
    <div style="margin-top:1rem;padding:2.5rem;background:#111d2e;
                border:1px solid rgba(0,212,255,0.1);border-radius:10px;text-align:center;">
        <div style="font-size:2.5rem;margin-bottom:1rem;opacity:0.3;">⬡</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:600;
                    color:#5a7a99;letter-spacing:2px;">UPLOAD AN IMAGE TO BEGIN</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                    color:#3a6080;margin-top:0.5rem;letter-spacing:1px;">
            // supports JPG & PNG  ·  configure key parameters in sidebar
        </div>
    </div>

    <div style="margin-top:1.2rem;display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
        <div style="padding:1.2rem;background:#111d2e;border:1px solid rgba(0,212,255,0.1);border-radius:8px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#3a6080;letter-spacing:1.5px;margin-bottom:0.5rem;">// LOGISTIC MAP</div>
            <div style="font-size:0.85rem;color:#5a9fd4;">r·x·(1−x) — generates chaotic pseudo-random sequence</div>
        </div>
        <div style="padding:1.2rem;background:#111d2e;border:1px solid rgba(0,212,255,0.1);border-radius:8px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#3a6080;letter-spacing:1.5px;margin-bottom:0.5rem;">// SINE MAP</div>
            <div style="font-size:0.85rem;color:#5a9fd4;">sin(π·x) — amplifies nonlinearity & unpredictability</div>
        </div>
        <div style="padding:1.2rem;background:#111d2e;border:1px solid rgba(0,212,255,0.1);border-radius:8px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#3a6080;letter-spacing:1.5px;margin-bottom:0.5rem;">// TENT MAP</div>
            <div style="font-size:0.85rem;color:#5a9fd4;">μ·min(x, 1−x) — uniform distribution enhancement</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
