import os, sqlite3, json, datetime
from flask import Flask, request, jsonify, render_template, g, abort
from rules import triage

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "cases.db")

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute("""CREATE TABLE IF NOT EXISTS cases(
            id INTEGER PRIMARY KEY AUTOINCREMENT, created TEXT, village TEXT, age INTEGER,
            days INTEGER, transcript TEXT, level TEXT, flags TEXT, summary TEXT, lang TEXT)""")
    return g.db

@app.teardown_appcontext
def close(_):
    d = g.pop("db", None)
    if d: d.close()

def llm_summary(transcript, result, age, days, lang):
    """Optional. LLM only WRITES the explanation; triage level comes from rules.py."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    names = {"en": "English", "hi": "Hindi", "mr": "Marathi"}
    flags = ", ".join(f["id"] for f in result["flags"]) or "none"
    if not key:
        return f"Triage {result['level'].upper()}. Flags: {flags}. Age {age or '?'}, {days or '?'} day(s). Report: {transcript}"
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        r = c.messages.create(
            model="claude-sonnet-4-6", max_tokens=300,
            messages=[{"role": "user", "content":
                f"Write a 3-line referral note for a doctor in {names.get(lang,'English')}. "
                f"Triage level (fixed, do not change): {result['level']}. Flags: {flags}. "
                f"Age: {age}. Days sick: {days}. Health worker report: {transcript}. "
                "Do not diagnose. Do not invent facts."}])
        return r.content[0].text
    except Exception as e:
        return f"(AI summary unavailable) Triage {result['level']}. Report: {transcript}"

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/triage")
def api_triage():
    d = request.get_json(force=True)
    text = (d.get("text") or "").strip()
    if not text:
        return jsonify(error="Say or type the symptoms first."), 400
    lang = d.get("lang", "en")
    age = int(d["age"]) if str(d.get("age", "")).isdigit() else None
    days = int(d["days"]) if str(d.get("days", "")).isdigit() else None
    result = triage(text, age, days, lang)
    summary = llm_summary(text, result, age, days, lang)
    cur = db().execute(
        "INSERT INTO cases(created,village,age,days,transcript,level,flags,summary,lang) VALUES(?,?,?,?,?,?,?,?,?)",
        (datetime.datetime.now().isoformat(timespec="seconds"), d.get("village", ""), age, days, text,
         result["level"], json.dumps([f["id"] for f in result["flags"]]), summary, lang))
    db().commit()
    result.update(id=cur.lastrowid, summary=summary)
    return jsonify(result)

@app.get("/api/stats")
def stats():
    rows = db().execute("SELECT level, COUNT(*) n FROM cases GROUP BY level").fetchall()
    by_village = db().execute(
        "SELECT village, COUNT(*) n FROM cases WHERE village!='' GROUP BY village ORDER BY n DESC LIMIT 5").fetchall()
    return jsonify(levels={r["level"]: r["n"] for r in rows}, villages=[dict(r) for r in by_village])

@app.get("/referral/<int:cid>")
def referral(cid):
    c = db().execute("SELECT * FROM cases WHERE id=?", (cid,)).fetchone()
    if not c: abort(404)
    return render_template("referral.html", c=c, flags=json.loads(c["flags"]))

if __name__ == "__main__":
    app.run(debug=True)
