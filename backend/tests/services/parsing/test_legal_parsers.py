from langchain_core.documents import Document

from app.services.parsing.constitution_parser import ConstitutionParser
from app.services.parsing.models import LegalNodeType
from app.services.parsing.statute_parser import StatuteParser


def test_constitution_parser_captures_article_context_and_body() -> None:
    documents = [
        Document(
            page_content="""PART III\nCHAPTER I\nArticle 21. Protection of life and personal liberty\nNo person shall be deprived of his life or personal liberty except according to procedure established by law.""",
            metadata={"source": "constitution.pdf", "page": 42},
        )
    ]

    nodes = ConstitutionParser().parse(documents)

    assert len(nodes) == 1
    article = nodes[0]
    assert article.number == "21"
    assert article.title == "Protection of life and personal liberty"
    assert article.content == (
        "No person shall be deprived of his life or personal liberty except "
        "according to procedure established by law."
    )
    assert article.metadata["part"] == "PART III"
    assert article.metadata["chapter"] == "CHAPTER I"
    assert article.metadata["source_page"] == 42


def test_constitution_parser_accepts_numbered_article_headings() -> None:
    documents = [
        Document(
            page_content="22. Protection against arrest\nNo person shall be detained.",
            metadata={"source": "constitution.pdf", "page": 43},
        )
    ]

    nodes = ConstitutionParser().parse(documents)

    assert [(node.number, node.title, node.content) for node in nodes] == [
        ("22", "Protection against arrest", "No person shall be detained.")
    ]


def test_statute_parser_builds_section_subsection_and_clause_hierarchy() -> None:
    documents = [
        Document(
            page_content="""3. Power to issue directions\nThe Central Government may issue directions.\n(1) It may issue directions for carrying out this Act.\n(a) directions may specify conditions;\n(b) directions may specify time limits.""",
            metadata={"source": "sample_act.txt"},
        )
    ]

    nodes = StatuteParser().parse(documents)

    assert [node.node_type for node in nodes] == [
        LegalNodeType.SECTION,
        LegalNodeType.SUBSECTION,
        LegalNodeType.CLAUSE,
        LegalNodeType.CLAUSE,
    ]
    section, subsection, first_clause, second_clause = nodes
    assert section.title == "Power to issue directions"
    assert "Central Government" in section.content
    assert subsection.parent == section.id
    assert subsection.content == "It may issue directions for carrying out this Act."
    assert first_clause.parent == subsection.id
    assert second_clause.metadata["section"] == "3"
