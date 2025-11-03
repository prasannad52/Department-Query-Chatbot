from flask import Flask, render_template, request, jsonify
from chatbot.nlp_utils import preprocess_text, detect_intent
from chatbot.response_generator import generate_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_message = request.json["message"]
    tokens = preprocess_text(user_message)
    intent = detect_intent(user_message)
    reply = generate_response(intent, tokens)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
