import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src import rag_logger
from src.multi_source_rag import SupportDeskRAG


class SupportDeskRAGTests(unittest.TestCase):
    def test_retrieves_docs_and_forum_for_refund_question(self):
        rag = SupportDeskRAG()
        result = rag.ask("A forum says refunds are 30 days. Which refund period is correct?")
        source_types = {source["type"] for source in result["sources"]}
        self.assertIn("docs", source_types)
        self.assertIn("forum", source_types)
        self.assertIn("14", result["answer"])

    def test_detects_refund_contradiction(self):
        rag = SupportDeskRAG()
        result = rag.ask("A forum says refunds are 30 days. Which refund period is correct?")
        self.assertTrue(result["contradictions"])
        self.assertEqual(result["contradictions"][0]["claim"], "refund_period_days")

    def test_logs_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "rag.jsonl"
            with patch.object(rag_logger, "LOG_PATH", log_path):
                rag = SupportDeskRAG()
                rag.ask("How long is a password reset link valid?")
            log_text = log_path.read_text(encoding="utf-8")
            self.assertIn("sources_used", log_text)
            self.assertIn("password reset", log_text.lower())

    def test_unknown_question_has_non_empty_fallback(self):
        rag = SupportDeskRAG()
        result = rag.ask("Tell me about quantum banana policy")
        self.assertIn("could not find enough", result["answer"].lower())


if __name__ == "__main__":
    unittest.main()
