from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("API_KEY_GROQ")

client = OpenAI(api_key=api_key,  base_url="https://api.groq.com/openai/v1")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods = ['Post'])
def ask():
    question = request.form.get("question")

    response = client.responses.create(
            model = 'meta-llama/llama-4-scout-17b-16e-instruct',
            input = [
                {'role' : 'system', 'content' : 'Act like a AI Personal Asistant'},
                {'role' : 'user', 'content' : question}
            ],
            temperature = 0.5,
            max_output_tokens = 512
        )
    answer = response.output_text.strip()
    return jsonify({"response" : answer}), 200 # Status code 200 (No problem)


@app.route("/summarize", methods = ['Post'])
def summarize():
    email_text = request.form.get("email")
    prompt = f"Summarize the following email in 2-3 sentences : {email_text}"

    response = client.responses.create(
            model = 'openai/gpt-oss-120b',
            input = [
                {'role' : 'system', 'content' : 'Act ike an expert email assistant'},
                {'role' : 'user', 'content' : prompt} 
            ],
            temperature = 0.2,
            max_output_tokens = 512
        )
    
    summary = response.output_text.strip()
    return jsonify({"response" : summary}), 200 # Status code 200 (No problem)


if __name__ == "__main__":
    app.run(debug=True)