from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import uuid
from werkzeug.utils import secure_filename

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Allow backend to import src/
sys.path.append(os.path.abspath(".."))

from src.search import RAGSearch
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore

app = Flask(__name__)
CORS(app)

# Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]  
)

# Base directory for uploads
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload PDF and build RAG
@app.route("/upload", methods=["POST"])
@limiter.limit("5 per minute")
def upload_report():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    report_id = str(uuid.uuid4())
    report_dir = os.path.join(UPLOAD_DIR, report_id)
    os.makedirs(report_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(report_dir, filename)
    file.save(file_path)

    docs = load_all_documents(report_dir)
    if not docs:
        return jsonify({
            "error": "Uploaded file does not appear to be a valid medical report"
        }), 400

    store = FaissVectorStore(persist_dir=report_dir)
    store.build_from_documents(docs)

    return jsonify({
        "report_id": report_id,
        "message": "Report uploaded and processed successfully"
    })

# Analyze report (deterministic)
@app.route("/analyze", methods=["GET"])
@limiter.limit("20 per minute")
def analyze():
    report_id = request.args.get("report_id")
    if not report_id:
        return jsonify({"error": "report_id is required"}), 400

    report_dir = os.path.join(UPLOAD_DIR, report_id)
    if not os.path.exists(report_dir):
        return jsonify({"error": "Invalid report_id"}), 404

    rag = RAGSearch(persist_dir=report_dir)
    results = rag.analyze_report()

    if not results:
        return jsonify({"error": "No analyzable lab data found"}), 404

    return jsonify({"results": results})


# Ask questions (LLM-based)
@app.route("/ask", methods=["POST"])
@limiter.limit("10 per minute")
def ask():
    data = request.json or {}
    question = data.get("question")
    report_id = data.get("report_id")

    if not question or not report_id:
        return jsonify({
            "error": "Both question and report_id are required"
        }), 400

    report_dir = os.path.join(UPLOAD_DIR, report_id)
    if not os.path.exists(report_dir):
        return jsonify({"error": "Invalid report_id"}), 404

    rag = RAGSearch(persist_dir=report_dir)
    answer = rag.search_and_summarize(question)

    return jsonify({"answer": answer})

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Backend running"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

