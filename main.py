from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
import os

app = FastAPI()

# 1. تعريف المتغيرات عالمياً
maternal_model = None
genetic_model = None

# 2. تحميل الموديلات عند تشغيل السيرفر
@app.on_event("startup")
def load_models():
    global maternal_model, genetic_model
    
    # تحميل موديل الأم
    try:
        if os.path.exists("random_forest_model.joblib"):
            maternal_model = joblib.load("random_forest_model.joblib")
            print("✅ Maternal model loaded successfully")
        else:
            print("❌ File 'random_forest_model.joblib' NOT found!")
    except Exception as e:
        print(f"❌ Error loading Maternal model: {e}")

    # تحميل موديل الوراثة (تم تعديل الاسم هنا)
    try:
        model_name = "thaqafni_model.pkl" # اسم الموديل الجديد
        if os.path.exists(model_name):
            genetic_model = joblib.load(model_name)
            print(f"✅ Genetic model '{model_name}' loaded successfully")
        else:
            print(f"❌ File '{model_name}' NOT found!")
    except Exception as e:
        print(f"❌ Error loading Genetic model: {e}")

# --- نماذج البيانات (Pydantic Models) ---

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

# --- نقاط الاتصال (Endpoints) ---

@app.get("/")
def home():
    return {
        "status": "online",
        "maternal_model": "Ready" if maternal_model else "Not Loaded",
        "genetic_model": "Ready" if genetic_model else "Not Loaded"
    }

@app.post("/predict_maternal")
async def predict_maternal(data: MaternalInput):
    if not maternal_model:
        return {"error": "Maternal model is not available"}
    
    features = np.array([[data.age, data.systolic_bp, data.diastolic_bp, data.bs, data.body_temp, data.heart_rate]])
    prediction = maternal_model.predict(features)
    return {"risk_level": int(prediction[0])}

@app.post("/predict_genetic")
async def predict_genetic(data: GeneticInput):
    if not genetic_model:
        return {"error": "Genetic model is not available"}

    # تحويل البيانات إلى DataFrame بنفس أسماء الأعمدة المستخدمة في التدريب
    input_data = pd.DataFrame([[
        data.age, 
        data.family_history, 
        data.hemoglobin, 
        data.fetal_hemoglobin, 
        data.sweat_chloride, 
        data.sickled_rbc_percent
    ]], columns=['Age', 'Family_History', 'Hemoglobin', 'Fetal_Hemoglobin', 'Sweat_Chloride', 'Sickled_RBC_Percent'])
    
    # تصحيح: استخدمي genetic_model بدلاً من model
    prediction = genetic_model.predict(input_data)[0]
    
    # تصحيح: حساب الاحتمالات من الـ genetic_model
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