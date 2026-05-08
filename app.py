# -*- coding: utf-8 -*-
"""
Streamlit UI untuk Enkripsi Citra Chaos T-S-L
Jalankan dengan: streamlit run app.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from PIL import Image
import io

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Chaos TSL Cipher",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Space Mono', monospace !important;
    }

    .main-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(120, 100, 255, 0.3);
    }

    .main-header h1 {
        color: #e0d9ff;
        font-size: 1.8rem;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .main-header p {
        color: #9b8ec4;
        margin: 0.4rem 0 0;
        font-size: 0.95rem;
    }

    .metric-box {
        background: #1a1a2e;
        border: 1px solid rgba(120, 100, 255, 0.25);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #9b8ec4;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Space Mono', monospace;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #c4b5fd;
        font-family: 'Space Mono', monospace;
    }

    .metric-status {
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    .status-ok { color: #4ade80; }
    .status-warn { color: #facc15; }

    .section-title {
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #7c6fcd;
        border-bottom: 1px solid rgba(120, 100, 255, 0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .key-badge {
        display: inline-block;
        background: rgba(120, 100, 255, 0.15);
        border: 1px solid rgba(120, 100, 255, 0.3);
        border-radius: 6px;
        padding: 0.2rem 0.6rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        color: #c4b5fd;
        margin: 2px;
    }

    div[data-testid="stSidebar"] {
        background: #0f0c29 !important;
    }

    div[data-testid="stSidebar"] label {
        color: #c4b5fd !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.8rem !important;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6d28d9, #4c1d95);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed, #5b21b6);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.4);
    }

    .info-box {
        background: rgba(120, 100, 255, 0.08);
        border-left: 3px solid #7c3aed;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #c4b5fd;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CORE FUNCTIONS (dari notebook asli)
# ─────────────────────────────────────────

def tsl_step(x: float, r: float, mu: float) -> float:
    l_x = r * x * (1 - x)
    s_x = np.sin(np.pi * l_x)
    t_x = mu * s_x if s_x < 0.5 else mu * (1 - s_x)
    return t_x


def generate_tsl_sequence(x0, r, mu, length, warmup=1000):
    x = x0
    for _ in range(warmup):
        x = tsl_step(x, r, mu)
    seq = np.empty(length)
    for i in range(length):
        x = tsl_step(x, r, mu)
        seq[i] = x
    return seq


def encrypt(img_array, x0, r, mu, C0=125, N0=1000):
    M, N, ch = img_array.shape
    L = M * N * ch
    seq = generate_tsl_sequence(x0, r, mu, length=L, warmup=N0)
    perm_idx = np.argsort(seq)
    flat = img_array.flatten()
    shuffled = flat[perm_idx]
    K_seq = (np.floor(seq * 1e14) % 256).astype(np.uint8)
    cipher_fwd = np.empty(L, dtype=np.uint8)
    cipher_fwd[0] = (int(shuffled[0]) + C0) % 256 ^ K_seq[0]
    for i in range(1, L):
        cipher_fwd[i] = (int(shuffled[i]) + int(cipher_fwd[i - 1])) % 256 ^ K_seq[i]
    cipher_flat = np.empty(L, dtype=np.uint8)
    cipher_flat[-1] = (int(cipher_fwd[-1]) + C0) % 256 ^ K_seq[-1]
    for i in range(L - 2, -1, -1):
        cipher_flat[i] = (int(cipher_fwd[i]) + int(cipher_flat[i + 1])) % 256 ^ K_seq[i]
    return cipher_flat.reshape(M, N, ch), K_seq


def decrypt(cipher_img, x0, r, mu, C0=125, N0=1000):
    M, N, ch = cipher_img.shape
    L = M * N * ch
    seq = generate_tsl_sequence(x0, r, mu, length=L, warmup=N0)
    perm_idx = np.argsort(seq)
    K_seq = (np.floor(seq * 1e14) % 256).astype(np.uint8)
    cipher_flat = cipher_img.flatten()
    cipher_fwd = np.empty(L, dtype=np.uint8)
    val = int(cipher_flat[-1]) ^ int(K_seq[-1])
    cipher_fwd[-1] = (val - C0) % 256
    for i in range(L - 2, -1, -1):
        val = int(cipher_flat[i]) ^ int(K_seq[i])
        cipher_fwd[i] = (val - int(cipher_flat[i + 1])) % 256
    shuffled = np.empty(L, dtype=np.uint8)
    val = int(cipher_fwd[0]) ^ int(K_seq[0])
    shuffled[0] = (val - C0) % 256
    for i in range(1, L):
        val = int(cipher_fwd[i]) ^ int(K_seq[i])
        shuffled[i] = (val - int(cipher_fwd[i - 1])) % 256
    inv_perm = np.empty_like(perm_idx)
    inv_perm[perm_idx] = np.arange(L)
    return shuffled[inv_perm].reshape(M, N, ch)


def hitung_entropi(img):
    hist, _ = np.histogram(img.flatten(), bins=256, range=[0, 256])
    hist = hist[hist > 0]
    prob = hist / hist.sum()
    return float(-np.sum(prob * np.log2(prob)))


def hitung_mse_psnr(img1, img2):
    a, b = img1.astype(np.float64), img2.astype(np.float64)
    mse = np.mean((a - b) ** 2)
    if mse == 0:
        return 0.0, float('inf')
    return float(mse), float(20 * math.log10(255.0 / math.sqrt(mse)))


def hitung_korelasi(img, n_sampel=5000):
    M, N = img.shape[:2]
    rng = np.random.default_rng(42)
    xi = rng.integers(0, M - 1, n_sampel)
    yi = rng.integers(0, N - 1, n_sampel)
    gray = img[:, :, 0].astype(np.float64)
    x_val = gray[xi, yi]
    corr = lambda a, b: float(np.corrcoef(a, b)[0, 1])
    return (corr(x_val, gray[xi, yi + 1]),
            corr(x_val, gray[xi + 1, yi]),
            corr(x_val, gray[xi + 1, yi + 1]))


def hitung_npcr_uaci(c1, c2):
    a, b = c1.astype(np.float64), c2.astype(np.float64)
    L = a.size
    D = (a != b).astype(np.float64)
    return float(D.sum() / L * 100.0), float(np.abs(a - b).sum() / (255.0 * L) * 100.0)


def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor='#0f0c29', edgecolor='none')
    buf.seek(0)
    return buf


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🔐 Chaos TSL Image Cipher</h1>
    <p>Enkripsi Citra berbasis Komposisi Peta Chaos — Logistik → Sine → Tent</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR — PARAMETER INPUT
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Kunci Enkripsi")
    st.markdown("---")

    x0 = st.slider(
        "x₀ — Kondisi Awal",
        min_value=0.001, max_value=0.999,
        value=0.456789, step=0.001,
        format="%.6f",
        help="Initial condition untuk chaos map. Sensitif sekali — beda sedikit = cipher beda total."
    )

    r = st.slider(
        "r — Parameter Logistik",
        min_value=2.5, max_value=4.0,
        value=3.95, step=0.01,
        format="%.2f",
        help="r > 3.57 → chaos. Ideal: mendekati 4.0 untuk entropi maksimum."
    )

    mu = st.slider(
        "μ — Parameter Tent",
        min_value=1.0, max_value=2.0,
        value=2.0, step=0.01,
        format="%.2f",
        help="μ = 2.0 menghasilkan chaos penuh pada peta Tent."
    )

    C0 = st.slider(
        "C₀ — Nilai Difusi Awal",
        min_value=0, max_value=255,
        value=125, step=1,
        help="Seed difusi untuk XOR berantai. Bagian dari kunci rahasia."
    )

    st.markdown("---")
    st.markdown("## 🔧 Konfigurasi")

    N0 = st.number_input(
        "N₀ — Iterasi Warm-Up",
        min_value=100, max_value=5000,
        value=1000, step=100,
        help="Membuang transien chaos. Lebih tinggi = lebih aman, lebih lambat."
    )

    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <b>Kunci aktif:</b><br>
        <span class="key-badge">x0={:.6f}</span>
        <span class="key-badge">r={:.2f}</span>
        <span class="key-badge">μ={:.2f}</span>
        <span class="key-badge">C0={}</span>
    </div>
    """.format(x0, r, mu, C0), unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN — UPLOAD & AKSI
