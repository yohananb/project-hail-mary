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
    error_type = None
    
    if request.method == "POST":
        user_input = request.form["error_input"].strip()

        if not user_input:
            return render_template("index.html", diagnosis="Please enter a valid error message or question before submitting.")

        classification = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=50,
            system='You are classifier. Look at what the user submitted and respond with ONLY one of these words: "TERMINAL_ERROR", "CODE_BUG", "CONFIG_ISSUE", "GENERAL_QUESTION". Nothing else, just the one word.',
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        error_type = classification.content[0].text.strip()

        prompts = {
            "TERMINAL_ERROR": "You are an expert at diagnosing terminal errors. The user has a terminal error. Identify exactly what caused it and give numbered steps to fix it.",
            "CODE_BUG": "You are an expert debugger. The user has a code bug. Explain what the bug is, why it happens, and show the corrected code.",
            "CONFIG_ISSUE": "You are an expert at configuration and environment setup. The user has a configuration issue. Give clear steps to resolve it.",
            "GENERAL_QUESTION": "You are a helpful coding assistant. Answer the user's coding question clearly and with examples."
        }

        system_prompt = prompts.get(error_type, "You are an expert debugging assistant. Help the user with their problem.")



        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        diagnosis = message.content[0].text
    
    return render_template("index.html", diagnosis=diagnosis, error_type=error_type)

if __name__ == "__main__":
    app.run(debug=True)