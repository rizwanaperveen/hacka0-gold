"""Summarization Skill - Text summarization and content extraction."""

import logging
from typing import Dict, Any, List, Optional
import re


class SummarizationSkill:
    """Skill for summarizing text, extracting key points, and generating insights."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("SummarizationSkill")
        self.max_summary_length = config.get("max_summary_length", 500)

    def summarize_text(
        self,
        text: str,
        max_length: int = None,
        style: str = "concise"
    ) -> Dict[str, Any]:
        """
        Summarize a block of text.

        Args:
            text: Text to summarize
            max_length: Maximum length of summary (words)
            style: Summary style ('concise', 'detailed', 'bullet')

        Returns:
            Dictionary with summary and metadata
        """
        try:
            max_length = max_length or self.max_summary_length

            self.logger.info(f"Summarizing text ({len(text)} chars) in {style} style")

            # Simple extractive summarization (in production, use NLP models)
            sentences = self._split_sentences(text)
            important_sentences = self._extract_important_sentences(sentences, max_length)

            if style == "bullet":
                summary = self._format_as_bullets(important_sentences)
            else:
                summary = " ".join(important_sentences)

            return {
                "status": "success",
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text) if text else 0,
                "style": style
            }

        except Exception as e:
            self.logger.error(f"Failed to summarize text: {str(e)}")
            return {"status": "error", "error": str(e)}

    def extract_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """
        Extract key points from text.

        Args:
            text: Text to analyze
            num_points: Number of key points to extract

        Returns:
            List of key points
        """
        try:
            self.logger.info(f"Extracting {num_points} key points")

            sentences = self._split_sentences(text)
            scored_sentences = self._score_sentences(sentences)

            # Get top N sentences
            top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:num_points]
            key_points = [sent[0] for sent in top_sentences]

            return key_points

        except Exception as e:
            self.logger.error(f"Failed to extract key points: {str(e)}")
            return []

    def summarize_conversation(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Summarize a conversation or chat thread.

        Args:
            messages: List of message dicts with 'sender' and 'text' keys

        Returns:
            Conversation summary
        """
        try:
            self.logger.info(f"Summarizing conversation with {len(messages)} messages")

            # Extract participants
            participants = set(msg.get("sender") for msg in messages)

            # Combine all messages
            full_text = " ".join(msg.get("text", "") for msg in messages)

            # Summarize
            summary_result = self.summarize_text(full_text, style="concise")

            return {
                "status": "success",
                "summary": summary_result.get("summary"),
                "participants": list(participants),
                "message_count": len(messages),
                "key_topics": self._extract_topics(full_text)
            }

        except Exception as e:
            self.logger.error(f"Failed to summarize conversation: {str(e)}")
            return {"status": "error", "error": str(e)}

    def summarize_document(
        self,
        document: str,
        include_sections: bool = True
    ) -> Dict[str, Any]:
        """
        Summarize a long document with section analysis.

        Args:
            document: Full document text
            include_sections: Whether to include section summaries

        Returns:
            Document summary with sections
        """
        try:
            self.logger.info("Summarizing document")

            # Overall summary
            overall = self.summarize_text(document, style="detailed")

            result = {
                "status": "success",
                "overall_summary": overall.get("summary"),
                "word_count": len(document.split()),
                "key_points": self.extract_key_points(document, num_points=5)
            }

            if include_sections:
                sections = self._detect_sections(document)
                result["sections"] = sections

            return result

        except Exception as e:
            self.logger.error(f"Failed to summarize document: {str(e)}")
            return {"status": "error", "error": str(e)}

    def generate_tldr(self, text: str, max_words: int = 50) -> str:
        """
        Generate a TL;DR (Too Long; Didn't Read) summary.

        Args:
            text: Text to summarize
            max_words: Maximum words in TL;DR

        Returns:
            TL;DR string
        """
        try:
            sentences = self._split_sentences(text)
            if not sentences:
                return ""

            # Get the most important sentence
            scored = self._score_sentences(sentences)
            best_sentence = max(scored, key=lambda x: x[1])[0]

            # Truncate if needed
            words = best_sentence.split()
            if len(words) > max_words:
                best_sentence = " ".join(words[:max_words]) + "..."

            return f"TL;DR: {best_sentence}"

        except Exception as e:
            self.logger.error(f"Failed to generate TL;DR: {str(e)}")
            return ""

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting (in production, use NLTK or spaCy)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _score_sentences(self, sentences: List[str]) -> List[tuple]:
        """Score sentences by importance."""
        scored = []
        for sentence in sentences:
            # Simple scoring based on length and keyword presence
            score = len(sentence.split())

            # Boost score for sentences with important keywords
            important_words = ['important', 'key', 'critical', 'essential', 'must', 'should']
            for word in important_words:
                if word in sentence.lower():
                    score += 10

            scored.append((sentence, score))

        return scored

    def _extract_important_sentences(self, sentences: List[str], max_length: int) -> List[str]:
        """Extract most important sentences up to max length."""
        scored = self._score_sentences(sentences)
        sorted_sentences = sorted(scored, key=lambda x: x[1], reverse=True)

        result = []
        total_words = 0

        for sentence, score in sorted_sentences:
            words = len(sentence.split())
            if total_words + words <= max_length:
                result.append(sentence)
                total_words += words
            else:
                break

        return result

    def _format_as_bullets(self, sentences: List[str]) -> str:
        """Format sentences as bullet points."""
        return "\n".join(f"• {sentence}" for sentence in sentences)

    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from text."""
        # Simple topic extraction (in production, use NLP)
        words = text.lower().split()
        word_freq = {}

        for word in words:
            if len(word) > 5:  # Only consider longer words
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top 5 most frequent words as topics
        topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        return [topic[0] for topic in topics]

    def _detect_sections(self, document: str) -> List[Dict[str, str]]:
        """Detect sections in a document."""
        # Simple section detection based on headers
        lines = document.split('\n')
        sections = []
        current_section = None
        current_content = []

        for line in lines:
            # Detect headers (lines that are short and possibly capitalized)
            if len(line) < 100 and line.isupper() or line.startswith('#'):
                if current_section:
                    sections.append({
                        "title": current_section,
                        "summary": self.summarize_text(" ".join(current_content), max_length=100).get("summary", "")
                    })
                current_section = line.strip('#').strip()
                current_content = []
            else:
                current_content.append(line)

        # Add last section
        if current_section:
            sections.append({
                "title": current_section,
                "summary": self.summarize_text(" ".join(current_content), max_length=100).get("summary", "")
            })

        return sections


def example_usage():
    """Example usage of summarization skill."""
    summarizer = SummarizationSkill()

    # Example text
    text = """
    Artificial intelligence is transforming the way we work and live. Machine learning algorithms
    can now process vast amounts of data and identify patterns that humans might miss. This technology
    is being applied in healthcare, finance, transportation, and many other industries. However, there
    are important ethical considerations to address, including privacy concerns and potential job
    displacement. As AI continues to advance, it's crucial that we develop it responsibly and ensure
    it benefits all of humanity.
    """

    # Summarize text
    result = summarizer.summarize_text(text, style="concise")
    print(f"Summary: {result['summary']}\n")

    # Extract key points
    key_points = summarizer.extract_key_points(text, num_points=3)
    print("Key Points:")
    for i, point in enumerate(key_points, 1):
        print(f"{i}. {point}")

    # Generate TL;DR
    tldr = summarizer.generate_tldr(text)
    print(f"\n{tldr}")


if __name__ == "__main__":
    example_usage()
