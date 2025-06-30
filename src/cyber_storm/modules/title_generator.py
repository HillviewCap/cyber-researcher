"""
Title generation module for Cyber-Researcher.

This module provides intelligent title generation with length constraints
and content-based optimization.
"""

import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class TitleConfig:
    """Configuration for title generation."""

    max_length: int = 80
    min_length: int = 20
    style: str = "engaging"  # engaging, formal, technical
    include_numbers: bool = True
    prefer_keywords: bool = True


class TitleGenerator:
    """Intelligent title generator with length constraints."""

    def __init__(self, config: Optional[TitleConfig] = None):
        """Initialize title generator."""
        self.config = config or TitleConfig()

        # Common cybersecurity keywords for prioritization
        self.cybersecurity_keywords = {
            "threat",
            "security",
            "attack",
            "defense",
            "vulnerability",
            "breach",
            "malware",
            "ransomware",
            "phishing",
            "zero-day",
            "encryption",
            "firewall",
            "intrusion",
            "detection",
            "prevention",
            "incident",
            "response",
            "forensics",
            "compliance",
            "risk",
            "assessment",
            "audit",
            "penetration",
            "testing",
            "authentication",
            "authorization",
            "identity",
            "access",
            "management",
            "cloud",
            "network",
            "endpoint",
            "infrastructure",
            "data",
            "privacy",
            "governance",
            "framework",
            "standards",
            "regulations",
            "cyber",
            "digital",
        }

        # Stop words to remove from titles
        self.stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "about",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "up",
            "down",
            "out",
            "off",
            "over",
            "under",
            "again",
            "further",
            "then",
            "once",
            "very",
            "also",
            "just",
            "now",
            "how",
            "what",
            "where",
            "when",
            "why",
            "which",
            "who",
            "whom",
        }

    def generate_title(
        self, topic: str, content: Optional[str] = None, content_type: str = "blog_post", **kwargs
    ) -> str:
        """
        Generate an optimized title based on topic and content.

        Args:
            topic: Main topic/title input
            content: Generated content to analyze (optional)
            content_type: Type of content (blog_post, book_chapter, research_report)
            **kwargs: Additional parameters (chapter_number, etc.)

        Returns:
            Optimized title within length constraints
        """
        try:
            # Extract keywords from topic and content
            keywords = self._extract_keywords(topic, content)

            # Generate title based on content type
            if content_type == "book_chapter":
                base_title = self._generate_chapter_title(topic, keywords, **kwargs)
            elif content_type == "research_report":
                base_title = self._generate_report_title(topic, keywords, **kwargs)
            else:  # blog_post or default
                base_title = self._generate_blog_title(topic, keywords)

            # Apply length constraints and optimization
            optimized_title = self._optimize_title_length(base_title, keywords)

            return optimized_title

        except Exception:
            # Fallback to simple truncation of original topic
            return self._fallback_title(topic, content_type, **kwargs)

    def _extract_keywords(self, topic: str, content: Optional[str] = None) -> List[str]:
        """Extract important keywords from topic and content."""
        keywords = []

        # Process topic
        topic_words = self._tokenize_text(topic)
        keywords.extend(topic_words)

        # Process content if available (first 500 chars to avoid processing huge content)
        if content:
            content_sample = content[:500].lower()
            content_words = self._tokenize_text(content_sample)

            # Prioritize cybersecurity keywords found in content
            cyber_keywords = [word for word in content_words if word in self.cybersecurity_keywords]
            keywords.extend(cyber_keywords)

        # Remove duplicates and stop words, prioritize cybersecurity terms
        filtered_keywords = []
        seen = set()

        # First pass: cybersecurity keywords
        for word in keywords:
            if (
                word not in seen
                and word not in self.stop_words
                and word in self.cybersecurity_keywords
                and len(word) > 2
            ):
                filtered_keywords.append(word)
                seen.add(word)

        # Second pass: other important words
        for word in keywords:
            if (
                word not in seen
                and word not in self.stop_words
                and len(word) > 2
                and len(filtered_keywords) < 8
            ):
                filtered_keywords.append(word)
                seen.add(word)

        return filtered_keywords[:6]  # Limit to most important keywords

    def _tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into clean words."""
        # Convert to lowercase and split on non-alphanumeric characters
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        return [word for word in words if len(word) > 2]

    def _generate_blog_title(self, topic: str, keywords: List[str]) -> str:
        """Generate a blog post title."""
        if not keywords:
            return topic

        # Try different title patterns based on style
        if self.config.style == "engaging":
            patterns = [
                f"{keywords[0].title()} {keywords[1].title()}: A Complete Guide",
                f"Understanding {keywords[0].title()} in {keywords[1].title()}",
                f"{keywords[0].title()} Best Practices for Modern Security",
                f"Essential {keywords[0].title()} Strategies You Need to Know",
                f"The Ultimate Guide to {keywords[0].title()} {keywords[1].title()}",
            ]
        elif self.config.style == "technical":
            patterns = [
                f"{keywords[0].title()} {keywords[1].title()}: Technical Analysis",
                f"Implementing {keywords[0].title()} in Enterprise Environments",
                f"{keywords[0].title()} Architecture and Implementation",
                f"Advanced {keywords[0].title()} Techniques and Methods",
            ]
        else:  # formal
            patterns = [
                f"{keywords[0].title()} {keywords[1].title()}: Professional Overview",
                f"Security Analysis: {keywords[0].title()} and {keywords[1].title()}",
                f"Enterprise {keywords[0].title()} Management",
                f"Professional {keywords[0].title()} Implementation Guide",
            ]

        # Select the best fitting pattern
        for pattern in patterns:
            if len(pattern) <= self.config.max_length:
                return pattern

        # Fallback: use first few keywords
        return " ".join(word.title() for word in keywords[:3])

    def _generate_chapter_title(self, topic: str, keywords: List[str], **kwargs) -> str:
        """Generate a book chapter title."""
        chapter_num = kwargs.get("chapter_number", 1)

        if not keywords:
            # Shorten the original topic
            short_topic = self._truncate_intelligently(topic, self.config.max_length - 15)
            return f"Chapter {chapter_num}: {short_topic}"

        # Create concise chapter title
        if len(keywords) >= 2:
            title_part = f"{keywords[0].title()} and {keywords[1].title()}"
        else:
            title_part = keywords[0].title()

        chapter_title = f"Chapter {chapter_num}: {title_part}"

        # Add additional context if space allows
        if len(chapter_title) < self.config.max_length - 20 and len(keywords) > 2:
            chapter_title += f" - {keywords[2].title()}"

        return chapter_title

    def _generate_report_title(self, topic: str, keywords: List[str], **kwargs) -> str:
        """Generate a research report title."""
        report_type = kwargs.get("report_type", "Security Analysis")

        if not keywords:
            short_topic = self._truncate_intelligently(topic, self.config.max_length - 20)
            return f"{report_type}: {short_topic}"

        # Create professional report title
        if len(keywords) >= 2:
            title_part = f"{keywords[0].title()} {keywords[1].title()}"
        else:
            title_part = keywords[0].title()

        # Choose appropriate report type based on keywords
        if "threat" in keywords or "attack" in keywords:
            report_prefix = "Threat Assessment"
        elif "risk" in keywords or "vulnerability" in keywords:
            report_prefix = "Risk Analysis"
        elif "incident" in keywords or "response" in keywords:
            report_prefix = "Incident Analysis"
        else:
            report_prefix = "Security Analysis"

        return f"{report_prefix}: {title_part}"

    def _optimize_title_length(self, title: str, keywords: List[str]) -> str:
        """Optimize title length while preserving meaning."""
        if len(title) <= self.config.max_length:
            return title

        # Try progressive shortening strategies
        optimized = title

        # 1. Remove common redundant words
        redundant_phrases = [
            "A Complete Guide to",
            "A Comprehensive Guide to",
            "An Introduction to",
            "Understanding the",
            "The Ultimate Guide to",
            "Best Practices for",
            "Advanced Techniques for",
            "Professional Guide to",
            "Complete Analysis of",
        ]

        for phrase in redundant_phrases:
            optimized = optimized.replace(phrase, "").strip()
            if len(optimized) <= self.config.max_length and len(optimized) > self.config.min_length:
                return optimized

        # 2. Use abbreviations for common cybersecurity terms
        abbreviations = {
            "Information Security": "InfoSec",
            "Cybersecurity": "CyberSec",
            "Application Security": "AppSec",
            "Network Security": "NetSec",
            "Cloud Security": "CloudSec",
            "Infrastructure": "Infra",
            "Management": "Mgmt",
            "Implementation": "Impl",
            "Assessment": "Assessment",
            "Analysis": "Analysis",
        }

        for full_term, abbrev in abbreviations.items():
            optimized = optimized.replace(full_term, abbrev)
            if len(optimized) <= self.config.max_length:
                return optimized

        # 3. Intelligent truncation at word boundaries
        return self._truncate_intelligently(optimized, self.config.max_length)

    def _truncate_intelligently(self, text: str, max_length: int) -> str:
        """Truncate text at word boundaries while preserving meaning."""
        if len(text) <= max_length:
            return text

        # Find the last space before max_length
        truncated = text[:max_length]
        last_space = truncated.rfind(" ")

        if last_space > max_length * 0.7:  # If we can keep most of the text
            return text[:last_space].rstrip(",:;-")
        else:
            # Truncate at max_length and add ellipsis if needed
            return text[: max_length - 3].rstrip(",:;- ") + "..."

    def _fallback_title(self, topic: str, content_type: str, **kwargs) -> str:
        """Fallback title generation method."""
        # Simple fallback patterns
        if content_type == "book_chapter":
            chapter_num = kwargs.get("chapter_number", 1)
            short_topic = self._truncate_intelligently(topic, 60)
            return f"Chapter {chapter_num}: {short_topic}"
        elif content_type == "research_report":
            short_topic = self._truncate_intelligently(topic, 60)
            return f"Security Analysis: {short_topic}"
        else:
            return self._truncate_intelligently(topic, self.config.max_length)


# Global title generator instance
title_generator = TitleGenerator()
