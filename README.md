# 🧠 Autonomous Product Catalog Cleaner & Manager

A production-grade application that uses LLMs to clean raw product catalog data, structure it, and provide an interface for viewing, updating, and managing product entries.

This project uses **LangChain + Groq LLMs** for intelligent field inference and **FastAPI + Streamlit** for full-stack interaction. The app is fully containerized using **Docker**.

---

## 🚀 Features

- 🧹 **Automatic product data cleaning** using LangGraph agents
- 📊 **Interactive dashboard** built with Streamlit
- 💾 **Database-backed storage** via SQLModel (SQLite by default)
- 📦 **View, search, edit, delete products**
- 🧠 Uses **LLM (Groq/Gemma)** to infer missing fields like brand, category, size
- 🐳 Fully containerized with Docker

---

## 🧱 Tech Stack

| Layer       | Tech                     |
|------------|--------------------------|
| LLM Agent   | LangGraph + Groq (Gemma) |
| Backend     | FastAPI (Pydantic v2)    |
| Frontend    | Streamlit                |
| ORM         | SQLModel (SQLite)        |
| Packaging   | Docker                   |
| Language    | Python 3.11+             |

---

## 🗂️ Project Structure
```
Autonomous-Product-Catalog-UsingDB/
├── backend/
│ ├── main.py # FastAPI app
│ ├── product_cleaner.py # LLM-powered cleaner
├── frontend/
│ └── app.py # Streamlit dashboard
├── models/
│ └── product_model.py # SQLModel database models
├── schemas/
│ └── schema.py # Pydantic schemas for validation
├── utils/
│ └── tools.py # JSON extraction helpers
├── Dockerfile # Unified backend + frontend Docker build
├── requirements.txt
└── README.md
```


## ⚙️ Setup Instructions

### ✅ Clone the Repo

```bash
git clone https://github.com/samanwaya938/Automomus-Product-Catalogue-Cleaning-System.git
cd Automomus-Product-Catalogue-Cleaning-System
```

## 🐳 Run with Docker

### 1️⃣ Build Docker Image

```bash
docker build -t (image_name):latest .
```

### 2️⃣ Run the Container

```bash
docker run -p 8000:8000 -p 8501:8501 --env GROQ_API_KEY="Your API Key" (image_name)
```

## 🌐 Access the App
| Service      | URL                                                      |
| ------------ | -------------------------------------------------------- |
| Backend Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Streamlit UI | [http://localhost:8501](http://localhost:8501)           |


## 🔌 API Endpoints
| Method | Endpoint                | Description                |
| ------ | ----------------------- | -------------------------- |
| POST   | `/clean-product`        | Clean a raw product row    |
| POST   | `/save-product`         | Save cleaned product to DB |
| GET    | `/products`             | Get all products           |
| GET    | `/product/{product_id}` | Get a specific product     |
| PUT    | `/product/{product_id}` | Update a specific product  |
| DELETE | `/product/{product_id}` | Delete a specific product  |

## 🧠 How It Works
Upload a CSV of raw product data via the Streamlit dashboard.

Each row is sent to the LLM cleaner agent via FastAPI.

Missing fields like brand, category, color are inferred.

Cleaned data is previewed and can be saved to a database.

Users can search, update, or delete entries using the UI.

## 📸 Screenshots (Add These)
![image](https://github.com/user-attachments/assets/29a5f076-320e-4513-a2f1-ffe0e9fb0a0b)
![image](https://github.com/user-attachments/assets/573ec62a-7848-4364-bff9-66971619dc5d)
![image](https://github.com/user-attachments/assets/62d2f4cb-5e0a-4e5d-b98d-a4ef2ee8af39)


## 🔒 Security & Future Work
 * Role-based access for viewers/editors

 * Vector-based RAG for document search

 * Integration with product APIs

 * Optional login + JWT protection

## 💡 Tips for Development
* Modify product_cleaner.py to enhance LLM prompts

* Change database from SQLite to Postgres by updating connection string in main.py

* Add unit tests for the cleaner agent and endpoints

* Use docker-compose.yml for multi-container setups (e.g., with Postgres)


## 📝 License
MIT © 2025

## 📬 Contact
GitHub: @samanwayaghosh938

Email: samanwayaghosh938@gmail.com

