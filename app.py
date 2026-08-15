import os
import sys
import tempfile
import subprocess

from flask import Flask, render_template, request, jsonify
from groq import Groq


app = Flask(__name__)

# =========================================================
# 🔐 GROQ SETUP
# =========================================================
# Local CMD:
#   Windows PowerShell: $env:GROQ_API_KEY="your-key"
#   CMD: set GROQ_API_KEY=your-key
#
# Render:
#   Dashboard -> Environment -> GROQ_API_KEY
#
# Never put the real API key inside GitHub code.

GROQ_API_KEY = os.environ.get("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")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY nahi mili. Environment variable set karo."
    )

client = Groq(api_key=GROQ_API_KEY)


# =========================================================
# 🧠 AI INSTRUCTION
# =========================================================

SYSTEM_INSTRUCTION = """
Tu "Code With Harshit" hai — ek friendly Python Teaching AI.

Student ko beginner-friendly Hindi/Hinglish mein samjha.
Programming ke technical terms English mein rakh sakta hai.

Main focus:
- Python
- Programming
- Errors
- Debugging
- Flask
- Web Development
- Games
- Real Projects

Teaching style:
1. Concept simple language mein bata.
2. Chhota example de.
3. Code de.
4. Code ko line-by-line samjha.
5. Real project mein use bata.
6. Zarurat ho to practice task de.

Student beginner ho to unnecessary advanced concepts se confuse mat kar.

Agar student pooche "Tujhe kisne banaya?"
toh bolo:
"Mujhe Harshit ne banaya hai! 😎"

Desi Mode ON ho to friendly Desi style aur light comedy use kar,
lekin explanation clear aur respectful rakho.
"""


MODE_INSTRUCTIONS = {
    "teacher": """
Teacher Mode:
Concept ko beginner-friendly examples ke saath samjha.
""",
    "debugger": """
Debugger Mode:
1. Problem kya hai
2. Error kyu aa raha hai
3. Correct code
4. Kya change hua
5. Future mein kaise avoid kare
""",
    "practice": """
Practice Mode:
Student ko coding challenge do.
Student ne attempt nahi kiya ho to pehle hint do,
complete solution turant mat do.
""",
    "game": """
Game Builder Mode:
Python games ko step-by-step practical projects ke through sikha.
""",
    "web": """
Web Development Mode:
Python + Flask + HTML + CSS ke through real websites banana sikha.
"""
}


# =========================================================
# 🏠 HOME
# =========================================================

@app.route("/")
def home():
    return render_template("code_with_harshit.html")


# =========================================================
# 🤖 AI CHAT
# =========================================================

@app.route("/get_response", methods=["POST"])
def get_response():

    user_msg = request.form.get("msg", "").strip()
    desi_mode = request.form.get("desi", "false").lower() == "true"
    mode = request.form.get("mode", "teacher")

    if not user_msg:
        return jsonify({
            "success": False,
            "reply": "Bhai pehle kuch likh toh 😂"
        }), 400

    mode_instruction = MODE_INSTRUCTIONS.get(
        mode,
        MODE_INSTRUCTIONS["teacher"]
    )

    desi_instruction = ""

    if desi_mode:
        desi_instruction = """
DESI MODE ON hai.
Close dost ki tarah simple Desi Hindi mein samjha.
Light funny examples use kar, lekin explanation useful rakho.
"""

    system_prompt = (
        SYSTEM_INSTRUCTION
        + "\n\nCURRENT MODE:\n"
        + mode_instruction
        + "\n\n"
        + desi_instruction
    )

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )

        reply = completion.choices[0].message.content

        return jsonify({
            "success": True,
            "reply": reply,
            "mode": mode
        })

    except Exception as e:

        print("GROQ ERROR:", str(e))

        return jsonify({
            "success": False,
            "reply": (
                "Bhai AI brain se connect hone mein "
                "problem aa gayi 😅 Thodi der baad try kar."
            )
        }), 500


# =========================================================
# 🐍 LOCAL PYTHON RUNNER
# =========================================================
# IMPORTANT:
# This endpoint is intended for local/private learning.
# Do NOT expose arbitrary Python execution publicly without
# a real sandbox/container isolation layer.

@app.route("/run_code", methods=["POST"])
def run_code():

    code = request.form.get("code", "").strip()

    if not code:
        return jsonify({
            "success": False,
            "output": "Bhai pehle Python code likh 😄"
        })

    temp_file = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout

        if result.stderr:
            output += result.stderr

        if not output.strip():
            output = (
                "✅ Code successfully run hua!"
                if result.returncode == 0
                else "❌ Python code mein error aaya."
            )

        return jsonify({
            "success": result.returncode == 0,
            "output": output.strip()
        })

    except subprocess.TimeoutExpired:

        return jsonify({
            "success": False,
            "output": (
                "⏱️ Code 5 seconds se zyada chal raha hai. "
                "Infinite loop ho sakta hai."
            )
        })

    except Exception as e:

        print("PYTHON RUNNER ERROR:", str(e))

        return jsonify({
            "success": False,
            "output": f"❌ Error: {str(e)}"
        })

    finally:

        if temp_file:
            try:
                os.remove(temp_file)
            except OSError:
                pass


# =========================================================
# ❤️ HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "app": "Code With Harshit",
        "ai": "Groq",
        "python_runner": "enabled"
    })


# =========================================================
# 🚀 START
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    print()
    print("==========================================")
    print("       CODE WITH HARSHIT 🚀")
    print("==========================================")
    print(f"Server: http://127.0.0.1:{port}")
    print("AI: Groq")
    print("Python Runner: ON")
    print("==========================================")
    print()

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
