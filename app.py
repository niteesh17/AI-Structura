from flask import Flask, render_template, request, jsonify
import requests
import graphviz
import re
from config import GOOGLE_GEMINI_API_KEY

app = Flask(__name__)

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_GEMINI_API_KEY}"



def generate_textual_diagram(code):
    """Sends code to Google Gemini API and extracts Graphviz DOT code."""
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"Convert the following code into a Graphviz DOT format diagram. Output only valid Graphviz DOT code:\n{code}"}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            ai_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return extract_graphviz_code(ai_text)  # Extract only Graphviz DOT syntax
        except KeyError:
            return "Error: Unexpected response format from AI"
    
    return f"Error: {response.status_code} - {response.text}"

def extract_graphviz_code(ai_response):
    """Extracts Graphviz DOT code from AI output."""
    match = re.search(r"```dot\n(.*?)\n```", ai_response, re.DOTALL)
    return match.group(1) if match else ai_response  # Return extracted code or fallback

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "No code provided"}), 400

    dot_code = generate_textual_diagram(code)
    
    try:
        dot = graphviz.Source(dot_code, format="svg")
        svg_data = dot.pipe(format='svg').decode('utf-8')
        return jsonify({"diagram": svg_data, "dot_code": dot_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

