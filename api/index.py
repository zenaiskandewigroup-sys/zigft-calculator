from flask import Flask, render_template_string, request

app = Flask(__name__)

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
    ]


HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
  <link rel="manifest" href="/manifest.json">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trader Family Auto Price v9.0</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #000000;
      --bg-card: #0a0a0a;
      --border: #222222;
      --border-focus: #444444;
      --text-main: #ededed;
      --text-muted: #888888;
      --accent: #ffffff;
      --accent-hover: #e0e0e0;
    }
    body { 
      background-color: var(--bg-main); 
      color: var(--text-main); 
      font-family: 'Inter', sans-serif; 
      min-height: 100vh; 
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 15px;
    }
    .container { max-width: 520px; width: 100%; }
    .dashboard-card { 
      background: var(--bg-card); 
      border: 1px solid var(--border); 
      border-radius: 12px; 
      padding: 32px; 
      box-shadow: 0 8px 30px rgba(0,0,0,0.6); 
    }
    .header { margin-bottom: 28px; }
    .header h3 { 
      color: var(--text-main); 
      font-weight: 700; 
      font-size: 1.4rem; 
      margin-bottom: 6px; 
      display: flex; 
      align-items: center; 
      gap: 10px;
    }
    .header p { 
      color: var(--text-muted); 
      font-size: 0.85rem; 
      font-weight: 400; 
      margin: 0; 
    }
    .form-label { 
      color: var(--text-muted) !important; 
      font-weight: 500; 
      font-size: 0.85rem;
      margin-bottom: 8px;
    }
    .form-control, .form-select { 
      background-color: var(--bg-main) !important; 
      border: 1px solid var(--border) !important; 
      color: var(--text-main) !important; 
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 0.95rem;
      transition: all 0.2s ease;
    }
    .form-control:focus, .form-select:focus { 
      border-color: var(--border-focus) !important; 
      box-shadow: 0 0 0 3px rgba(255,255,255,0.05) !important; 
    }
    .form-control::placeholder { color: #444 !important; }
    .btn-submit { 
      background: var(--accent); 
      color: #000; 
      font-weight: 600; 
      border: none; 
      font-size: 0.95rem; 
      padding: 14px;
      border-radius: 8px;
      transition: all 0.2s ease;
      margin-top: 10px;
    }
    .btn-submit:hover { 
      background: var(--accent-hover); 
      transform: translateY(-1px);
    }
    .result-wrapper { 
      margin-top: 24px; 
      background: var(--bg-card); 
      border: 1px solid var(--border); 
      border-radius: 12px; 
      padding: 24px; 
    }
    .result-header {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid var(--border);
    }
    .result-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    .data-item {
      background: var(--bg-main);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }
    .data-label {
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }
    .data-value {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text-main);
    }

    /* TAMBAHAN: tombol salin */
    .copy-btn {
      margin-top: 10px;
      width: 100%;
      padding: 7px 10px;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: #111111;
      color: #888888;
      font-size: 0.75rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .copy-btn:hover {
      background: #1a1a1a;
      color: #ededed;
      border-color: #444444;
    }

    .copy-btn.copied {
      color: #4caf50;
      border-color: rgba(76, 175, 80, 0.3);
    }

    .status-badge {
      margin-top: 20px;
      padding: 14px;
      border-radius: 8px;
      font-weight: 500;
      font-size: 0.9rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .status-valid {
      background: rgba(40, 167, 69, 0.1);
      color: #4caf50;
      border: 1px solid rgba(40, 167, 69, 0.2);
    }
    .status-invalid {
      background: rgba(220, 53, 69, 0.1);
      color: #f44336;
      border: 1px solid rgba(220, 53, 69, 0.2);
    }
    footer { margin-top: 32px; text-align: center; font-size: 0.8rem; color: #555; }
  </style>
</head>
<body>
  <div class="container">
    <div class="dashboard-card">
      <div class="header">
        <h3>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06-.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
          Auto Price v9.0
        </h3>
        <p>RR Smart Mode | TF Official System 2025 | Auto Value Pair</p>
      </div>
      <form method="POST">
        <div class="mb-3">
          <label class="form-label">Pair</label>
          <input type="text" name="pair" class="form-control" placeholder="contoh: XAUUSD / AUDUSD / USDJPY" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Side</label>
          <select name="side" class="form-select" required>
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>
        <div class="mb-3">
          <label class="form-label">Entry Price</label>
          <input type="number" step="any" name="entry" class="form-control" placeholder="contoh: 4060.52 atau 0.65352" required>
        </div>
        <div class="mb-3">
          <label class="form-label">RR (1 - 3)</label>
          <input type="number" step="0.1" name="rr" class="form-control" placeholder="contoh: 2.5" required>
        </div>
        <button type="submit" class="btn btn-submit w-100">Hitung SL/TP</button>
      </form>
    </div>

    {% if result %}
    <div class="result-wrapper">
      <div class="result-header">Hasil Perhitungan</div>
      <div class="result-grid">
        <div class="data-item">
          <div class="data-label">Pair</div>
          <div class="data-value">{{ result.pair }}</div>
        </div>
        <div class="data-item">
          <div class="data-label">Side / RR</div>
          <div class="data-value">{{ result.side.upper() }} <span style="font-size: 0.9rem; color: #888;">(1:{{ result.rr }})</span></div>
        </div>

        <div class="data-item">
          <div class="data-label">Entry</div>
          <div class="data-value">{{ result.entry }}</div>
          <button type="button" class="copy-btn" onclick="copyPrice('{{ result.entry }}', this)">Salin Entry</button>
        </div>

        <div class="data-item">
          <div class="data-label">Value Pair</div>
          <div class="data-value">{{ result.value_pair }}</div>
        </div>

        <div class="data-item" style="border-color: rgba(244, 67, 54, 0.3);">
          <div class="data-label" style="color: #f44336;">Stop Loss (SL)</div>
          <div class="data-value">{{ result.sl }} <span style="font-size: 0.8rem; color: #888; font-weight: 400;">(-{{ result.sl_pips }} pips)</span></div>
          <button type="button" class="copy-btn" onclick="copyPrice('{{ result.sl }}', this)">Salin SL</button>
        </div>

        <div class="data-item" style="border-color: rgba(76, 175, 80, 0.3);">
          <div class="data-label" style="color: #4caf50;">Take Profit (TP)</div>
          <div class="data-value">{{ result.tp }} <span style="font-size: 0.8rem; color: #888; font-weight: 400;">(+{{ result.tp_pips }} pips)</span></div>
          <button type="button" class="copy-btn" onclick="copyPrice('{{ result.tp }}', this)">Salin TP</button>
        </div>
      </div>
      
      {% if result.valid %}
        <div class="status-badge status-valid">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          Valid TF 2025 ({{ result.validation_text }})
        </div>
      {% else %}
        <div class="status-badge status-invalid">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
          Tidak Valid TF 2025 ({{ result.validation_text }})
        </div>
      {% endif %}
    </div>
    {% endif %}

    <footer>© 2025 MaelFX × Idris Lab | TF 2025 System Integrated</footer>
  </div>

  <!-- TAMBAHAN: fungsi copy harga -->
  <script>
    function copyPrice(value, button) {
      navigator.clipboard.writeText(value).then(function() {
        const originalText = button.innerText;

        button.innerText = "✓ Tersalin";
        button.classList.add("copied");

        setTimeout(function() {
          button.innerText = originalText;
          button.classList.remove("copied");
        }, 1500);
      }).catch(function() {
        const textArea = document.createElement("textarea");
        textArea.value = value;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);

        const originalText = button.innerText;

        button.innerText = "✓ Tersalin";
        button.classList.add("copied");

        setTimeout(function() {
          button.innerText = originalText;
          button.classList.remove("copied");
        }, 1500);
      });
    }
  </script>
</body>
</html>
"""

# Data resmi TF 2025
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

    # ==========================================
    # LOGIKA XAUUSD: SL TETAP DI ~166.66 pips (max_sl / 3),
    # TP MENGIKUTI KELIPATAN RR (1x, 2x, 3x dari SL)
    # ==========================================
    if pair == "XAUUSD":
        sl_pips = rule["max_sl"] / 3  # Menghasilkan ~166.66 pips
        tp_pips = sl_pips * rr        # RR 1 -> 1x SL, RR 2 -> 2x SL, RR 3 -> 3x SL
            
    # ==========================================
    # LOGIKA ORIGINAL: UNTUK PAIR LAINNYA
    # ==========================================
    else:
        sl_pips = rule["max_sl"] / rr
        if sl_pips < rule["min_sl"]:
            sl_pips = rule["min_sl"]
        if sl_pips > rule["max_sl"]:
            sl_pips = rule["max_sl"]

        tp_pips = sl_pips * rr

    # Jarak pips ke value harga
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
    return render_template_string(HTML, result=result)

app = app
