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

    classification, reply = generate_smart_reply(incoming_msg)
    msg.body(reply)
    return str(response)

def generate_smart_reply(message):
    system_prompt = """
    أنت مساعد ذكي باللهجة الليبية، تشتغل مع بزنس يبيع زيت شعر طبيعي اسمه "ميسال".
    مهمتك ترد على العملاء، وتقنعهم بطريقة ذكية بالشراء، وتصنف نيتهم (طلب - استفسار - دعم - غير معروف).
    لو حسّيت إن الزبون جدي، اطلب منه اسمه، رقم هاتفه، وعنوانه لتكمل الطلب.
    لا تكرر نفس الجمل، وكون لطيف وقريب من الزبون.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300
        )
        reply = chat.choices[0].message.content.strip()
        return "جاري المعالجة", reply
    except Exception as e:
        return "مشكلة", "صار خلل بسيط، جرب تبعتلنا من جديد بالله."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
