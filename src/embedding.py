from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import re
from src.data_loader import load_all_documents


class EmbeddingPipeline:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(model_name)
        print(f"[INFO] Loaded embedding model: {model_name}")


    def normalize_medical_tables(self, text: str) -> str:
        """
        Convert CBC-style table rows into explicit sentences.
        Handles patterns like:
        HAEMOGLOBIN 12.1 g/dL 12-15
        """

        lines = [l.strip() for l in text.split("\n") if l.strip()]
        normalized_lines = []

        row_pattern = re.compile(
            r"^([A-Z][A-Z\s\.\(\)]+)\s+([\d\.]+)\s*([a-zA-Z/%\.]+)\s+([\d\-–\.]+)"
        )

        for line in lines:
            match = row_pattern.match(line)
            if match:
                test, value, unit, ref = match.groups()
                sentence = (
                    f"The {test.lower()} level is {value} {unit}. "
                    f"The normal reference range is {ref}."
                )
                normalized_lines.append(sentence)
            else:
                normalized_lines.append(line)

        return " ".join(normalized_lines)

    def preprocess_documents(self, documents: List[Any]) -> List[Any]:
        """
        Apply table-to-text normalization on each document.
        """
        for doc in documents:
            doc.page_content = self.normalize_medical_tables(doc.page_content)
        return documents

    def chunk_documents(self, documents: List[Any]) -> List[Any]:
        documents = self.preprocess_documents(documents)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

        chunks = splitter.split_documents(documents)
        print(f"[INFO] Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks

    def embed_chunks(self, chunks: List[Any]) -> np.ndarray:
        texts = [chunk.page_content for chunk in chunks]
        print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"[INFO] Embeddings shape: {embeddings.shape}")
        return embeddings


if __name__ == "__main__":
    docs = load_all_documents("data")
    emb_pipe = EmbeddingPipeline()
    chunks = emb_pipe.chunk_documents(docs)
    embeddings = emb_pipe.embed_chunks(chunks)
    print("[INFO] Example chunk:", chunks[0].page_content if chunks else None)
