from dotenv import load_dotenv
import os
import anthropic
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    diagnosis = None
    
    if request.method == "POST":
        user_input = request.form["error_input"]
        
        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            system="You are an expert debugging assistant. When given an error or code problem, you diagnose what is wrong and give a clear, step by step fix. Be specific and practical.",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        diagnosis = message.content[0].text
    
    return render_template("index.html", diagnosis=diagnosis)

if __name__ == "__main__":
    app.run(debug=True)