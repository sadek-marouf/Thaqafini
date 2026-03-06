from fastapi import FastAPI, UploadFile, File
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
import os
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import io

app = FastAPI()

# ==============================
# المتغيرات العالمية للمودلات
# ==============================

maternal_model = None
genetic_model = None
food_model = None
food_processor = None

# ==============================
# تحميل المودلات عند تشغيل السيرفر
# ==============================

@app.on_event("startup")
def load_models():
    global maternal_model, genetic_model, food_model, food_processor
    
    # تحميل موديل الأم
    try:
        if os.path.exists("random_forest_model.joblib"):
            maternal_model = joblib.load("random_forest_model.joblib")
            print("✅ Maternal model loaded successfully")
        else:
            print("❌ File 'random_forest_model.joblib' NOT found!")
    except Exception as e:
        print(f"❌ Error loading Maternal model: {e}")

    # تحميل موديل الوراثة
    try:
        model_name = "thaqafni_model.pkl"
        if os.path.exists(model_name):
            genetic_model = joblib.load(model_name)
            print(f"✅ Genetic model '{model_name}' loaded successfully")
        else:
            print(f"❌ File '{model_name}' NOT found!")
    except Exception as e:
        print(f"❌ Error loading Genetic model: {e}")

    # تحميل مودل التعرف على الطعام
    try:
        food_path = "food101"

        if os.path.exists(food_path):
            food_processor = AutoImageProcessor.from_pretrained(food_path)
            food_model = AutoModelForImageClassification.from_pretrained(food_path)

            print("✅ Food model loaded successfully")

        else:
            print("❌ Folder 'food101' NOT found!")

    except Exception as e:
        print(f"❌ Error loading Food model: {e}")

# ==============================
# نماذج البيانات
# ==============================

class MaternalInput(BaseModel):
    age: int
    systolic_bp: int
    diastolic_bp: int
    bs: float
    body_temp: float
    heart_rate: int

class GeneticInput(BaseModel):
    age: int
    family_history: int
    hemoglobin: float
    fetal_hemoglobin: float
    sweat_chloride: float
    sickled_rbc_percent: float

# ==============================
# الصفحة الرئيسية
# ==============================

@app.get("/")
def home():
    return {
        "status": "online",
        "maternal_model": "Ready" if maternal_model else "Not Loaded",
        "genetic_model": "Ready" if genetic_model else "Not Loaded",
        "food_model": "Ready" if food_model else "Not Loaded"
    }

# ==============================
# مودل مخاطر الأم
# ==============================

@app.post("/predict_maternal")
async def predict_maternal(data: MaternalInput):

    if not maternal_model:
        return {"error": "Maternal model is not available"}

    features = np.array([[ 
        data.age,
        data.systolic_bp,
        data.diastolic_bp,
        data.bs,
        data.body_temp,
        data.heart_rate
    ]])

    prediction = maternal_model.predict(features)

    return {
        "risk_level": int(prediction[0])
    }

# ==============================
# مودل الأمراض الوراثية
# ==============================

@app.post("/predict_genetic")
async def predict_genetic(data: GeneticInput):

    if not genetic_model:
        return {"error": "Genetic model is not available"}

    input_data = pd.DataFrame([[
        data.age,
        data.family_history,
        data.hemoglobin,
        data.fetal_hemoglobin,
        data.sweat_chloride,
        data.sickled_rbc_percent
    ]],
    columns=[
        'Age',
        'Family_History',
        'Hemoglobin',
        'Fetal_Hemoglobin',
        'Sweat_Chloride',
        'Sickled_RBC_Percent'
    ])

    prediction = genetic_model.predict(input_data)[0]

    probabilities = genetic_model.predict_proba(input_data)[0]
    confidence = float(np.max(probabilities) * 100)

    ar_map = {
        "Thalassemia": "ثلاسيميا",
        "Normal": "سليم - طبيعي",
        "Sickle Cell Anemia": "فقر الدم المنجلي",
        "Cystic Fibrosis": "تليف كيسي",
        "High Risk": "معرض لخطورة عالية"
    }

    return {
        "diagnosis": prediction,
        "diagnosis_ar": ar_map.get(prediction, "غير معروف"),
        "confidence": f"{confidence:.2f}%",
        "status": "success"
    }

# ==============================
# مودل التعرف على الطعام
# ==============================

@app.post("/predict_food")
async def predict_food(file: UploadFile = File(...)):

    if not food_model:
        return {"error": "Food model is not available"}

    try:
        image_bytes = await file.read()

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        inputs = food_processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = food_model(**inputs)

        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()

        food_name = food_model.config.id2label[predicted_class_id]

        return {
            "food_id": predicted_class_id,
            "food_name": food_name,
            "status": "success"
        }

    except Exception as e:
        return {
            "error": str(e)
        }