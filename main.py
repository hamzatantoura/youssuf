from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body")
    response = MessagingResponse()
    msg = response.message()
    classification = classify_message(incoming_msg)
    reply = generate_reply(classification, incoming_msg)
    msg.body(reply)
    return str(response)

def classify_message(message):
    prompt = f"""صنف النص التالي بناءً على حالته (طلب جديد، استفسار عام، دعم فني، غير مصنف):\nالنص: {message}\nالتصنيف:""" 
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return "غير مصنف"

def generate_reply(classification, message):
    if "طلب جديد" in classification:
        return "تمام 🌟، توا هنكمل معاك طلبك. ممكن تبعتلنا اسمك، رقمك، والعنوان؟"
    elif "استفسار عام" in classification:
        return "أكيد! شن استفسارك؟ 🌿"

    elif "دعم فني" in classification:
        return "ما تقلقش ✨، بلغنا المشكلة اللي تواجهك وإن شاء الله نلقوا حل."
    else:
        return "معليش، مش فاهمينك كويس. ممكن توضح شني اللي تبيه؟"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
