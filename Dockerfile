# استخدام نسخة بايثون رسمية
FROM python:3.9

# تحديد مجلد العمل داخل السيرفر
WORKDIR /code

# نسخ ملف المتطلبات أولاً لتسريع التحميل
COPY ./requirements.txt /code/requirements.txt

# تثبيت المكتبات
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# نسخ باقي ملفات المشروع (بما فيها الموديلات)
COPY . .

# تشغيل FastAPI باستخدام Uvicorn على المنفذ 7860 (الافتراضي لهجنغ فيس)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
