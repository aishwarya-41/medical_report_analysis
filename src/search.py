import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.vectorstore import FaissVectorStore
from src.data_loader import load_all_documents
from src.analyze import extract_lab_results


load_dotenv()


class RAGSearch:
    def __init__(
        self,
        persist_dir: str = "faiss_store",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "llama-3.1-8b-instant",
    ):
        self.project_root = Path(__file__).resolve().parents[1]
        self.data_dir = self.project_root / "data"
        self.persist_dir = self.project_root / persist_dir

        self.vectorstore = FaissVectorStore(
            persist_dir=str(self.persist_dir),
            embedding_model=embedding_model,
        )

        faiss_path = self.persist_dir / "faiss.index"
        meta_path = self.persist_dir / "metadata.pkl"

        if faiss_path.exists() and meta_path.exists():
            print("[INFO] Loading existing FAISS index...")
            self.vectorstore.load()
        else:
            print("[INFO] No FAISS index found. Building from documents...")
            docs = load_all_documents(str(self.data_dir))

            if not docs:
                raise RuntimeError(
                    f"No documents found in {self.data_dir}. Cannot build vector store."
                )

            self.vectorstore.build_from_documents(docs)

   
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment variables")

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=llm_model,
            temperature=0.1,
        )

        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def analyze_report(self):
        """
        Return structured lab results with normal/out-of-range status.
        """
        texts = [
            meta.get("text", "")
            for meta in self.vectorstore.metadata
            if meta
        ]

        if not texts:
            return []

        results = extract_lab_results(texts)

        unique = {}
        for r in results:
            unique[r["test"]] = r

        return list(unique.values())

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        if not query.strip():
            return "Query cannot be empty."

        print(f"[INFO] RAG query: {query}")

        results = self.vectorstore.query(query, top_k=top_k)

        texts = [
            r["metadata"].get("text", "")
            for r in results
            if r.get("metadata")
        ]

        if not texts:
            return "No relevant information found in the report."

        context = "\n\n".join(texts)

        prompt = f"""
You are a medical report analysis assistant.

STRICT RULES:
- You may ONLY answer questions that ask for:
  • exact lab values
  • normal reference ranges
  • whether a value is within or outside the normal range
   Explain what a test is (definition)
- You MUST NOT:
  • interpret results
  • explain causes
  • assess risk
  • give medical advice
  • suggest treatments
- If a question asks for interpretation, impact, risk, or advice,
  you MUST reply with:
  "I can only report values from the medical report. Please consult a healthcare professional for medical interpretation."

Use ONLY the provided context.
Do NOT use external medical knowledge.
Do NOT guess.

Question:
{query}

Context:
{context}

Answer:
"""


        response = self.llm.invoke(prompt)
        return response.content.strip()


if __name__ == "__main__":
    rag = RAGSearch()
    answer = rag.search_and_summarize("What is the haemoglobin level?")
    print("\nAnswer:\n", answer)
