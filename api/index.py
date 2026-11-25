import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

DEFAULT_QUANT_API = os.environ.get("QUANT_API_URL", "").strip().rstrip("/")


@app.route('/manifest.json')
def manifest():
    return {
        "background_color": "#000000",
        "dir": "ltr",
        "display": "standalone",
        "name": "ZIGFT calculator",
        "orientation": "portrait",
        "scope": "/",
        "short_name": "ZIGFT",
        "start_url": "/",
        "theme_color": "#000000",
        "id": "/",
        "description": "Professional Entry, Stop Loss, and Take Profit calculator for Trader Family analysts to simplify market analysis.",
        "lang": "id",
        "categories": [
            "finance"
        ],
        "icons": [
            {
                "src": "https://raw.githubusercontent.com/zenaiskandewigroup-sys/zigft-calculator/main/icon.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }


@app.route('/.well-known/assetlinks.json')
def assetlinks():
    return [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "app.vercel.zigft_calculator.twa",
            "sha256_cert_fingerprints": [
                "18:5B:EE:A9:AA:8C:84:0D:79:F7:36:E9:23:32:4A:D6:D7:57:5E:6F:39:0A:CB:14:29:E1:EC:1C:27:EB:E9:7F"
            ]
        }
    }]


BASE_CSS = """
  :root {
    --bg-main: #000000;
    --bg-card: #0a0a0a;
    --border: #222222;
    --border-focus: #444444;
    --text-main: #ededed;
    --text-muted: #888888;
    --accent: #ffffff;
    --accent-hover: #e0e0e0;
    --neon-green: #00e676;
    --danger: #f44336;
    --warn: #ffc107;
  }
  body {
    background-color: var(--bg-main);
    color: var(--text-main);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 15px 40px 15px;
    margin: 0;
  }
  .container { max-width: 540px; width: 100%; position: relative; }
  .top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 6px;
  }
  .nav-tabs-wrap { display: flex; gap: 6px; flex: 1; }
  .nav-pill {
    flex: 1;
    text-align: center;
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 9px 10px;
    border-radius: 7px;
    color: var(--text-muted);
    transition: all 0.2s ease;
  }
  .nav-pill:hover { color: var(--text-main); }
  .nav-pill.active {
    background: #161616;
    color: var(--neon-green);
    border: 1px solid rgba(0, 230, 118, 0.25);
  }
  .api-config-btn {
    background: var(--bg-main);
    border: 1px solid var(--border);
    color: var(--text-muted);
    border-radius: 7px;
    padding: 8px 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    white-space: nowrap;
  }
  .api-config-btn:hover { border-color: var(--border-focus); color: var(--text-main); }
  .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #555; }
  .status-dot.active { background: var(--neon-green); box-shadow: 0 0 6px var(--neon-green); }

  /* LIVE NEWS COUNTDOWN BANNER (TOP) */
  .news-banner {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 14px;
  }
  .news-banner-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }
  .news-timer-box {
    font-family: monospace;
    font-size: 0.95rem;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 6px;
    background: rgba(0, 230, 118, 0.12);
    color: var(--neon-green);
    border: 1px solid rgba(0, 230, 118, 0.3);
    letter-spacing: 0.5px;
  }
  .news-timer-box.urgent {
    background: rgba(244, 67, 54, 0.16);
    color: #ff6b6b;
    border-color: rgba(244, 67, 54, 0.45);
  }

  .dashboard-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 26px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  }
  .header { margin-bottom: 22px; }
  .header h3 {
    color: var(--text-main);
    font-weight: 700;
    font-size: 1.35rem;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .header p { color: var(--text-muted); font-size: 0.82rem; margin: 0; }
  .form-label { color: var(--text-muted) !important; font-weight: 500; font-size: 0.83rem; margin-bottom: 6px; }
  .form-control, .form-select {
    background-color: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-main) !important;
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 0.95rem;
  }
  .form-control:focus, .form-select:focus {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.05) !important;
  }
  .form-control::placeholder { color: #444 !important; }
  #pairInput { cursor: pointer; }

  .btn-submit {
    background: var(--accent);
    color: #000;
    font-weight: 600;
    border: none;
    font-size: 0.95rem;
    padding: 13px;
    border-radius: 8px;
    transition: all 0.2s ease;
    margin-top: 8px;
  }
  .btn-submit:hover { background: var(--accent-hover); transform: translateY(-1px); }
  .btn-neon {
    background: var(--neon-green);
    color: #000;
    font-weight: 700;
    border: none;
    font-size: 0.9rem;
    padding: 12px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .btn-neon:disabled {
    background: #1b1b1b;
    color: #555;
    cursor: not-allowed;
  }
  .btn-outline-custom {
    background: #111111;
    border: 1px solid #2c2c2c;
    color: var(--text-main);
    font-size: 0.85rem;
    font-weight: 600;
    padding: 11px 14px;
    border-radius: 8px;
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: rgba(0, 230, 118, 0.2);
    transition: transform 0.12s ease, background 0.15s ease, border-color 0.15s ease;
  }
  .btn-outline-custom:hover {
    background: #191919;
    border-color: var(--neon-green);
  }
  .btn-outline-custom:active {
    transform: scale(0.95);
    background: rgba(0, 230, 118, 0.15);
  }
  .btn-outline-custom:disabled {
    color: #666;
    border-color: #1c1c1c;
    background: #090909;
    cursor: wait;
    transform: none;
  }
  .btn-mini-spin {
    display: inline-block;
    width: 12px;
    height: 12px;
    border: 2px solid #444;
    border-top-color: var(--neon-green);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    vertical-align: middle;
  }

  .result-wrapper, .quant-section {
    margin-top: 20px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px;
  }
  .result-header, .quant-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .data-item {
    background: var(--bg-main);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
  }
  .data-label { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  .data-value { font-size: 1.05rem; font-weight: 600; color: var(--text-main); }
  .val-container { display: flex; align-items: center; justify-content: space-between; }
  .copy-btn {
    background: none; border: none; color: var(--text-muted); cursor: pointer;
    padding: 6px; border-radius: 6px; display: flex; align-items: center; justify-content: center;
  }
  .copy-btn:hover { background: rgba(255,255,255,0.1); color: var(--text-main); }

  .status-badge {
    margin-top: 16px; padding: 12px; border-radius: 8px; font-weight: 500; font-size: 0.85rem;
    display: flex; align-items: center; justify-content: center; gap: 8px;
  }
  .status-valid { background: rgba(40, 167, 69, 0.1); color: #4caf50; border: 1px solid rgba(40, 167, 69, 0.2); }
  .status-invalid { background: rgba(220, 53, 69, 0.1); color: #f44336; border: 1px solid rgba(220, 53, 69, 0.2); }

  .quant-tag {
    font-size: 0.7rem; padding: 3px 8px; border-radius: 6px;
    background: rgba(0, 230, 118, 0.12); color: var(--neon-green);
    border: 1px solid rgba(0, 230, 118, 0.25); font-weight: 600;
  }
  .q-card {
    background: var(--bg-main);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 12px;
  }
  .q-card:last-child { margin-bottom: 0; }
  .q-card-head {
    display: flex; justify-content: space-between; align-items: center; gap: 8px;
    margin-bottom: 8px; font-size: 0.76rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.4px;
  }
  .q-pill { font-size: 0.68rem; font-weight: 600; padding: 2px 8px; border-radius: 4px; white-space: nowrap; }
  .pill-green { background: rgba(76, 175, 80, 0.15); color: #4caf50; border: 1px solid rgba(76, 175, 80, 0.3); }
  .pill-yellow { background: rgba(255, 193, 7, 0.15); color: #ffc107; border: 1px solid rgba(255, 193, 7, 0.3); }
  .pill-red { background: rgba(244, 67, 54, 0.15); color: #f44336; border: 1px solid rgba(244, 67, 54, 0.3); }
  .pill-neutral { background: rgba(255, 255, 255, 0.08); color: #ccc; border: 1px solid #333; }

  .liq-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 8px; }
  .liq-box { background: #0a0a0a; border: 1px solid #1e1e1e; border-radius: 6px; padding: 8px; text-align: center; }
  .liq-lbl { font-size: 0.66rem; color: var(--text-muted); }
  .liq-val { font-size: 0.83rem; font-weight: 600; color: var(--text-main); margin-top: 2px; }

  .progress-track { width: 100%; height: 6px; background: #1a1a1a; border-radius: 4px; overflow: hidden; margin: 8px 0; }
  .progress-fill { height: 100%; background: var(--neon-green); transition: width 0.4s ease; }

  .csm-bar-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; font-size: 0.85rem; margin-top: 6px; }
  .csm-rank-strip { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #222; }
  .csm-chip { font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: #111; border: 1px solid #262626; color: #bbb; }
  .alert-box-warn {
    margin-top: 8px; padding: 8px 10px; border-radius: 6px;
    background: rgba(244, 67, 54, 0.12); border: 1px solid rgba(244, 67, 54, 0.3);
    color: #ff6b6b; font-size: 0.79rem;
  }

  .gate-check {
    display: flex; align-items: center; gap: 10px; padding: 10px 12px;
    background: #0d0d0d; border: 1px solid #222; border-radius: 8px;
    margin-bottom: 8px; cursor: pointer; font-size: 0.83rem;
  }
  .gate-check input { width: 16px; height: 16px; accent-color: var(--neon-green); cursor: pointer; }

  .spinner-box { text-align: center; padding: 20px 10px; color: var(--text-muted); font-size: 0.84rem; }
  .spinner-ring {
    width: 22px; height: 22px; border: 2px solid #333; border-top-color: var(--neon-green);
    border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 10px auto;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Modal */
  .modal-overlay {
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.85); z-index: 9999; align-items: center; justify-content: center;
    backdrop-filter: blur(5px);
  }
  .modal-container {
    background: var(--bg-main); width: 100%; max-width: 520px; height: 100%; max-height: 100vh;
    display: flex; flex-direction: column; animation: slideUp 0.25s ease-out;
  }
  @media (min-width: 521px) {
    .modal-container { height: 85vh; border-radius: 12px; border: 1px solid var(--border); }
  }
  @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
  .modal-header { display: flex; align-items: center; padding: 18px 20px; border-bottom: 1px solid var(--border); }
  .modal-header h4 { margin: 0; font-size: 1.05rem; font-weight: 600; color: var(--text-main); flex: 1; text-align: center; }
  .close-modal-btn { background: none; border: none; color: var(--text-main); padding: 5px; cursor: pointer; display: flex; align-items: center; }
  .modal-search-wrapper { padding: 14px 20px; border-bottom: 1px solid var(--border); position: relative; }
  .modal-search-icon { position: absolute; left: 35px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
  .modal-search-wrapper input {
    width: 100%; padding: 11px 16px 11px 42px; background: var(--bg-card); border: 1px solid var(--border);
    color: var(--text-main); border-radius: 8px; font-size: 0.92rem; outline: none;
  }
  .list-header {
    display: flex; justify-content: space-between; padding: 10px 24px; font-size: 0.75rem;
    color: var(--text-muted); text-transform: uppercase; background: var(--bg-card); border-bottom: 1px solid var(--border);
  }
  .modal-list { flex: 1; overflow-y: auto; padding-bottom: 20px; }
  .symbol-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 15px 24px; border-bottom: 1px solid var(--border); cursor: pointer;
  }
  .symbol-item:hover { background: var(--bg-card); }
  .symbol-item .pair-name { font-weight: 500; font-size: 0.98rem; color: var(--text-main); }
  .symbol-item .pair-vp { color: var(--text-muted); font-size: 0.92rem; }

  /* PnL Calendar Grid */
  .cal-header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .cal-nav-btn {
    background: #121212; border: 1px solid #262626; color: var(--text-main);
    border-radius: 6px; padding: 5px 11px; font-size: 0.85rem; cursor: pointer;
  }
  .cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
  .cal-dow { text-align: center; font-size: 0.7rem; color: var(--text-muted); padding-bottom: 4px; font-weight: 600; }
  .cal-cell {
    background: #0e0e0e; border: 1px solid #1e1e1e; border-radius: 7px; min-height: 54px;
    padding: 5px 4px; display: flex; flex-direction: column; justify-content: space-between;
    align-items: center; cursor: pointer; transition: transform 0.15s ease;
  }
  .cal-cell:hover { transform: scale(1.03); }
  .cal-cell.empty { background: transparent; border-color: transparent; cursor: default; }
  .cal-cell.profit { background: rgba(0, 230, 118, 0.14); border-color: rgba(0, 230, 118, 0.45); }
  .cal-cell.loss { background: rgba(244, 67, 54, 0.15); border-color: rgba(244, 67, 54, 0.45); }
  .cal-day-num { font-size: 0.7rem; color: var(--text-muted); align-self: flex-start; padding-left: 2px; }
  .cal-pnl-txt { font-size: 0.72rem; font-weight: 700; text-align: center; line-height: 1.1; }
  .cal-cell.profit .cal-pnl-txt { color: var(--neon-green); }
  .cal-cell.loss .cal-pnl-txt { color: #ff6b6b; }

  footer { margin-top: 28px; text-align: center; font-size: 0.78rem; color: #555; }
"""


COMMON_API_MODAL = """
  <div id="apiModal" class="modal-overlay">
    <div class="modal-container" style="height: auto; max-height: 90vh; padding: 24px;">
      <div class="modal-header" style="padding: 0 0 16px 0;">
        <button class="close-modal-btn" onclick="closeApiModal()">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
        <h4>Koneksi Render Quant Engine</h4>
        <div style="width: 22px;"></div>
      </div>
      <div style="margin-top: 16px;">
        <label class="form-label">URL Backend Render Anda</label>
        <input type="url" id="renderUrlInput" class="form-control" placeholder="https://zigft-calculator-backend.onrender.com">
        <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 8px;">
          URL tersimpan otomatis di browser perangkat ini dan menghubungkan Hitung Mundur News, Kalkulator Quant, serta Kalender PnL.
        </p>
        <button type="button" class="btn btn-submit w-100" onclick="saveRenderUrl()">Simpan &amp; Hubungkan</button>
      </div>
    </div>
  </div>

  <script>
    const ENV_QUANT_API = "{{ default_quant_api }}";
    function getQuantApiUrl() {
      const saved = localStorage.getItem("zigft_quant_api_url");
      if (saved && saved.trim() !== "") return saved.trim().replace(/\/+$/, "");
      return ENV_QUANT_API;
    }
    function updateStatusDot() {
      const dot = document.getElementById("quantStatusDot");
      if (!dot) return;
      if (getQuantApiUrl()) dot.classList.add("active");
      else dot.classList.remove("active");
    }
    function openApiModal() {
      document.getElementById("renderUrlInput").value = getQuantApiUrl();
      document.getElementById("apiModal").style.display = "flex";
    }
    function closeApiModal() {
      document.getElementById("apiModal").style.display = "none";
    }
    function saveRenderUrl() {
      const val = document.getElementById("renderUrlInput").value.trim().replace(/\/+$/, "");
      localStorage.setItem("zigft_quant_api_url", val);
      updateStatusDot();
      closeApiModal();
      if (typeof onApiConnected === "function") onApiConnected();
    }
    updateStatusDot();
  </script>
"""


HTML_CALCULATOR = """
<!DOCTYPE html>
<html lang="id">
<head>
  <link rel="manifest" href="/manifest.json">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ZIGFT Terminal | TF 2025 Quant Calculator</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>{{ base_css | safe }}</style>
</head>
<body>
  <div class="container">
    <div class="top-nav">
      <div class="nav-tabs-wrap">
        <a href="/" class="nav-pill active">Kalkulator &amp; Quant</a>
        <a href="/portfolio" class="nav-pill">Kalender PnL &amp; Curve</a>
      </div>
      <button type="button" class="api-config-btn" onclick="openApiModal()">
        <span id="quantStatusDot" class="status-dot"></span>
        <span>Quant API</span>
      </button>
    </div>

    <!-- TOP LIVE MACRO NEWS COUNTDOWN & PRE-NEWS BIAS BANNER -->
    <div class="news-banner" id="topNewsBanner">
      <div class="news-banner-head">
        <span style="font-size:0.74rem; color:var(--text-muted); text-transform:uppercase; font-weight:600;">
          High-Impact News Countdown
        </span>
        <span class="news-timer-box" id="newsCountdownClock">--:--:--</span>
      </div>
      <div id="topNewsContent" style="font-size:0.82rem; color:var(--text-muted);">
        Memuat jadwal berita high-impact &amp; proyeksi arah...
      </div>
    </div>

    <div class="dashboard-card">
      <div class="header">
        <h3>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
          Auto Price v9.0
        </h3>
        <p>SMC OTE • Pre-News Bot • ZIGFT Rule Enforcer • TF 2025</p>
      </div>

      <form method="POST" onsubmit="return validatePairForm()">
        <div class="mb-3">
          <label class="form-label">Pair</label>
          <input type="text" id="pairInput" name="pair" class="form-control" placeholder="Pilih Symbol" value="{{ result.pair if result else '' }}" readonly onclick="openModal()" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Side</label>
          <select name="side" class="form-select" required>
            <option value="buy" {% if result and result.side == 'buy' %}selected{% endif %}>Buy</option>
            <option value="sell" {% if result and result.side == 'sell' %}selected{% endif %}>Sell</option>
          </select>
        </div>
        <div class="mb-3">
          <label class="form-label">Entry Price</label>
          <input type="number" step="any" name="entry" class="form-control" placeholder="contoh: 2650.50 atau 0.65352" value="{{ result.entry if result else '' }}" required>
        </div>
        <div class="mb-3">
          <label class="form-label">RR (1 - 3)</label>
          <input type="number" step="0.1" name="rr" class="form-control" placeholder="contoh: 3" value="{{ result.rr if result else '' }}" required>
        </div>
        <button type="submit" class="btn btn-submit w-100">Hitung SL/TP &amp; Analisis Quant</button>
      </form>
    </div>

    {% if result %}
    <div class="result-wrapper">
      <div class="result-header">
        <span>Hasil Perhitungan</span>
        <span style="font-size: 0.78rem; color: var(--neon-green); font-weight: 600;">{{ result.pair }} • 1:{{ result.rr }}</span>
      </div>
      <div class="result-grid">
        <div class="data-item">
          <div class="data-label">Pair</div>
          <div class="data-value">{{ result.pair }}</div>
        </div>
        <div class="data-item">
          <div class="data-label">Side / RR</div>
          <div class="data-value">{{ result.side.upper() }} <span style="font-size: 0.85rem; color: #888;">(1:{{ result.rr }})</span></div>
        </div>
        <div class="data-item">
          <div class="data-label">Entry</div>
          <div class="val-container">
            <div class="data-value">{{ result.entry }}</div>
            <button type="button" class="copy-btn" onclick="copyText('{{ result.entry }}', this)" title="Salin Entry">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            </button>
          </div>
        </div>
        <div class="data-item">
          <div class="data-label">Value Pair</div>
          <div class="data-value">{{ result.value_pair }}</div>
        </div>
        <div class="data-item" style="border-color: rgba(244, 67, 54, 0.3);">
          <div class="data-label" style="color: #f44336;">Stop Loss (SL)</div>
          <div class="val-container">
            <div>
              <span class="data-value">{{ result.sl }}</span><br>
              <span style="font-size: 0.78rem; color: #888;">(-{{ result.sl_pips }} pips)</span>
            </div>
            <button type="button" class="copy-btn" onclick="copyText('{{ result.sl }}', this)" title="Salin SL">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            </button>
          </div>
        </div>
        <div class="data-item" style="border-color: rgba(76, 175, 80, 0.3);">
          <div class="data-label" style="color: #4caf50;">Take Profit (TP)</div>
          <div class="val-container">
            <div>
              <span class="data-value">{{ result.tp }}</span><br>
              <span style="font-size: 0.78rem; color: #888;">(+{{ result.tp_pips }} pips)</span>
            </div>
            <button type="button" class="copy-btn" onclick="copyText('{{ result.tp }}', this)" title="Salin TP">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            </button>
          </div>
        </div>
      </div>

      {% if result.valid %}
        <div class="status-badge status-valid">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          Valid TF 2025 ({{ result.validation_text }})
        </div>
      {% else %}
        <div class="status-badge status-invalid">
          Tidak Valid TF 2025 ({{ result.validation_text }})
        </div>
      {% endif %}

      <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <span style="font-size:0.78rem; font-weight:600; color:var(--text-muted); text-transform:uppercase;">ZIGFT Structure &amp; Discipline Gate</span>
          <span id="ruleQuotaBadge" class="q-pill pill-neutral">Checking Quota...</span>
        </div>

        <div id="cooldownBanner"></div>

        <label class="gate-check">
          <input type="checkbox" id="chkIdm" onchange="updateActionGate()">
          <span><strong>Inducement (IDM)</strong> sudah tervalidasi pada struktur</span>
        </label>
        <label class="gate-check">
          <input type="checkbox" id="chkLiq" onchange="updateActionGate()">
          <span><strong>Liquidity Pool / Sweep</strong> sudah terkonfirmasi</span>
        </label>

        <div id="lotSimBox" style="font-size:0.78rem; color:var(--text-muted); margin: 8px 0 10px 0;"></div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px;">
          <button type="button" id="btnCopySignal" class="btn-outline-custom" disabled onclick="copyFullSignal(this)">
            Salin Format Signal
          </button>
          <button type="button" id="btnLogEntry" class="btn-neon" disabled onclick="logEntryToPortfolio()">
            Catat Entry (1 Lot)
          </button>
        </div>
        <div id="logFeedback" style="font-size:0.8rem; margin-top:8px;"></div>
      </div>
    </div>

    <div class="quant-section" id="quantPanel">
      <div class="quant-title">
        <span>Quant Market Intelligence</span>
        <span class="quant-tag" id="quantSourceTag">LIVE FEED</span>
      </div>
      <div id="correlationBox"></div>
      <div id="quantDynamicBody">
        <div class="spinner-box">
          <div class="spinner-ring"></div>
          <div>Menganalisis Pre-News Bot, SMC OTE 50%–75%, Likuiditas &amp; ATR-14...</div>
        </div>
      </div>
    </div>
    {% endif %}

    <footer>© 2025 MaelFX × Idris Lab | TF 2025 &amp; ZIGFT System Integrated</footer>
  </div>

  <!-- POP-UP MODAL SYMBOL SELECTION -->
  <div id="symbolModal" class="modal-overlay">
    <div class="modal-container">
      <div class="modal-header">
        <button class="close-modal-btn" onclick="closeModal()">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        </button>
        <h4>Pilih Symbol</h4>
        <div style="width: 24px;"></div>
      </div>
      <div class="modal-search-wrapper">
        <svg class="modal-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="searchInput" placeholder="Cari Symbol..." onkeyup="filterSymbols()">
      </div>
      <div class="list-header">
        <span>Symbols/Pair</span>
        <span>Value Pair</span>
      </div>
      <div class="modal-list" id="symbolList">
        {% for pair_name, rule_data in tf_rules.items() %}
        <div class="symbol-item" onclick="selectPair('{{ pair_name }}')">
          <span class="pair-name">{{ pair_name }}</span>
          <span class="pair-vp">{{ rule_data.vp }}</span>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>

  {{ common_api_modal | safe }}

  <script>
    let targetNewsReleaseMs = null;
    let countdownTimerId = null;

    function startNewsCountdown(releaseTsMs) {
      targetNewsReleaseMs = releaseTsMs;
      if (countdownTimerId) clearInterval(countdownTimerId);

      function tick() {
        const clockEl = document.getElementById("newsCountdownClock");
        if (!clockEl || !targetNewsReleaseMs) return;

        const diffMs = targetNewsReleaseMs - Date.now();
        if (diffMs <= 0) {
          clockEl.innerText = "RILIS SEKARANG";
          clockEl.classList.add("urgent");
          return;
        }

        const totalSec = Math.floor(diffMs / 1000);
        const hrs = String(Math.floor(totalSec / 3600)).padStart(2, "0");
        const mins = String(Math.floor((totalSec % 3600) / 60)).padStart(2, "0");
        const secs = String(totalSec % 60).padStart(2, "0");

        clockEl.innerText = `${hrs}:${mins}:${secs}`;
        if (totalSec <= 1800) clockEl.classList.add("urgent");
        else clockEl.classList.remove("urgent");
      }

      tick();
      countdownTimerId = setInterval(tick, 1000);
    }

    async function loadTopNewsBanner(pairFilter = "") {
      const contentEl = document.getElementById("topNewsContent");
      const clockEl = document.getElementById("newsCountdownClock");
      const apiBase = getQuantApiUrl();

      if (!apiBase) {
        clockEl.innerText = "NO API";
        contentEl.innerHTML = `Hubungkan URL Render lewat tombol <strong>Quant API</strong> di pojok kanan atas untuk mengaktifkan hitung mundur news.`;
        return;
      }

      try {
        const q = pairFilter ? `?pair=${encodeURIComponent(pairFilter)}` : "";
        const resp = await fetch(`${apiBase}/api/news-radar${q}`);
        const data = await resp.json();
        if (!resp.ok || data.error) throw new Error(data.error || "Gagal memuat jadwal news");

        const nw = data.news;
        if (!nw.has_event) {
          clockEl.innerText = "AMAN";
          clockEl.classList.remove("urgent");
          contentEl.innerHTML = `<span style="color:#4caf50;">✓</span> ${nw.note}`;
          return;
        }

        if (nw.release_ts_ms) {
          startNewsCountdown(nw.release_ts_ms);
        }

        const predColor = nw.prediction.includes("BULLISH") ? "#00e676" : (nw.prediction.includes("BEARISH") ? "#ff6b6b" : "#ffc107");
        contentEl.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:3px;">
            <strong style="color:var(--text-main); font-size:0.86rem;">[${nw.currency}] ${nw.title}</strong>
            <span style="font-size:0.72rem; font-weight:700; color:${predColor};">${nw.prediction}</span>
          </div>
          <div style="font-size:0.76rem; color:var(--text-muted);">
            Jadwal: <strong style="color:#ddd;">${nw.release_wib}</strong> • Forecast: <strong>${nw.forecast}</strong> | Prev: <strong>${nw.previous}</strong>
          </div>
          <div style="font-size:0.77rem; color:#ccc; margin-top:3px;">${nw.reasoning}</div>
        `;
      } catch (err) {
        clockEl.innerText = "SLEEP";
        contentEl.innerHTML = `Server Render sedang bangun: ${err.message}`;
      }
    }

    function validatePairForm() {
      if (!document.getElementById("pairInput").value.trim()) {
        openModal();
        return false;
      }
      return true;
    }
    function copyText(text, btnElement) {
      navigator.clipboard.writeText(text).then(() => {
        const orig = btnElement.innerHTML;
        btnElement.innerHTML = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        setTimeout(() => { btnElement.innerHTML = orig; }, 1500);
      });
    }
    function openModal() {
      document.getElementById('symbolModal').style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
    function closeModal() {
      document.getElementById('symbolModal').style.display = 'none';
      document.body.style.overflow = 'auto';
    }
    function selectPair(pairName) {
      document.getElementById('pairInput').value = pairName;
      closeModal();
      loadTopNewsBanner(pairName);
    }
    function filterSymbols() {
      const filter = document.getElementById('searchInput').value.toUpperCase();
      const items = document.getElementById('symbolList').getElementsByClassName('symbol-item');
      for (let i = 0; i < items.length; i++) {
        const name = items[i].getElementsByClassName('pair-name')[0].innerText;
        items[i].style.display = name.toUpperCase().indexOf(filter) > -1 ? "flex" : "none";
      }
    }

    loadTopNewsBanner("{{ result.pair if result else '' }}");

    {% if result %}
    let latestQuantData = null;

    function updateActionGate() {
      const idmChecked = document.getElementById("chkIdm").checked;
      const liqChecked = document.getElementById("chkLiq").checked;
      const structureValid = idmChecked && liqChecked;

      document.getElementById("btnCopySignal").disabled = !structureValid;

      const canEnter = latestQuantData && latestQuantData.zigft_rules ? latestQuantData.zigft_rules.can_enter : true;
      document.getElementById("btnLogEntry").disabled = !(structureValid && canEnter);
    }

    function copyFullSignal(btn) {
      const txt = [
        `PAIR: {{ result.pair }}`,
        `ORDER: {{ result.side.upper() }} (RR 1:{{ result.rr }})`,
        `ENTRY: {{ result.entry }}`,
        `SL: {{ result.sl }} (-{{ result.sl_pips }} pips)`,
        `TP: {{ result.tp }} (+{{ result.tp_pips }} pips)`,
        `VALIDASI: IDM + Liquidity Confirmed | ZIGFT System`
      ].join("\\n");
      navigator.clipboard.writeText(txt).then(() => {
        const orig = btn.innerText;
        btn.innerText = "✓ Tersalin!";
        setTimeout(() => { btn.innerText = orig; }, 1500);
      });
    }

    async function logEntryToPortfolio() {
      const apiBase = getQuantApiUrl();
      const fb = document.getElementById("logFeedback");
      const btn = document.getElementById("btnLogEntry");
      if (!apiBase) { openApiModal(); return; }

      btn.disabled = true;
      fb.style.color = "#888";
      fb.innerText = "Mencatat entry ke sistem pemantauan harga...";

      try {
        const resp = await fetch(`${apiBase}/api/entries`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            pair: "{{ result.pair }}",
            side: "{{ result.side }}",
            entry: {{ result.entry }},
            sl: {{ result.sl }},
            tp: {{ result.tp }},
            sl_pips: {{ result.sl_pips }},
            tp_pips: {{ result.tp_pips }},
            rr: {{ result.rr }},
            inducement_confirmed: document.getElementById("chkIdm").checked,
            liquidity_confirmed: document.getElementById("chkLiq").checked
          })
        });
        const data = await resp.json();
        if (!resp.ok || data.error) throw new Error(data.error || "Gagal mencatat entry");

        fb.style.color = "#00e676";
        fb.innerText = "✓ " + data.message;
        runQuantFetch();
      } catch (err) {
        fb.style.color = "#ff6b6b";
        fb.innerText = "✕ " + err.message;
        updateActionGate();
      }
    }

    function checkCorrelationGuard(pair, side) {
      const todayKey = "zigft_setups_" + new Date().toISOString().slice(0, 10);
      let setups = [];
      try { setups = JSON.parse(localStorage.getItem(todayKey) || "[]"); } catch (e) { setups = []; }

      const base = pair.slice(0, 3), quote = pair.slice(3);
      const currExp = {};
      currExp[base] = side === "buy" ? 1 : -1;
      currExp[quote] = side === "buy" ? -1 : 1;

      const conflicts = [];
      setups.forEach(s => {
        if (s.pair === pair && s.side === side) return;
        const sExp = {};
        sExp[s.pair.slice(0, 3)] = s.side === "buy" ? 1 : -1;
        sExp[s.pair.slice(3)] = s.side === "buy" ? -1 : 1;
        for (const ccy of Object.keys(currExp)) {
          if (sExp[ccy] && sExp[ccy] === currExp[ccy]) {
            conflicts.push(`${ccy} (${currExp[ccy] > 0 ? "Long" : "Short"}) searah dengan ${s.pair} ${s.side.toUpperCase()}`);
          }
        }
      });

      const filtered = setups.filter(s => !(s.pair === pair && s.side === side));
      filtered.push({ pair: pair, side: side, ts: Date.now() });
      localStorage.setItem(todayKey, JSON.stringify(filtered.slice(-10)));

      const box = document.getElementById("correlationBox");
      if (conflicts.length > 0 && box) {
        box.innerHTML = `
          <div class="q-card" style="border-color: rgba(255, 193, 7, 0.35);">
            <div class="q-card-head">
              <span style="color: #ffc107;">Correlation Exposure Guard</span>
              <span class="q-pill pill-yellow">STACKED RISK</span>
            </div>
            <div style="font-size: 0.8rem; color: #ddd;">
              Eksposur mata uang ganda: <strong>${[...new Set(conflicts)].join(" • ")}</strong>.
            </div>
          </div>
        `;
      }
    }

    async function runQuantFetch() {
      const container = document.getElementById("quantDynamicBody");
      const apiBase = getQuantApiUrl();

      if (!apiBase) {
        container.innerHTML = `
          <div class="q-card">
            <div style="font-size: 0.84rem; color: var(--text-muted); margin-bottom: 10px;">
              URL Backend Render belum diatur. Klik <strong>Quant API</strong> di kanan atas untuk menghubungkan.
            </div>
            <button type="button" class="btn btn-submit w-100" style="padding:10px; font-size:0.85rem;" onclick="openApiModal()">Hubungkan URL Render</button>
          </div>
        `;
        return;
      }

      try {
        const resp = await fetch(`${apiBase}/api/quant-analysis`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            pair: "{{ result.pair }}",
            side: "{{ result.side }}",
            entry: {{ result.entry }},
            sl: {{ result.sl }},
            tp: {{ result.tp }},
            sl_pips: {{ result.sl_pips }},
            tp_pips: {{ result.tp_pips }},
            rr: {{ result.rr }}
          })
        });

        const data = await resp.json();
        if (!resp.ok || data.error) throw new Error(data.error || "Gagal memuat analisis");
        latestQuantData = data;

        document.getElementById("quantSourceTag").innerText = `${data.feed_source}${data.spot_calibrated ? " • SPOT CAL" : ""}`;

        const zr = data.zigft_rules;
        const badge = document.getElementById("ruleQuotaBadge");
        badge.innerText = `Entry: ${zr.daily_used}/${zr.daily_max} Hari Ini • SL: ${zr.monthly_sl_used}/${zr.monthly_sl_max} Bulan Ini`;
        badge.className = "q-pill " + (zr.can_enter ? "pill-green" : "pill-red");

        if (!zr.can_enter && zr.block_reason) {
          document.getElementById("cooldownBanner").innerHTML = `<div class="alert-box-warn" style="margin-bottom:10px;">🔒 ${zr.block_reason}</div>`;
        }

        document.getElementById("lotSimBox").innerHTML = `
          Simulasi <strong>1.00 Lot</strong> ($${data.usd_per_pip_1lot}/pip):
          SL <strong style="color:#f44336;">$${data.est_sl_usd_1lot}</strong> |
          TP <strong style="color:#00e676;">+$${data.est_tp_usd_1lot}</strong>
        `;
        updateActionGate();

        const np = data.news_prediction;
        if (np.has_event && np.release_ts_ms) {
          startNewsCountdown(np.release_ts_ms);
        }

        let newsHtml = "";
        if (np.has_event) {
          let predPill = np.prediction.includes("BULLISH") ? "pill-green" : (np.prediction.includes("BEARISH") ? "pill-red" : "pill-yellow");
          let slipWarn = np.slippage_warning ? `<div class="alert-box-warn">⚠️ High Slippage Risk: Berita rilis ${np.countdown}!</div>` : "";
          newsHtml = `
            <div class="q-card" style="border-color: rgba(0, 230, 118, 0.25);">
              <div class="q-card-head">
                <span>1. Pre-News Predictive Bot (${np.currency})</span>
                <span class="q-pill ${predPill}">${np.prediction}</span>
              </div>
              <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-main);">${np.title}</div>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
                Jadwal: <strong style="color:#ededed;">${np.release_wib}</strong> (${np.countdown}) • Forecast: <strong>${np.forecast}</strong> | Prev: <strong>${np.previous}</strong>
              </div>
              <div style="font-size: 0.8rem; color: #ccc; margin-top: 6px;">${np.reasoning}</div>
              ${slipWarn}
            </div>
          `;
        } else {
          newsHtml = `
            <div class="q-card">
              <div class="q-card-head">
                <span>1. Macro News Radar</span>
                <span class="q-pill pill-neutral">CLEAR</span>
              </div>
              <div style="font-size: 0.8rem; color: var(--text-muted);">${np.note}</div>
            </div>
          `;
        }

        const smc = data.smc;
        let smcPill = (smc.verdict === "OPTIMAL" || smc.verdict === "VALID") ? "pill-green" : (smc.verdict === "STRETCHED" ? "pill-yellow" : "pill-red");
        let idmColor = smc.idm_swept ? "#4caf50" : "#ffc107";

        let kzPill = data.killzone.is_weekend ? "pill-red" : (data.killzone.quality === "KILLZONE" ? "pill-green" : (data.killzone.quality === "SPREAD_RISK" ? "pill-red" : "pill-neutral"));
        let sweepHtml = `<div style="font-size: 0.79rem; color: #4caf50; margin-top: 8px;">✓ Posisi SL aman dari radius sweep likuiditas terdekat.</div>`;
        if (data.liquidity.sweep_alerts && data.liquidity.sweep_alerts.length > 0) {
          sweepHtml = data.liquidity.sweep_alerts.map(a => `<div class="alert-box-warn">⚠️ Sweep Risk: ${a}</div>`).join("");
        }

        let atrPill = data.volatility.status === "OPTIMAL" ? "pill-green" : (data.volatility.status === "STRETCHED" ? "pill-yellow" : "pill-red");
        let barWidth = Math.min(data.volatility.exhaustion_pct, 100);
        let barColor = data.volatility.exhaustion_pct >= 85 ? "#f44336" : (data.volatility.exhaustion_pct >= 65 ? "#ffc107" : "#00e676");

        let csmPill = data.strength.verdict === "ALIGNED" ? "pill-green" : (data.strength.verdict === "COUNTER" ? "pill-red" : "pill-neutral");
        let chipsHtml = data.strength.ranking.map(r => `<span class="csm-chip">${r.ccy} <strong>${r.score}</strong></span>`).join("");

        container.innerHTML = `
          ${newsHtml}

          <div class="q-card">
            <div class="q-card-head">
              <span>2. SMC Dealing Range (Fib 50%–75%)</span>
              <span class="q-pill ${smcPill}">${smc.zone}</span>
            </div>
            <div class="liq-grid">
              <div class="liq-box"><div class="liq-lbl">50% EQ</div><div class="liq-val">${smc.eq_50}</div></div>
              <div class="liq-box"><div class="liq-lbl">61.8% OTE</div><div class="liq-val">${smc.fib_618}</div></div>
              <div class="liq-box"><div class="liq-lbl">75.0% OTE</div><div class="liq-val">${smc.fib_750}</div></div>
            </div>
            <div style="font-size: 0.8rem; color: #ccc; margin-top: 8px;">${smc.note}</div>
            <div style="font-size: 0.79rem; color: ${idmColor}; margin-top: 4px;">${smc.idm_swept ? "✓" : "•"} ${smc.idm_note}</div>
          </div>

          <div class="q-card">
            <div class="q-card-head">
              <span>3. Liquidity Pool &amp; Killzone</span>
              <span class="q-pill ${kzPill}">${data.killzone.is_weekend ? "MARKET CLOSED" : data.killzone.zone_name}</span>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted);">
              Waktu Lokal: <strong style="color: var(--text-main);">${data.killzone.day_name}, ${data.killzone.wib_time}</strong>
            </div>
            <div class="liq-grid">
              <div class="liq-box"><div class="liq-lbl">PDH</div><div class="liq-val">${data.liquidity.pdh}</div></div>
              <div class="liq-box"><div class="liq-lbl">PWH</div><div class="liq-val">${data.liquidity.pwh}</div></div>
              <div class="liq-box"><div class="liq-lbl">Asian High</div><div class="liq-val">${data.liquidity.asian_high}</div></div>
              <div class="liq-box"><div class="liq-lbl">PDL</div><div class="liq-val">${data.liquidity.pdl}</div></div>
              <div class="liq-box"><div class="liq-lbl">PWL</div><div class="liq-val">${data.liquidity.pwl}</div></div>
              <div class="liq-box"><div class="liq-lbl">Asian Low</div><div class="liq-val">${data.liquidity.asian_low}</div></div>
            </div>
            ${sweepHtml}
          </div>

          <div class="q-card">
            <div class="q-card-head">
              <span>4. ATR(14) &amp; Daily Range Filter</span>
              <span class="q-pill ${atrPill}">${data.volatility.status}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.82rem;">
              <span>Hari Ini: <strong>${data.volatility.today_range_pips} pips</strong></span>
              <span>ATR-14: <strong>${data.volatility.atr_14_pips} pips</strong> (${data.volatility.exhaustion_pct}%)</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill" style="width: ${barWidth}%; background: ${barColor};"></div>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted);">${data.volatility.note}</div>
          </div>

          <div class="q-card">
            <div class="q-card-head">
              <span>5. Live Currency Strength (0–10)</span>
              <span class="q-pill ${csmPill}">${data.strength.verdict}</span>
            </div>
            <div class="csm-bar-row">
              <span><strong>${data.strength.base_ccy}</strong>: ${data.strength.base_score}/10</span>
              <span style="color:var(--text-muted); font-size:0.75rem;">VS</span>
              <span><strong>${data.strength.quote_ccy}</strong>: ${data.strength.quote_score}/10</span>
            </div>
            <div style="font-size: 0.79rem; color: #ccc; margin-top: 6px;">${data.strength.note}</div>
            <div class="csm-rank-strip">${chipsHtml}</div>
          </div>

          <div class="q-card">
            <div class="q-card-head">
              <span>6. Quantitative Historical Edge</span>
              <span class="q-pill pill-neutral">2Y DATA</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--text-main); margin-bottom: 4px;">
              Hari <strong>${data.seasonality.day_name}</strong> (${data.side}): <strong style="color: var(--neon-green);">${data.seasonality.day_winrate}%</strong> searah <span style="color:var(--text-muted); font-size:0.74rem;">(N=${data.seasonality.day_samples}, median ${data.seasonality.day_median_pips} pips)</span>
            </div>
            <div style="font-size: 0.82rem; color: var(--text-main);">
              Sesi <strong>${data.seasonality.session_name}</strong> (${data.side}): <strong style="color: var(--neon-green);">${data.seasonality.session_winrate}%</strong> searah <span style="color:var(--text-muted); font-size:0.74rem;">(N=${data.seasonality.session_samples}, median ${data.seasonality.session_median_pips} pips)</span>
            </div>
          </div>
        `;
      } catch (err) {
        container.innerHTML = `
          <div class="q-card">
            <div style="font-size: 0.82rem; color: #ff6b6b; margin-bottom: 10px;">
              Server Render sedang bangun dari mode sleep (cold start) atau tidak terjangkau: ${err.message}
            </div>
            <button type="button" class="btn btn-submit w-100" style="padding: 10px; font-size: 0.85rem;" onclick="runQuantFetch()">Muat Ulang Analisis</button>
          </div>
        `;
      }
    }

    function onApiConnected() {
      loadTopNewsBanner("{{ result.pair }}");
      runQuantFetch();
    }
    checkCorrelationGuard("{{ result.pair }}", "{{ result.side }}");
    runQuantFetch();
    {% else %}
    function onApiConnected() {
      loadTopNewsBanner(document.getElementById("pairInput").value);
    }
    {% endif %}
  </script>
</body>
</html>
"""


HTML_PORTFOLIO = """
<!DOCTYPE html>
<html lang="id">
<head>
  <link rel="manifest" href="/manifest.json">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ZIGFT Portfolio | Kalender PnL &amp; Equity Curve</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
  <style>{{ base_css | safe }}</style>
</head>
<body>
  <div class="container">
    <div class="top-nav">
      <div class="nav-tabs-wrap">
        <a href="/" class="nav-pill">Kalkulator &amp; Quant</a>
        <a href="/portfolio" class="nav-pill active">Kalender PnL &amp; Curve</a>
      </div>
      <button type="button" class="api-config-btn" onclick="openApiModal()">
        <span id="quantStatusDot" class="status-dot"></span>
        <span>Quant API</span>
      </button>
    </div>

    <div class="dashboard-card">
      <div class="header" style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; flex-wrap:wrap;">
        <div>
          <h3>Portofolio &amp; Kalender PnL</h3>
          <p>Auto-Settlement 00:00 WIB • Hapus Data Mentah +2 Jam</p>
          <div id="lastCheckStatus" style="font-size:0.75rem; color:var(--neon-green); margin-top:5px;">Menyiapkan koneksi...</div>
        </div>
        <div style="display:flex; gap:6px;">
          <button type="button" class="btn-neon" style="padding:9px 11px; font-size:0.76rem; white-space:nowrap;" onclick="openManualModal()">
            + Input Trade
          </button>
          <button type="button" id="btnCheckLive" class="btn-outline-custom" style="padding:9px 11px; font-size:0.76rem; white-space:nowrap;" onclick="loadPortfolio(true)">
            Cek Harga Live
          </button>
        </div>
      </div>

      <div id="portfolioBody">
        <div class="spinner-box">
          <div class="spinner-ring"></div>
          <div>Memuat Kalender PnL, Equity Curve &amp; Status Entry...</div>
        </div>
      </div>
    </div>

    <footer>© 2025 MaelFX × Idris Lab | 1.00 Lot Auto-Price Settlement Engine</footer>
  </div>

  <!-- MODAL INPUT TRADE LAMA (SUDAH TP/SL) ATAU MASIH BERJALAN -->
  <div id="manualTradeModal" class="modal-overlay">
    <div class="modal-container" style="height: auto; max-height: 92vh; overflow-y: auto; padding: 22px;">
      <div class="modal-header" style="padding: 0 0 14px 0;">
        <button class="close-modal-btn" onclick="closeManualModal()">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
        <h4>Input Trade Lampau / Berjalan</h4>
        <div style="width: 22px;"></div>
      </div>

      <div style="margin-top: 14px;">
        <div class="mb-2">
          <label class="form-label">Status Posisi Saat Ini</label>
          <select id="bfOutcome" class="form-select" onchange="toggleBfTimeField()">
            <option value="TP_HIT">Sudah TP (Masuk Kalender PnL Permanen)</option>
            <option value="SL_HIT">Sudah SL (Masuk Kalender &amp; Hitung Kuota SL)</option>
            <option value="OPEN">Masih Berjalan (Pantau dari Tanggal Entry)</option>
          </select>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px;" class="mb-2">
          <div>
            <label class="form-label">Pair</label>
            <select id="bfPair" class="form-select">
              <option value="XAUUSD">XAUUSD</option>
              <option value="EURUSD">EURUSD</option>
              <option value="GBPUSD">GBPUSD</option>
              <option value="AUDUSD">AUDUSD</option>
              <option value="NZDUSD">NZDUSD</option>
              <option value="USDJPY">USDJPY</option>
              <option value="USDCAD">USDCAD</option>
              <option value="USDCHF">USDCHF</option>
              <option value="EURGBP">EURGBP</option>
              <option value="EURJPY">EURJPY</option>
              <option value="GBPJPY">GBPJPY</option>
              <option value="AUDJPY">AUDJPY</option>
              <option value="NZDJPY">NZDJPY</option>
              <option value="CADJPY">CADJPY</option>
              <option value="CHFJPY">CHFJPY</option>
              <option value="EURNZD">EURNZD</option>
            </select>
          </div>
          <div>
            <label class="form-label">Side</label>
            <select id="bfSide" class="form-select">
              <option value="buy">Buy</option>
              <option value="sell">Sell</option>
            </select>
          </div>
        </div>

        <div class="mb-2">
          <label class="form-label">Entry Price</label>
          <input type="number" step="any" id="bfEntry" class="form-control" placeholder="contoh: 3544.74">
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px;" class="mb-2">
          <div>
            <label class="form-label">Stop Loss (SL)</label>
            <input type="number" step="any" id="bfSl" class="form-control" placeholder="harga SL">
          </div>
          <div>
            <label class="form-label">Take Profit (TP)</label>
            <input type="number" step="any" id="bfTp" class="form-control" placeholder="harga TP">
          </div>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px;" class="mb-3">
          <div>
            <label class="form-label">Tanggal Trade (WIB)</label>
            <input type="date" id="bfDate" class="form-control">
          </div>
          <div id="bfTimeWrap" style="display:none;">
            <label class="form-label">Jam Entry (WIB)</label>
            <input type="time" id="bfTime" class="form-control" value="08:00">
          </div>
        </div>

        <label class="gate-check">
          <input type="checkbox" id="bfIdm">
          <span><strong>Inducement (IDM)</strong> sudah tervalidasi</span>
        </label>
        <label class="gate-check">
          <input type="checkbox" id="bfLiq">
          <span><strong>Liquidity Pool / Sweep</strong> terkonfirmasi</span>
        </label>

        <div id="bfFeedback" style="font-size:0.79rem; margin:8px 0;"></div>

        <button type="button" id="btnSubmitManual" class="btn btn-neon w-100" onclick="submitManualTrade()">
          Simpan ke Portofolio &amp; Supabase
        </button>
      </div>
    </div>
  </div>

  {{ common_api_modal | safe }}

  <script>
    let portfolioData = null;
    let equityChart = null;
    let viewYear = new Date().getFullYear();
    let viewMonth = new Date().getMonth();

    const BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];

    function openManualModal() {
      const todayIso = new Date().toISOString().slice(0, 10);
      document.getElementById("bfDate").value = todayIso;
      document.getElementById("bfFeedback").innerText = "";
      toggleBfTimeField();
      document.getElementById("manualTradeModal").style.display = "flex";
    }
    function closeManualModal() {
      document.getElementById("manualTradeModal").style.display = "none";
    }
    function toggleBfTimeField() {
      const out = document.getElementById("bfOutcome").value;
      document.getElementById("bfTimeWrap").style.display = (out === "OPEN") ? "block" : "none";
    }

    async function submitManualTrade() {
      const apiBase = getQuantApiUrl();
      const fb = document.getElementById("bfFeedback");
      const btn = document.getElementById("btnSubmitManual");
      if (!apiBase) { openApiModal(); return; }

      btn.disabled = true;
      btn.innerText = "Menyimpan ke Supabase...";
      fb.style.color = "#ffc107";
      fb.innerText = "Memproses data & menyinkronkan ke kalender...";

      try {
        const resp = await fetch(`${apiBase}/api/entries/manual`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            outcome: document.getElementById("bfOutcome").value,
            pair: document.getElementById("bfPair").value,
            side: document.getElementById("bfSide").value,
            entry: parseFloat(document.getElementById("bfEntry").value || "0"),
            sl: parseFloat(document.getElementById("bfSl").value || "0"),
            tp: parseFloat(document.getElementById("bfTp").value || "0"),
            trade_date: document.getElementById("bfDate").value,
            trade_time: document.getElementById("bfTime").value,
            inducement_confirmed: document.getElementById("bfIdm").checked,
            liquidity_confirmed: document.getElementById("bfLiq").checked
          })
        });
        const data = await resp.json();
        if (!resp.ok || data.error) throw new Error(data.error || "Gagal menyimpan trade");

        fb.style.color = "#00e676";
        fb.innerText = "✓ " + data.message;
        setTimeout(() => {
          closeManualModal();
          loadPortfolio(false);
        }, 900);
      } catch (err) {
        fb.style.color = "#ff6b6b";
        fb.innerText = "✕ " + err.message;
      } finally {
        btn.disabled = false;
        btn.innerText = "Simpan ke Portofolio & Supabase";
      }
    }

    function formatSignedUsd(val) {
      const num = Number(val || 0);
      if (num > 0) return `+$${num.toFixed(0)}`;
      if (num < 0) return `-$${Math.abs(num).toFixed(0)}`;
      return "$0";
    }

    function changeMonth(delta) {
      viewMonth += delta;
      if (viewMonth > 11) { viewMonth = 0; viewYear++; }
      if (viewMonth < 0) { viewMonth = 11; viewYear--; }
      renderCalendarGrid();
    }

    function selectCalDay(dateStr) {
      const detailBox = document.getElementById("dayDetailBox");
      if (!portfolioData || !detailBox) return;
      const d = portfolioData.daily_pnl[dateStr];
      if (!d) {
        detailBox.innerHTML = `<div style="font-size:0.8rem; color:var(--text-muted);">Tanggal <strong>${dateStr}</strong>: Tidak ada transaksi terselesaikan.</div>`;
        return;
      }
      const listHtml = (d.trades || []).map(t => `
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; padding:4px 0; border-top:1px dashed #222;">
          <span><strong>${t.pair}</strong> ${t.side} (1:${t.rr}) • ${t.result}</span>
          <span style="color:${t.pnl_usd >= 0 ? '#00e676' : '#f44336'}; font-weight:600;">
            ${t.pnl_usd >= 0 ? '+' : '-'}$${Math.abs(t.pnl_usd).toFixed(2)} (${t.pnl_pips} pips)
          </span>
        </div>
      `).join("");

      detailBox.innerHTML = `
        <div style="font-size:0.82rem; font-weight:600; margin-bottom:6px;">
          Detail Permanen ${dateStr}: <span style="color:${d.pnl_usd >= 0 ? '#00e676' : '#f44336'};">${d.pnl_usd >= 0 ? '+' : '-'}$${Math.abs(d.pnl_usd).toFixed(2)}</span> (${d.wins}W / ${d.losses}L)
        </div>
        ${listHtml}
      `;
    }

    function renderCalendarGrid() {
      const grid = document.getElementById("pnlCalendarGrid");
      const title = document.getElementById("calMonthTitle");
      if (!grid || !title || !portfolioData) return;

      title.innerText = `${BULAN_ID[viewMonth]} ${viewYear}`;
      const firstDay = new Date(viewYear, viewMonth, 1).getDay();
      const mondayOffset = (firstDay + 6) % 7;
      const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();

      let html = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"].map(d => `<div class="cal-dow">${d}</div>`).join("");

      for (let i = 0; i < mondayOffset; i++) {
        html += `<div class="cal-cell empty"></div>`;
      }

      for (let day = 1; day <= daysInMonth; day++) {
        const mStr = String(viewMonth + 1).padStart(2, "0");
        const dStr = String(day).padStart(2, "0");
        const key = `${viewYear}-${mStr}-${dStr}`;
        const rec = portfolioData.daily_pnl[key];

        let cls = "cal-cell";
        let pnlTxt = "";
        if (rec) {
          cls += rec.pnl_usd >= 0 ? " profit" : " loss";
          pnlTxt = formatSignedUsd(rec.pnl_usd);
        }
        html += `
          <div class="${cls}" onclick="selectCalDay('${key}')">
            <span class="cal-day-num">${day}</span>
            <span class="cal-pnl-txt">${pnlTxt}</span>
          </div>
        `;
      }
      grid.innerHTML = html;
    }

    function renderEquityChart() {
      const canvas = document.getElementById("equityCanvas");
      if (!canvas || !portfolioData) return;
      const curve = portfolioData.equity_curve || [];
      const labels = curve.length ? curve.map(c => c.date.slice(5)) : ["Start"];
      const values = curve.length ? curve.map(c => c.cumulative_pnl) : [0];

      if (equityChart) equityChart.destroy();
      equityChart = new Chart(canvas.getContext("2d"), {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: "Cumulative PnL ($)",
            data: values,
            borderColor: "#00e676",
            backgroundColor: "rgba(0, 230, 118, 0.12)",
            borderWidth: 2,
            fill: true,
            tension: 0.25,
            pointRadius: 3,
            pointBackgroundColor: "#00e676"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: "#888", font: { size: 10 } }, grid: { color: "#1a1a1a" } },
            y: { ticks: { color: "#888", font: { size: 10 }, callback: v => "$" + v }, grid: { color: "#1a1a1a" } }
          }
        }
      });
    }

    async function loadPortfolio(forceCheck = false) {
      const container = document.getElementById("portfolioBody");
      const btn = document.getElementById("btnCheckLive");
      const statusEl = document.getElementById("lastCheckStatus");
      const apiBase = getQuantApiUrl();

      if (!apiBase) {
        container.innerHTML = `
          <div class="q-card">
            <div style="font-size:0.84rem; color:var(--text-muted); margin-bottom:10px;">
              Hubungkan URL Backend Render terlebih dahulu melalui tombol <strong>Quant API</strong> di pojok kanan atas.
            </div>
            <button type="button" class="btn btn-submit w-100" onclick="openApiModal()">Hubungkan URL Render</button>
          </div>
        `;
        return;
      }

      if (btn) {
        btn.disabled = true;
        btn.classList.add("is-loading");
        btn.innerHTML = `<span class="btn-mini-spin"></span> <span>${forceCheck ? "Cek Live..." : "Memuat..."}</span>`;
      }
      if (statusEl) {
        statusEl.style.color = "#ffc107";
        statusEl.innerText = forceCheck ? "⏳ Menarik candle M15 live dari Yahoo Finance..." : "⏳ Sinkronisasi data Supabase...";
      }

      try {
        const resp = await fetch(`${apiBase}/api/portfolio?force=${forceCheck ? "1" : "0"}`);
        const data = await resp.json();
        if (!resp.ok || data.error) throw new Error(data.error || "Gagal memuat portofolio");
        portfolioData = data;

        if (statusEl) {
          statusEl.style.color = "#00e676";
          statusEl.innerText = `✓ Terakhir dicek: ${data.checked_at_wib || data.server_wib}`;
        }

        const s = data.summary;
        const zr = data.zigft_rules;
        const netColor = s.net_pnl_usd >= 0 ? "#00e676" : "#f44336";

        let rawHtml = `<div style="font-size:0.8rem; color:var(--text-muted);">Tidak ada data mentah aktif (semua riwayat lama sudah diolah ke kalender &amp; dibersihkan otomatis).</div>`;
        if (data.raw_entries && data.raw_entries.length > 0) {
          rawHtml = data.raw_entries.map(e => {
            let pillCls = "pill-neutral";
            let statusTxt = "OPEN (PANTAU LIVE)";
            if (e.status === "TP_HIT") { pillCls = "pill-green"; statusTxt = `TP HIT (+$${e.pnl_usd})`; }
            if (e.status === "SL_HIT") { pillCls = "pill-red"; statusTxt = `SL HIT (-$${Math.abs(e.pnl_usd)})`; }

            let lifecycleNote = "Menunggu sentuhan harga TP/SL.";
            if (e.settled) {
              lifecycleNote = `✓ Sudah masuk Kalender PnL. Data mentah dihapus otomatis pukul <strong>${e.delete_after_wib}</strong> (+2 jam buffer).`;
            } else if (e.status !== "OPEN") {
              lifecycleNote = "Menunggu jam <strong>00:00 WIB</strong> untuk dipindahkan ke Kalender PnL permanen.";
            }

            return `
              <div style="padding:10px; border:1px solid #1e1e1e; border-radius:8px; margin-bottom:8px; background:#070707;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:0.88rem;">${e.pair} ${e.side.toUpperCase()} (1:${e.rr})</strong>
                  <span class="q-pill ${pillCls}">${statusTxt}</span>
                </div>
                <div style="font-size:0.76rem; color:var(--text-muted); margin-top:4px;">
                  Entry: ${e.entry} | SL: ${e.sl} | TP: ${e.tp} • Dicatat: ${e.created_wib}
                </div>
                <div style="font-size:0.75rem; color:#bbb; margin-top:4px;">${lifecycleNote}</div>
              </div>
            `;
          }).join("");
        }

        container.innerHTML = `
          <div class="result-grid" style="margin-bottom:14px;">
            <div class="data-item">
              <div class="data-label">Net PnL Permanen (1 Lot)</div>
              <div class="data-value" style="color:${netColor};">${s.net_pnl_usd >= 0 ? '+' : '-'}$${Math.abs(s.net_pnl_usd).toFixed(2)}</div>
            </div>
            <div class="data-item">
              <div class="data-label">Win Rate / Settled</div>
              <div class="data-value">${s.win_rate}% <span style="font-size:0.8rem; color:#888;">(${s.wins}W/${s.losses}L)</span></div>
            </div>
            <div class="data-item">
              <div class="data-label">Kuota SL Bulanan</div>
              <div class="data-value">${zr.monthly_sl_used} / ${zr.monthly_sl_max} SL</div>
            </div>
            <div class="data-item">
              <div class="data-label">Settlement Berikutnya</div>
              <div class="data-value" style="font-size:0.85rem;">${data.next_settlement_wib}</div>
            </div>
          </div>

          ${zr.cooldown_active ? `<div class="alert-box-warn" style="margin-bottom:14px;">🔒 ${zr.block_reason}</div>` : ""}

          <div class="q-card">
            <div class="q-card-head">
              <span>Equity Curve (Kumulatif Permanen)</span>
              <span class="q-pill pill-green">1.00 LOT BASIS</span>
            </div>
            <div style="height: 170px; width: 100%;">
              <canvas id="equityCanvas"></canvas>
            </div>
          </div>

          <div class="q-card">
            <div class="cal-header-bar">
              <button type="button" class="cal-nav-btn" onclick="changeMonth(-1)">‹</button>
              <strong id="calMonthTitle" style="font-size:0.92rem;"></strong>
              <button type="button" class="cal-nav-btn" onclick="changeMonth(1)">›</button>
            </div>
            <div class="cal-grid" id="pnlCalendarGrid"></div>
            <div id="dayDetailBox" style="margin-top:12px; padding-top:10px; border-top:1px solid #1e1e1e; font-size:0.78rem; color:var(--text-muted);">
              Ketuk kotak tanggal untuk melihat rincian profit/loss harian.
            </div>
          </div>

          <div class="q-card">
            <div class="q-card-head">
              <span>Riwayat Entry Mentah (Sementara)</span>
              <span class="q-pill pill-neutral">AUTO-PURGE +2J</span>
            </div>
            ${rawHtml}
          </div>
        `;

        renderEquityChart();
        renderCalendarGrid();
      } catch (err) {
        if (statusEl) {
          statusEl.style.color = "#ff6b6b";
          statusEl.innerText = `✕ Gagal cek: ${err.message}`;
        }
        container.innerHTML = `
          <div class="q-card">
            <div style="font-size:0.82rem; color:#ff6b6b; margin-bottom:10px;">Gagal memuat portofolio: ${err.message}</div>
            <button type="button" class="btn btn-submit w-100" onclick="loadPortfolio(false)">Coba Lagi</button>
          </div>
        `;
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.classList.remove("is-loading");
          btn.innerText = "Cek Harga Live";
        }
      }
    }

    function onApiConnected() { loadPortfolio(false); }
    loadPortfolio(false);
  </script>
</body>
</html>
"""

TF_RULES = {
    "NZDUSD": {"vp": 2, "min_sl": 10, "max_sl": 200},
    "AUDUSD": {"vp": 2, "min_sl": 10, "max_sl": 200},
    "EURGBP": {"vp": 2, "min_sl": 10, "max_sl": 200},
    "USDCHF": {"vp": 2, "min_sl": 10, "max_sl": 200},
    "USDCAD": {"vp": 1.5, "min_sl": 10, "max_sl": 200},
    "EURUSD": {"vp": 1.5, "min_sl": 10, "max_sl": 200},
    "GBPUSD": {"vp": 1.5, "min_sl": 10, "max_sl": 200},
    "NZDJPY": {"vp": 1.5, "min_sl": 15, "max_sl": 300},
    "CADJPY": {"vp": 1.5, "min_sl": 15, "max_sl": 300},
    "AUDJPY": {"vp": 1.5, "min_sl": 15, "max_sl": 300},
    "CHFJPY": {"vp": 1, "min_sl": 20, "max_sl": 400},
    "USDJPY": {"vp": 1, "min_sl": 20, "max_sl": 400},
    "EURJPY": {"vp": 1, "min_sl": 20, "max_sl": 400},
    "GBPJPY": {"vp": 1, "min_sl": 20, "max_sl": 400},
    "EURNZD": {"vp": 1, "min_sl": 20, "max_sl": 400},
    "XAUUSD": {"vp": 0.5, "min_sl": 30, "max_sl": 500},
}


def detect_pip_value(pair: str, entry: float):
    pair = pair.upper()
    if "XAU" in pair:
        return 0.1
    elif "JPY" in pair:
        return 0.01
    else:
        decimals = len(str(entry).split('.')[-1]) if '.' in str(entry) else 0
        return 0.0001 if decimals >= 4 else 0.01


def calculate_sl_tp(pair, side, entry, rr):
    pair = pair.upper()
    rule = TF_RULES.get(pair, {"vp": 1, "min_sl": 20, "max_sl": 200})
    pv = detect_pip_value(pair, entry)

    sl_pips = rule["max_sl"] / 3
    tp_pips = sl_pips * rr

    sl_distance = sl_pips * pv
    tp_distance = tp_pips * pv

    if side == "buy":
        sl = entry - sl_distance
        tp = entry + tp_distance
    else:
        sl = entry + sl_distance
        tp = entry - tp_distance

    valid = rule["min_sl"] <= sl_pips <= rule["max_sl"]
    validation_text = f"SL {rule['min_sl']}–{rule['max_sl']} pips | VP={rule['vp']}"

    return {
        "pair": pair,
        "side": side,
        "entry": entry,
        "sl": round(sl, 5),
        "tp": round(tp, 5),
        "sl_pips": round(sl_pips, 1),
        "tp_pips": round(tp_pips, 1),
        "rr": rr,
        "valid": valid,
        "value_pair": rule["vp"],
        "validation_text": validation_text
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        pair = request.form["pair"].upper().strip()
        side = request.form["side"].lower().strip()
        entry = float(request.form["entry"])
        rr = float(request.form["rr"])
        if 1 <= rr <= 3:
            result = calculate_sl_tp(pair, side, entry, rr)

    return render_template_string(
        HTML_CALCULATOR,
        result=result,
        tf_rules=TF_RULES,
        base_css=BASE_CSS,
        common_api_modal=COMMON_API_MODAL,
        default_quant_api=DEFAULT_QUANT_API,
    )


@app.route("/portfolio", methods=["GET"])
def portfolio():
    return render_template_string(
        HTML_PORTFOLIO,
        base_css=BASE_CSS,
        common_api_modal=COMMON_API_MODAL,
        default_quant_api=DEFAULT_QUANT_API,
    )


app = app
