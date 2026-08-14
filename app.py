import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Groq Free AI client setup with your verified key
client = Groq(api_key="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")

SYSTEM_INSTRUCTION = """
Tu ek world-class Python Teaching Expert AI hai. Tera naam 'Code with Harshit' hai.
Tujhe sikhane ka tareeka bilkul aasan, dosto wala, aur SIRF Desi Hindi me hona chahiye (English words ka use bilkul mat kar, technical terms jaise 'Variable', 'Loop' ko chhod kar baaki sab Hindi me bol).
Rules:
1. Agar koi puche ki tujhe kisne banaya hai, toh hamesha garv se bolna: "Mujhe ek genius AI Coder, Harshit Prajapat ne banaya hai!"
2. Sirf Python coding, errors, aur programming concepts par focus kar.
3. Agar 'Desi Mode' ON ho, toh thoda mazaakiya aur roast style me pyaar se Desi Hindi me samjha.
"""

@app.route("/")
def home():
    return render_template("code_with_harshit.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_msg = request.form.get("msg")
    desi_mode = request.form.get("desi") == "true"
    
    try:
        current_system_prompt = SYSTEM_INSTRUCTION
        if desi_mode:
            current_system_prompt += "\n[Note: Desi Mode is ON. Use funny and roasting Desi Hindi examples like a close friend.]"

        # Groq ka lightning-fast real AI call
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": current_system_prompt},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        reply = completion.choices[0].message.content

    except Exception as e:
        reply = f"Bhai AI brain se connect hone me error aa raha hai: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
