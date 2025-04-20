from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    classification, reply = generate_smart_reply(incoming_msg)
    msg.body(reply)
    return str(resp)

def generate_smart_reply(message):
    try:
        system_prompt = f"""
أنت مساعد ذكي تتحدث باللهجة الليبية، هدفك فهم العميل وبيع زيت شعر يعالج التساقط. إذا طلب، اسأله على اسمه ورقمه وعنوانه.
الرسالة: {message}
الرد:
        """

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=200
        )

        reply = completion.choices[0].message["content"].strip()
        return "طلب جديد", reply
    except Exception as e:
        return "خطأ", "صار خلل بسيط، جرب تبعتلنا من جديد بالله."

if __name__ == "__main__":
    app.run(debug=True)
