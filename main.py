from flask import Flask, request
import os
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
أنت مساعد مبيعات ذكي باللهجة الليبية، تشتغل في شركة تبيع زيت شعر طبيعي اسمه "ميسال".

مهمتك:
- ترد بطريقة لبقة ومقنعة وباللهجة الليبية.
- تفهم نية الزبون (طلب، تردد، فضول، استفسار).
- إذا الزبون ناوي يشتري، اسأله بلطافة على:
  الاسم، العنوان، ورقم الهاتف.
- لا تكرر نفس الكلام بين الردود.
- لا تبين إنك روبوت، وتصرف كأنك موظف بشري.

معلومات المنتج:
- اسم المنتج: زيت شعر ميسال
- مناسب للرجال والنساء
- يعالج تساقط الشعر، يقوي البصيلات، ينبت الفراغات، يعطي لمعة وترطيب طبيعي
- يُستخدم 3 مرات في الأسبوع
- يُترك من 3 إلى 5 ساعات ثم يُغسل
- السعر: 120 دينار ليبي مع شحن مجاني خلال 3 أيام
- الدفع عند الاستلام

ردك لازم يكون مختصر ومقنع حسب كلام الزبون.
"""},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        reply = "صار خلل بسيط، جرب تبعتلنا من جديد بالله."

    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
