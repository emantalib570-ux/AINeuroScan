from flask import Flask, request, jsonify, send_file
import re

app = Flask(__name__)

def scan_content(content):
    ai_phrases = ["delve", "comprehensive", "moreover", "in conclusion", "vibrant", "it is important to note"]
    found_text = [p for p in ai_phrases if p in content.lower()]
    
    is_code = any(kw in content for kw in ["def ", "import ", "function", "public class", "const "])
    ai_code_score = 0
    if is_code:
        if content.count("#") > 3 or content.count("//") > 3:
            ai_code_score = 2

    total_score = len(found_text) + ai_code_score

    if total_score >= 2:
        verdict = "⚠️ AI GENERATED"
        color = "text-danger"
    elif total_score == 1:
        verdict = "🟡 MIXED / UNCERTAIN"
        color = "text-warning"
    else:
        verdict = "✅ HUMAN GENERATED"
        color = "text-success"

    return {
        "verdict": verdict,
        "color_class": color,
        "links": len(re.findall(r'https?://[^\s]+', content)),   # better regex
        "is_code": "Yes" if is_code else "No",
        "score_detail": f"AI Markers Found: {len(found_text)}",
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    content = data.get('content', '')
    result = scan_content(content)
    return jsonify(result)

@app.route('/', methods=['GET'])
def homepage():
    return send_file('index.html')

if __name__ == "__main__":
    app.run(debug=True)