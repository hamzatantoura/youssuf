from flask import Flask, request
import os
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import openai

# تحميل المتغيرات من .env
load_dotenv()

app = Flask(__name__)

# مفتاح OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    # تصنيف الرسالة وتوليد الرد
    try:
        reply = generate_smart_reply(incoming_msg)
    except Exception as e:
        reply = "صار خلل بسيط، جرب تبعتلنا من جديد بالله."

    msg.body(reply)
    return str(response)

def generate_smart_reply(message):
    system_prompt = """
    أنت مساعد ذكي وظيفتك ترد على استفسارات العملاء بخصوص منتج زيت الشعر باللهجة الليبية بطريقة مقنعة ومرتبة.
    مهمتك:
    1. فهم نية الزبون (استفسار، طلب، تردد).
    2. الرد بلغة بسيطة ومقنعة.
    3. طلب اسم المستلم، العنوان، ورقم الهاتف إذا حسيت إنه الزبون ناوي يشتري.

    ملاحظة: الزيت مخصص للرجال والنساء، يعالج التساقط، ويُستخدم ٣ مرات أسبوعيًا. سعره 120 دينار مع شحن مجاني.
    """
    prompt = f"{system_prompt}\n\nالرسالة من الزبون: {message}\n\nردك باللهجة الليبية:"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return completion.choices[0].message["content"].strip()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
