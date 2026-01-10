
# Medical Report Analyzer Web Application

A full-stack AI-powered web application that analyzes uploaded medical reports (PDFs), extracts lab values, highlights abnormal results, and allows users to ask natural language questions about their report using Retrieval-Augmented Generation (RAG).

---

## Table of Contents

* Overview
* Features
* Screenshots
* System Architecture
* Model Details
* Tech Stack
* Setup Instructions
* Usage
* Limitations
* Future Enhancements
* Contributing
* License

---

## Overview

The **Medical Report Analyzer** is a web application designed to simplify understanding of medical lab reports. Users can upload a PDF medical report, automatically extract lab values, identify out-of-range parameters, and ask questions related to the uploaded report.

The application uses a **RAG pipeline** combining vector embeddings, FAISS similarity search, and a large language model (Groq LLaMA) to answer user queries strictly based on the uploaded report content.

This project focuses on:

* Practical AI integration
* Document understanding
* Medical data visualization
* End-to-end full-stack deployment

---

## Features

* **PDF Upload & Processing**
  Upload medical reports securely for analysis.

* **Automatic Lab Extraction**
  Extracts lab test names, values, reference ranges, and status (Normal / Out of Range).

* **Out-of-Range Highlighting**
  Color-coded display of abnormal values for quick visual understanding.

* **Toggle View**
  Switch between:

  * All results
  * Only out-of-range results

* **Ask Questions (RAG)**
  Users can ask natural language questions such as:

  * *“What is my haemoglobin level?”*
  * *“Which values are abnormal?”*

* **Fast Semantic Search**
  Uses vector embeddings + FAISS for relevant context retrieval.

* **Context-Restricted Answers**
  The model answers strictly based on uploaded report content (no hallucination).

* **Responsive UI**
  Mobile-friendly interface with clean UX.

---

## Screenshots

<img width="1352" height="950" alt="image" src="https://github.com/user-attachments/assets/03de2ee1-6ab3-4309-a70f-2b91d5124650" />
<br/>
<br/>

<img width="3014" height="1456" alt="image" src="https://github.com/user-attachments/assets/7613c1ed-d687-4141-89ce-798af7d17508" />
<br/>
<br/>

<img width="3018" height="1616" alt="image" src="https://github.com/user-attachments/assets/18265ef7-fe90-45b1-94d2-b4cd50904818" />
<br/>
<br/>

<img width="3014" height="1366" alt="image" src="https://github.com/user-attachments/assets/8fa66b79-79f6-4ba5-9ebd-22b3ddf7c290" />
<br/>
<br/>

---

## System Architecture

1. **Frontend (React)**

   * Uploads PDF
   * Displays extracted lab table
   * Toggle filtering
   * Question interface

2. **Backend (Flask API)**

   * Receives PDF
   * Extracts text from PDF
   * Builds FAISS vector index per report
   * Performs deterministic lab extraction
   * Handles RAG-based queries

3. **AI Pipeline**

   * Sentence Transformers → Embeddings
   * FAISS → Similarity search
   * Groq LLaMA → Answer generation

---

## Model Details

* **Embedding Model:**
  `all-MiniLM-L6-v2` (Sentence Transformers)

* **Vector Store:**
  FAISS (local vector index)

* **LLM:**
  Groq – `llama-3.1-8b-instant`

* **Approach:**
  Retrieval-Augmented Generation (RAG)

* **Answer Policy:**

  * Answers only from retrieved context
  * No external medical advice or assumptions

---

## Tech Stack

### Frontend

* React (Vite)
* CSS (Responsive UI)
* Axios

### Backend

* Flask
* Flask-CORS
* Flask-Limiter (rate limiting)
* LangChain
* FAISS
* Sentence Transformers
* PyMuPDF / PyPDF
* Python-dotenv

### Infrastructure

* Local FAISS vector storage per uploaded report
* REST APIs

---

## Setup Instructions

1. Clone the Repository <br>

```bash 
git clone https://github.com/<your-username>/medical_report_analysis.git
cd medical_report_analysis
```


2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```


3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```


4. Configure Environment Variables

Create a `.env` file in project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```


5. Run Backend Server

```bash
cd backend
python app.py
```

Backend will run at:

```
http://127.0.0.1:5000
```


6. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

## Usage

1. Open the web app in your browser.
2. Upload a medical report PDF.
3. View:

   * Extracted lab values
   * Normal vs Out-of-Range status
4. Use toggle to filter abnormal values.
5. Navigate to **Ask Page** and ask questions about the report.
6. Receive AI-generated answers based strictly on your report.

---

## Limitations

* Not a medical diagnostic tool.
* Answers are informational only.
* Large PDFs may increase memory usage.
* No persistent user history or authentication.

---

## Future Enhancements

* User authentication
* Report history dashboard
* Downloadable analysis summary
* Cloud vector storage
* Improved medical NLP extraction
* Multi-report comparison
* Deployment optimization

---

## Contributing

Contributions and improvements are welcome!

If you'd like to:

* Improve extraction accuracy
* Optimize performance
* Enhance UI
* Add new features

Feel free to fork the repository and submit a pull request.

---

## License

Distributed under the MIT License.

---


