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
    incoming_msg = request.form.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    try:
        system_prompt = """
أنت مساعد ذكي باللهجة الليبية، وظيفتك ترد على العملاء المهتمين بزيت شعر طبيعي اسمه "ميسال".
مهمتك:
- تفهم نية الزبون.
- تجاوب بطريقة مقنعة ومرتبة.
- إذا الزبون ناوي يطلب، اسأله على الاسم والعنوان ورقم الهاتف.
ملاحظة: الزيت يعالج التساقط، يستخدم 3 مرات في الأسبوع، وسعره 120 دينار مع شحن مجاني.
"""

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=200
        )

        reply = chat.choices[0].message["content"].strip()
        msg.body(reply)

    except Exception as e:
        print("OpenAI Error:", str(e))
        msg.body("صار خلل بسيط، جرب تبعتلنا من جديد بالله.")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