# ─────────────────────────────────────────
col_upload, col_action = st.columns([3, 1])

with col_upload:
    st.markdown('<p class="section-title">📁 Upload Gambar</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Pilih file gambar (JPG / PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

with col_action:
    st.markdown('<p class="section-title">▶ Aksi</p>', unsafe_allow_html=True)
    run_encrypt = st.button("🔒 ENKRIPSI", use_container_width=True)
    run_decrypt_only = st.button("🔓 DEKRIPSI SAJA", use_container_width=True,
                                  help="Gunakan jika kamu upload gambar cipher untuk didekripsi")

# ─────────────────────────────────────────
# PROSES
# ─────────────────────────────────────────
if uploaded is not None:
    img_pil = Image.open(uploaded).convert("RGB")
    plain = np.array(img_pil, dtype=np.uint8)
    M, N, ch = plain.shape

    st.markdown(f"""
    <div class="info-box">
        📐 Dimensi gambar: <b>{M} × {N} × {ch}</b> &nbsp;|&nbsp;
        Total piksel: <b>{M*N*ch:,}</b>
    </div>
    """, unsafe_allow_html=True)

    if run_encrypt:
        # ── Enkripsi ──
        with st.spinner("Membangkitkan deret chaos & mengenkripsi…"):
            t0 = time.perf_counter()
            cipher, K_seq = encrypt(plain, x0, r, mu, C0, N0)
            t_enc = time.perf_counter() - t0

        with st.spinner("Memverifikasi dekripsi…"):
            t0 = time.perf_counter()
            decrypted = decrypt(cipher, x0, r, mu, C0, N0)
            t_dec = time.perf_counter() - t0

        st.success(f"✅ Enkripsi selesai dalam **{t_enc:.3f}s** | Dekripsi dalam **{t_dec:.3f}s**")

        # ── Tampilkan gambar ──
        st.markdown("---")
        st.markdown('<p class="section-title">🖼️ Hasil Visual</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.image(plain, caption="Citra Asli (Plaintext)", use_container_width=True)
        c2.image(cipher, caption="Citra Terenkripsi (Ciphertext)", use_container_width=True)
        c3.image(decrypted, caption="Citra Terdekripsi", use_container_width=True)

        # ── Download cipher ──
        buf_cipher = io.BytesIO()
        Image.fromarray(cipher).save(buf_cipher, format='PNG')
        st.download_button(
            "⬇️ Download Cipher Image (PNG)",
            data=buf_cipher.getvalue(),
            file_name="cipher_tsl.png",
            mime="image/png"
        )

        # ── Analisis ──
        st.markdown("---")
        st.markdown('<p class="section-title">📊 Analisis Keamanan</p>', unsafe_allow_html=True)

        ent_plain = hitung_entropi(plain)
        ent_cipher = hitung_entropi(cipher)
        mse_val, psnr_val = hitung_mse_psnr(plain, cipher)
        mse_dec, psnr_dec = hitung_mse_psnr(plain, decrypted)
        corr_plain = hitung_korelasi(plain)
        corr_cipher = hitung_korelasi(cipher)

        plain_mod = plain.copy()
        plain_mod[0, 0, 0] ^= 1
        cipher_mod, _ = encrypt(plain_mod, x0, r, mu, C0, N0)
        npcr, uaci = hitung_npcr_uaci(cipher, cipher_mod)

        # Metric cards
        m1, m2, m3, m4, m5 = st.columns(5)

        def metric_card(col, label, value, status_text, ok):
            status_class = "status-ok" if ok else "status-warn"
            col.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-status {status_class}">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)

        metric_card(m1, "Entropi Cipher", f"{ent_cipher:.4f}",
                    "✅ Ideal" if ent_cipher > 7.9 else "⚠️ Rendah",
                    ent_cipher > 7.9)
        metric_card(m2, "PSNR (Asli↔Cipher)", f"{psnr_val:.2f} dB",
                    "✅ < 10 dB" if psnr_val < 10 else "⚠️ Terlalu tinggi",
                    psnr_val < 10)
        metric_card(m3, "MSE", f"{mse_val:.1f}",
                    "✅ Tinggi" if mse_val > 5000 else "⚠️ Rendah",
                    mse_val > 5000)
        metric_card(m4, "NPCR", f"{npcr:.3f}%",
                    "✅ > 99.6%" if npcr > 99.6 else "⚠️ Kurang",
                    npcr > 99.6)
        metric_card(m5, "UACI", f"{uaci:.3f}%",
                    "✅ ≈ 33.46%" if 30 < uaci < 36 else "⚠️ Kurang",
                    30 < uaci < 36)

        # ── Tabel korelasi ──
        st.markdown("---")
        st.markdown('<p class="section-title">📐 Korelasi Piksel Berdekatan</p>', unsafe_allow_html=True)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("**Citra Asli**")
            for arah, val in zip(["Horizontal", "Vertikal", "Diagonal"], corr_plain):
                bar = "🟩" * int(abs(val) * 10) + "⬜" * (10 - int(abs(val) * 10))
                st.markdown(f"`{arah:<12}` {bar} `{val:+.4f}`")
        with col_t2:
            st.markdown("**Citra Cipher** (ideal ≈ 0)")
            for arah, val in zip(["Horizontal", "Vertikal", "Diagonal"], corr_cipher):
                bar = "🟦" * int(abs(val) * 10) + "⬜" * (10 - int(abs(val) * 10))
                ok = "✅" if abs(val) < 0.05 else "⚠️"
                st.markdown(f"`{arah:<12}` {bar} `{val:+.4f}` {ok}")

        # ── Histogram ──
        st.markdown("---")
        st.markdown('<p class="section-title">📈 Histogram & Scatter Korelasi</p>', unsafe_allow_html=True)

        plt.style.use('dark_background')
        fig_hist, axes = plt.subplots(1, 2, figsize=(12, 4))
        fig_hist.patch.set_facecolor('#0f0c29')
        colors = ('#ff6b9d', '#56c596', '#4a9eed')
        labels = ('R', 'G', 'B')
        for ax in axes:
            ax.set_facecolor('#1a1a2e')
            ax.spines[:].set_color('#302b63')
        for i, (c, lbl) in enumerate(zip(colors, labels)):
            h, _ = np.histogram(plain[:, :, i].ravel(), 256, [0, 256])
            axes[0].plot(h, color=c, alpha=0.85, label=lbl, linewidth=1.2)
        axes[0].set_title("Histogram Citra Asli", color='#c4b5fd', fontsize=11)
        axes[0].legend(labelcolor='#c4b5fd')
        axes[0].tick_params(colors='#9b8ec4')
        for i, (c, lbl) in enumerate(zip(colors, labels)):
            h, _ = np.histogram(cipher[:, :, i].ravel(), 256, [0, 256])
            axes[1].plot(h, color=c, alpha=0.85, label=lbl, linewidth=1.2)
        axes[1].set_title("Histogram Cipher (Ideal: Seragam)", color='#c4b5fd', fontsize=11)
        axes[1].legend(labelcolor='#c4b5fd')
        axes[1].tick_params(colors='#9b8ec4')
        st.image(fig_to_bytes(fig_hist), use_container_width=True)
        plt.close(fig_hist)

        # ── Scatter korelasi ──
        rng = np.random.default_rng(42)
        xi = rng.integers(0, M - 1, 2000)
        yi = rng.integers(0, N - 1, 2000)
        gray_p = plain[:, :, 0].astype(np.float64)
        gray_c = cipher[:, :, 0].astype(np.float64)

        fig_sc, axes_sc = plt.subplots(3, 2, figsize=(10, 11))
        fig_sc.patch.set_facecolor('#0f0c29')
        fig_sc.suptitle("Scatter Plot Korelasi Piksel Berdekatan",
                         color='#e0d9ff', fontsize=13, fontweight='bold')
        arah_config = [
            ("Horizontal", gray_p[xi, yi], gray_p[xi, yi + 1],
             gray_c[xi, yi], gray_c[xi, yi + 1]),
            ("Vertikal", gray_p[xi, yi], gray_p[xi + 1, yi],
             gray_c[xi, yi], gray_c[xi + 1, yi]),
            ("Diagonal", gray_p[xi, yi], gray_p[xi + 1, yi + 1],
             gray_c[xi, yi], gray_c[xi + 1, yi + 1]),
        ]
        for i, (nama, px, py, cx, cy) in enumerate(arah_config):
            for j, ax in enumerate(axes_sc[i]):
                ax.set_facecolor('#1a1a2e')
                ax.spines[:].set_color('#302b63')
                ax.tick_params(colors='#9b8ec4', labelsize=8)
            axes_sc[i, 0].scatter(px, py, s=1, alpha=0.4, color='#56c596')
            axes_sc[i, 0].set_title(f"Asli — {nama} (r={corr_plain[i]:.4f})",
                                     color='#c4b5fd', fontsize=9)
            axes_sc[i, 1].scatter(cx, cy, s=1, alpha=0.4, color='#ff6b9d')
            axes_sc[i, 1].set_title(f"Cipher — {nama} (r={corr_cipher[i]:.4f})",
                                     color='#c4b5fd', fontsize=9)
        plt.tight_layout()
        st.image(fig_to_bytes(fig_sc), use_container_width=True)
        plt.close(fig_sc)

        # ── Download decrypted ──
        buf_dec = io.BytesIO()
        Image.fromarray(decrypted).save(buf_dec, format='PNG')
        st.download_button(
            "⬇️ Download Gambar Terdekripsi (PNG)",
            data=buf_dec.getvalue(),
            file_name="decrypted_tsl.png",
            mime="image/png"
        )

    elif run_decrypt_only:
        with st.spinner("Mendekripsi gambar…"):
            t0 = time.perf_counter()
            result = decrypt(plain, x0, r, mu, C0, N0)
            t_dec = time.perf_counter() - t0
        st.success(f"✅ Dekripsi selesai dalam **{t_dec:.3f}s**")
        col_a, col_b = st.columns(2)
        col_a.image(plain, caption="Input (Cipher)", use_container_width=True)
        col_b.image(result, caption="Hasil Dekripsi", use_container_width=True)
        buf_dec2 = io.BytesIO()
        Image.fromarray(result).save(buf_dec2, format='PNG')
        st.download_button("⬇️ Download Hasil Dekripsi", data=buf_dec2.getvalue(),
                           file_name="decrypted_tsl.png", mime="image/png")

else:
    st.markdown("""
    <div class="info-box">
        👆 Upload gambar di atas untuk memulai, lalu tekan tombol <b>ENKRIPSI</b>.
        <br><br>
        Parameter kunci bisa diatur bebas di sidebar kiri. Perubahan kecil pada x₀
        akan menghasilkan cipher yang sama sekali berbeda — itulah kekuatan chaos map!
    </div>
    """, unsafe_allow_html=True)

    # Preview parameter info
    st.markdown("---")
    st.markdown('<p class="section-title">📖 Panduan Parameter</p>', unsafe_allow_html=True)
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        st.markdown("""
        | Parameter | Range | Fungsi |
        |-----------|-------|--------|
        | **x₀** | 0.001–0.999 | Kondisi awal chaos, kunci utama |
        | **r** | 2.5–4.0 | Laju pertumbuhan logistik |
        | **μ** | 1.0–2.0 | Parameter peta Tent |
        | **C₀** | 0–255 | Seed difusi XOR |
        """)
    with pcol2:
        st.markdown("""
        **💡 Tips:**
        - `x₀` dan `r` adalah kunci terpenting
        - Gunakan `r ≥ 3.9` untuk chaos optimal
        - `μ = 2.0` = chaos penuh pada Tent map
        - `N₀ = 1000` sudah cukup untuk keamanan standar
        """)
