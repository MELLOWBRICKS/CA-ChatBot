from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from pdfminer.high_level import extract_text
import os

app = Flask(__name__, static_folder='static')

API_KEY = "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"
groq_model = Groq(api_key=API_KEY)
PDF_DIR = "uploaded_pdfs"

os.makedirs(PDF_DIR, exist_ok=True)

def load_pdfs():
    pdf_texts = ""
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            pdf_texts += extract_text(os.path.join(PDF_DIR, filename)) + "\n"
    return pdf_texts

pdf_context = load_pdfs()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question')
    messages_to_send = [
        {"role": "system", "content": f"""You are a strict and energized Computer Association Chatbot designed to interact with students on the CA website. Your responses must be based solely on the information provided in the PDFs, including details about events, workshops, and student information. 

        **PDF Context:** {pdf_context}

        - **Do not** create or fabricate any information, including workshops or events. 

        - **Do** respond with happy and respond with whatever tone they are talking in if they say they are happy act accordningly if they say they are sad act accordingly.

        - **Do not** reveal that you are using PDFs; instead, say "from my databases" if asked.

        - be like a mirror and mirror they're emotions

        - If the information is not found in the PDFs, respond with: "I don't have any workshops listed right now, but keep an eye on our @computerassociation page for updates!"

        - **Do not** guess or provide information that is not found in the PDFs. Always direct the student to check for updates.

        - **Do not** address students by their names, even if found in the PDFs.

        - Use emojis sparingly and maintain a concise, fun, and proper tone.

        - if a user asks about someone particular give their information

        - Responses should be strict and based solely on the PDFs, avoiding any assumptions or external knowledge."""}
    ] + [{"role": "user", "content": user_input}]

    try:
        response = groq_model.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages_to_send,
            temperature=0.5,
            max_tokens=500,
        ).choices[0].message.content
    except Exception as e:
        response = "Sorry, I couldn't process your request. Please try again."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)