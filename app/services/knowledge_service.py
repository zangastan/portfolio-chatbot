from typing import List, Optional
from datetime import datetime
import io
from fastapi import UploadFile

from app.repositories.knowledge_repo import KnowledgeRepository
from app.models.knowledge import KnowledgeDocument
from app.core.database import supabase

class KnowledgeService:
    def __init__(self):
        self.repo = KnowledgeRepository(supabase)

    async def ingest_file(
        self,
        tenant_id: str,
        file: UploadFile,
        title: Optional[str] = None
    ) -> KnowledgeDocument:
        """
        Ingests a file, extracts text, and stores it in the knowledge base.
        """
        content = await self._parse_file(file)
        if not content:
            raise ValueError("Could not extract text from file")

        doc_title = title or file.filename

        # Store document
        doc = self.repo.create({
            "tenant_id": tenant_id,
            "title": doc_title,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        })

        return doc

    def add_document(
        self,
        tenant_id: str,
        title: str,
        content: str
    ) -> KnowledgeDocument:
        """
        Adds raw text as a document.
        """
        doc = self.repo.create({
            "tenant_id": tenant_id,
            "title": title,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        })

        return doc

    async def _parse_file(self, file: UploadFile) -> str:
        file_bytes = await file.read()
        content = ""

        # File parsing logic remains same as it only extracts text
        import pypdf
        import docx

        if file.content_type == "application/pdf":
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                content += (page.extract_text() or "") + "\n"

        elif file.content_type == ("application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            document = docx.Document(io.BytesIO(file_bytes))
            for para in document.paragraphs:
                content += para.text + "\n"

        elif file.content_type.startswith("text/"):
            content = file_bytes.decode("utf-8", errors="ignore")

        else:
            raise ValueError(f"Unsupported file type: {file.content_type}")

        return content.strip()

    def get_tenant_documents(self, tenant_id: str) -> List[KnowledgeDocument]:
        return self.repo.list_by_tenant(tenant_id)

    def search_context(self, tenant_id: str, query: str = "") -> str:
        """
        Fetches all knowledge base content for a tenant to be used as context.
        Query is ignored here as we provide full context to the AI.
        """
        documents = self.get_tenant_documents(tenant_id)
        
        if not documents:
            return ""

        context_parts = []
        for doc in documents:
            context_parts.append(f"Document Title: {doc.title}\nContent:\n{doc.content}")

        return "\n\n---\n\n".join(context_parts)

    def delete_document(self, doc_id: str) -> None:
        return self.repo.delete(doc_id)
