from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trader Family Auto Price v9.0</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: linear-gradient(to bottom, #0a0a0a, #1a1a1a); color: #f8f8f8; font-family: 'Poppins', sans-serif; min-height: 100vh; }
    .container { max-width: 520px; margin-top: 40px; }
    .card { background: #111; border: 1px solid #222; border-radius: 16px; padding: 22px; box-shadow: 0 0 10px rgba(0,255,128,0.1); }
    h3 { color: #28a745; text-align: center; font-weight: 700; margin-bottom: 5px; }
    p.text-center { color: #00bfff; font-weight: 500; margin-bottom: 15px; }
    label.form-label { color: #fff !important; font-weight: 500; }
    input, select { background-color: #222 !important; border: 1px solid #444; color: #fff !important; }
    input::placeholder { color: #aaa !important; }
    .btn-success { background: linear-gradient(to right, #00c853, #009624); font-weight: 600; border: none; font-size: 16px; box-shadow: 0 0 6px rgba(0,255,128,0.4); }
    .btn-success:hover { background: linear-gradient(to right, #00e676, #00c853); }
    .result-card { background: #f9f9f9; color: #000; border-radius: 16px; padding: 18px; margin-top: 25px; box-shadow: 0 0 12px rgba(0,255,128,0.2); }
    footer { margin-top: 40px; text-align: center; font-size: 13px; color: #999; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h3>⚙️ Trader Family Auto Price v9.0</h3>
      <p class="text-center">RR Smart Mode | TF Official System 2025 | Auto Value Pair</p>
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
        <button type="submit" class="btn btn-success w-100">Hitung SL/TP ✅</button>
      </form>
    </div>

    {% if result %}
    <div class="result-card">
      <h5 class="fw-bold text-center mb-3">📊 Hasil Perhitungan</h5>
      <p><strong>PAIR :</strong> {{ result.pair }}</p>
      <p><strong>TYPE :</strong> {{ result.side.upper() }}</p>
      <p><strong>ENTRY :</strong> {{ result.entry }}</p>
      <p><strong>SL :</strong> {{ result.sl }} (-{{ result.sl_pips }} pips)</p>
      <p><strong>TP :</strong> {{ result.tp }} (+{{ result.tp_pips }} pips)</p>
      <p><strong>RR :</strong> 1 : {{ result.rr }}</p>
      <p><strong>Value Pair :</strong> {{ result.value_pair }}</p>
      {% if result.valid %}
        <div class="alert alert-success text-center fw-bold mt-3" role="alert">
          ✅ Valid TF 2025 ({{ result.validation_text }})
        </div>
      {% else %}
        <div class="alert alert-danger text-center fw-bold mt-3" role="alert">
          ⚠️ Tidak Valid TF 2025 ({{ result.validation_text }})
        </div>
      {% endif %}
    </div>
    {% endif %}

    <footer>© 2025 MaelFX × Idris Lab | TF 2025 System Integrated</footer>
  </div>
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

    # SL minimum → RR dikalkulasi otomatis
    sl_pips = rule["max_sl"] / rr
    if sl_pips < rule["min_sl"]:
        sl_pips = rule["min_sl"]
    if sl_pips > rule["max_sl"]:
        sl_pips = rule["max_sl"]

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
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)

