from langchain_core.documents import Document

from app.services.parsing.base_parser import BaseParser
from app.services.parsing.models import LegalDocumentNode


class StatuteParser(BaseParser):
    def parse(
        self,
        documents: list[Document],
    ) -> list[LegalDocumentNode]:
        return []