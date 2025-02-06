# 🚀 FastAPI Firestore Query Generator

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-46a2f1?style=for-the-badge)
![Flutter](https://img.shields.io/badge/Integrated%20with-Flutter-02569B?style=for-the-badge&logo=flutter)

A FastAPI-powered application that generates **Firestore query expressions** based on user input using **LangChain** and **Google Gemini AI**. The generated expressions can then be used dynamically to fetch product IDs from Firestore.

---

## 📌 Features
✅ Generate structured Firestore query expressions dynamically.  
✅ Uses **Google Gemini AI** to interpret user queries.  
✅ Secure execution with controlled query generation.  
✅ Firestore query building using structured AI-generated filters.  
✅ Limits data retrieval to **20** documents per query.  
✅ Deployed on **Railway** and integrated with **Flutter app**.  

---

## 🚀 Getting Started

### 🔹 1. Clone the Repository
```bash
git clone https://github.com/abdullah-khaled0/AI-Powered-Search-and-Recommendation-System.git
cd AI-Powered-Search-and-Recommendation-System
```

### 🔹 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 🔹 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 4. Set Up Firebase Credentials
1. **Go to Firebase Console** → Generate a service account key.
2. **Store it as an environment variable**:
   ```bash
   export FIREBASE_CREDENTIALS='{"type": "service_account", "project_id": "your-project" ... }'
   ```
   *(For Windows, use `set` instead of `export`.)*

---

## ⚡ Running the App

### 🚀 Start FastAPI Locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 📡 Test the API in Postman
Send a **POST request** to:
```
http://127.0.0.1:8000/generate-code
```
With the following JSON body:
```json
{
  "question": "Find all Samsung products."
}
```
Expected response:
```json
{
  "product_ids": ["12345", "67890", "54321"]
}
```

---

## 🚀 Deployment on Railway
### 🔹 Steps to Deploy
1. **Push your code to GitHub**.
2. **Go to Railway.app** → Create a **New Web Service**.
3. **Connect GitHub Repo** → Select **Docker** as runtime.
4. **Set Environment Variables**:
   ```
   FIREBASE_CREDENTIALS = {PASTE YOUR FIREBASE JSON AS A SINGLE LINE}
   ```
5. **Click Deploy** and get your API URL!

Your API will be available at:  
```
https://your-app-name.onrailway.app/generate-code
```

---

## 📲 Flutter Integration
The Railway API is integrated with a Flutter app to send requests and receive Firestore queries.


---

## 📜 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate-code` | Generate Firestore query expressions based on user input and fetch product IDs |
