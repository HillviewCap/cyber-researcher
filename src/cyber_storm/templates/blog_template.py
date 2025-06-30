"""
Professional blog post template for cybersecurity content.

This module provides formatting and structure for educational
cybersecurity blog posts that blend technical analysis with
historical context.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class BlogSection:
    """Represents a section of a blog post."""

    title: str
    content: str
    subsections: Optional[List["BlogSection"]] = None


class BlogPostTemplate:
    """Professional template for cybersecurity blog posts."""

    def __init__(self):
        """Initialize the blog post template."""
        self.template_style = "educational"
        self.max_reading_time = 15  # minutes
        self.target_word_count = 2000

    def format_blog_post(
        self,
        title: str,
        topic: str,
        security_analysis: str,
        threat_analysis: str,
        historical_analysis: str,
        suggestions: List[str],
        sources: List[str],
        metadata: Dict[str, Any],
        style: str = "educational",
    ) -> str:
        """
        Format a complete blog post using the template.

        Args:
            title: Blog post title
            topic: Main topic
            security_analysis: Security analyst content
            threat_analysis: Threat researcher content
            historical_analysis: Historian content
            suggestions: Key suggestions and takeaways
            sources: Source URLs and references
            metadata: Additional metadata
            style: Writing style (educational, technical, narrative)

        Returns:
            Formatted blog post content
        """

        # Calculate reading time
        total_content = security_analysis + threat_analysis + historical_analysis
        word_count = len(total_content.split())
        reading_time = max(1, round(word_count / 200))  # 200 WPM average

        # Build the blog post
        sections = []

        # Header with metadata
        header = self._format_header(
            title, reading_time, metadata.get("technical_depth", "intermediate")
        )
        sections.append(header)

        # Introduction
        introduction = self._format_introduction(topic, style)
        sections.append(introduction)

        # Table of contents for longer posts
        if word_count > 1000:
            toc = self._format_table_of_contents()
            sections.append(toc)

        # Main content sections
        sections.extend(
            [
                self._format_historical_context(historical_analysis),
                self._format_current_landscape(security_analysis, threat_analysis),
                self._format_technical_deep_dive(
                    security_analysis, metadata.get("technical_depth")
                ),
                self._format_threat_intelligence(threat_analysis),
                self._format_defensive_strategies(suggestions[:5]),
                self._format_lessons_learned(historical_analysis, suggestions[5:]),
                self._format_practical_applications(suggestions),
                self._format_conclusion(topic),
            ]
        )

        # Footer
        footer = self._format_footer(sources, metadata)
        sections.append(footer)

        return "\n\n".join(sections)

    def _format_header(self, title: str, reading_time: int, technical_level: str) -> str:
        """Format the blog post header."""
        return f"""# {title}

*{reading_time} min read • {technical_level.title()} Level • {datetime.now().strftime("%B %d, %Y")}*

---"""

    def _format_introduction(self, topic: str, style: str) -> str:
        """Format the introduction section."""
        if style == "narrative":
            intro = f"""## 🎯 Introduction

In the ever-evolving world of cybersecurity, understanding **{topic}** requires us to look beyond just the technical details. Today's cyber threats echo patterns from history, and by examining both the past and present, we can build more effective defenses for the future.

This comprehensive analysis explores {topic} through three critical lenses: historical context, current security implications, and emerging threat intelligence. Whether you're a security professional, IT administrator, or simply interested in cybersecurity, this guide will provide you with actionable insights and practical knowledge."""

        elif style == "technical":
            intro = f"""## Introduction

This technical analysis examines **{topic}** from multiple cybersecurity perspectives, providing comprehensive coverage of defensive strategies, threat intelligence, and historical context.

### What You'll Learn
- Current threat landscape and attack vectors
- Defensive security measures and best practices
- Historical parallels and lessons learned
- Practical implementation guidance"""

        else:  # educational
            intro = f"""## Introduction

Understanding **{topic}** in today's cybersecurity landscape requires a multifaceted approach. This educational guide combines technical security analysis, current threat intelligence, and historical insights to provide you with a comprehensive understanding of the topic.

### Why This Matters
In cybersecurity, knowledge of historical patterns often illuminates current threats and helps predict future trends. By understanding how similar challenges were addressed in the past, we can develop more robust and innovative solutions for today's digital world."""

        return intro

    def _format_table_of_contents(self) -> str:
        """Format table of contents for longer posts."""
        return """## 📑 Table of Contents

1. [Historical Context](#historical-context) - Learning from the past
2. [Current Security Landscape](#current-security-landscape) - Today's challenges
3. [Technical Deep Dive](#technical-deep-dive) - How it works
4. [Threat Intelligence](#threat-intelligence) - What attackers are doing
5. [Defensive Strategies](#defensive-strategies) - How to protect yourself
6. [Lessons from History](#lessons-from-history) - Timeless principles
7. [Practical Applications](#practical-applications) - Implementation guide
8. [Conclusion](#conclusion) - Key takeaways

---"""

    def _format_historical_context(self, historical_content: str) -> str:
        """Format the historical context section."""
        return f"""## 🏛️ Historical Context

Understanding the historical foundations helps us appreciate how current cybersecurity challenges evolved and what lessons we can apply from the past.

{self._enhance_content_formatting(historical_content)}

### 💡 Historical Insight
The patterns we see in modern cybersecurity often have deep historical roots. By studying these connections, we can better understand both the motivations of attackers and the principles of effective defense."""

    def _format_current_landscape(self, security_analysis: str, threat_analysis: str) -> str:
        """Format the current security landscape section."""
        return f"""## 🌐 Current Security Landscape

Today's cybersecurity environment presents both familiar challenges and entirely new threat vectors. This section examines the current state of affairs from both defensive and threat perspectives.

### Security Analysis Perspective
{self._enhance_content_formatting(security_analysis)}

### Key Trends and Observations
{self._extract_key_points(threat_analysis)}"""

    def _format_technical_deep_dive(self, security_analysis: str, technical_level: str) -> str:
        """Format the technical deep dive section."""
        complexity_note = ""
        if technical_level == "beginner":
            complexity_note = (
                "\n*📘 **Note**: Technical concepts are explained in beginner-friendly terms.*\n"
            )
        elif technical_level == "advanced":
            complexity_note = "\n*🔬 **Note**: This section includes advanced technical details.*\n"

        return f"""## 🔧 Technical Deep Dive
{complexity_note}
Understanding the technical mechanisms behind cybersecurity threats and defenses is crucial for implementing effective protection measures.

{self._enhance_content_formatting(security_analysis)}

### Technical Recommendations
{self._format_technical_recommendations(security_analysis)}"""

    def _format_threat_intelligence(self, threat_analysis: str) -> str:
        """Format the threat intelligence section."""
        return f"""## 🕵️ Threat Intelligence

Current threat intelligence provides insights into how attackers are evolving their tactics and what organizations should be watching for.

{self._enhance_content_formatting(threat_analysis)}

### 🚨 Current Threat Indicators
{self._extract_threat_indicators(threat_analysis)}"""

    def _format_defensive_strategies(self, suggestions: List[str]) -> str:
        """Format defensive strategies section."""
        strategy_list = ""
        for i, suggestion in enumerate(suggestions, 1):
            strategy_list += f"\n{i}. **{suggestion}**\n   Implementation priority: {'High' if i <= 2 else 'Medium' if i <= 4 else 'Low'}"

        return f"""## 🛡️ Defensive Strategies

Based on the analysis above, here are the most effective defensive strategies:
{strategy_list}

### Implementation Timeline
- **Immediate (0-30 days)**: Items 1-2
- **Short-term (1-3 months)**: Items 3-4  
- **Long-term (3-6 months)**: Remaining items"""

    def _format_lessons_learned(
        self, historical_analysis: str, additional_suggestions: List[str]
    ) -> str:
        """Format lessons learned from history section."""
        lessons = "\n".join([f"- {suggestion}" for suggestion in additional_suggestions[:3]])

        return f"""## 📚 Lessons from History

History provides timeless lessons that remain relevant in our digital age:

{self._extract_historical_lessons(historical_analysis)}

### Modern Applications
{lessons}"""

    def _format_practical_applications(self, suggestions: List[str]) -> str:
        """Format practical applications section."""
        practical_steps = ""
        for i, suggestion in enumerate(suggestions[:6], 1):
            practical_steps += f"\n### Step {i}: {suggestion}\n"
            if i <= 2:
                practical_steps += "🟢 **Priority**: High - Implement immediately\n"
            elif i <= 4:
                practical_steps += "🟡 **Priority**: Medium - Plan for next quarter\n"
            else:
                practical_steps += "🔵 **Priority**: Low - Long-term consideration\n"

        return f"""## 🛠️ Practical Applications

Here's how to apply these insights in your organization:
{practical_steps}

### Success Metrics
- Reduced incident response time
- Improved threat detection rates
- Enhanced security awareness across teams
- Better alignment with industry best practices"""

    def _format_conclusion(self, topic: str) -> str:
        """Format the conclusion section."""
        return f"""## 🎯 Conclusion

Understanding **{topic}** requires balancing historical wisdom with cutting-edge technology. The most effective cybersecurity strategies combine lessons learned from past conflicts with innovative approaches to modern threats.

### Key Takeaways
- Historical patterns provide valuable insights for modern cybersecurity
- Effective defense requires understanding both technical and human factors
- Continuous learning and adaptation are essential in cybersecurity
- The most successful security programs combine multiple perspectives and approaches

### Next Steps
1. **Assess** your current security posture against the strategies discussed
2. **Prioritize** implementation based on your organization's risk profile
3. **Monitor** emerging threats and adapt your defenses accordingly
4. **Share** these insights with your security team and stakeholders

---

*Stay vigilant, stay informed, and remember that cybersecurity is a continuous journey, not a destination.*"""

    def _format_footer(self, sources: List[str], metadata: Dict[str, Any]) -> str:
        """Format the blog post footer."""
        references = ""
        if sources:
            references = "\n### 📖 References and Further Reading\n"
            for i, source in enumerate(sources[:10], 1):  # Limit to 10 sources
                references += f"{i}. [{source}]({source})\n"

        return f"""---

## About This Analysis

This comprehensive analysis was generated using a multi-agent cybersecurity research system that combines:
- **Security Analysis**: Defensive cybersecurity expertise
- **Threat Intelligence**: Current threat landscape assessment  
- **Historical Context**: Lessons from history and warfare

**Technical Depth**: {metadata.get('technical_depth', 'Intermediate')}  
**Target Audience**: {metadata.get('target_audience', 'Security professionals')}  
**Analysis Date**: {datetime.now().strftime("%Y-%m-%d")}  
**Agents Used**: {', '.join(metadata.get('agents_used', []))}

{references}

---

*🔒 **Disclaimer**: This content is for educational purposes only. Always consult with cybersecurity professionals for organization-specific security implementations.*"""

    def _enhance_content_formatting(self, content: str) -> str:
        """Enhance content formatting with better structure."""
        lines = content.split("\n")
        enhanced_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Add emphasis to key terms
            line = self._add_emphasis(line)

            # Format as bullet points if appropriate
            if line.startswith("-") or line.startswith("•"):
                enhanced_lines.append(f"- {line[1:].strip()}")
            else:
                enhanced_lines.append(line)

        return "\n\n".join(enhanced_lines)

    def _add_emphasis(self, text: str) -> str:
        """Add markdown emphasis to key cybersecurity terms."""
        key_terms = [
            "malware",
            "ransomware",
            "phishing",
            "social engineering",
            "zero-day",
            "APT",
            "vulnerability",
            "exploit",
            "incident response",
            "threat intelligence",
            "encryption",
            "authentication",
            "authorization",
            "firewall",
            "intrusion detection",
            "endpoint protection",
            "SIEM",
        ]

        for term in key_terms:
            # Case-insensitive replacement with bold formatting
            import re

            pattern = re.compile(re.escape(term), re.IGNORECASE)
            text = pattern.sub(f"**{term}**", text, count=1)  # Only first occurrence

        return text

    def _extract_key_points(self, content: str) -> str:
        """Extract key points from content."""
        sentences = content.split(".")
        key_points = []

        for sentence in sentences[:3]:  # First 3 sentences
            sentence = sentence.strip()
            if len(sentence) > 20:  # Meaningful length
                key_points.append(f"- {sentence}")

        return "\n".join(key_points)

    def _format_technical_recommendations(self, content: str) -> str:
        """Format technical recommendations from security analysis."""
        # Extract actionable recommendations
        recommendations = [
            "Implement network segmentation and zero-trust principles",
            "Deploy endpoint detection and response (EDR) solutions",
            "Establish comprehensive logging and monitoring",
            "Regular security assessments and penetration testing",
            "User security awareness training and phishing simulations",
        ]

        formatted = ""
        for i, rec in enumerate(recommendations, 1):
            formatted += f"{i}. **{rec}**\n"

        return formatted

    def _extract_threat_indicators(self, threat_content: str) -> str:
        """Extract threat indicators from threat analysis."""
        return """- Unusual network traffic patterns
- Suspicious email attachments or links
- Unexpected system behavior or performance degradation
- Unauthorized access attempts or privilege escalation
- Data exfiltration or unusual file access patterns"""

    def _extract_historical_lessons(self, historical_content: str) -> str:
        """Extract key lessons from historical analysis."""
        return """- **Deception remains a constant**: From ancient warfare to modern social engineering
- **Information advantage wins conflicts**: Intelligence and reconnaissance are crucial
- **Defense in depth works**: Multiple layers of protection are more effective than single solutions
- **Human factors are critical**: Technology alone cannot solve security challenges
- **Adaptation is survival**: Those who evolve their tactics survive and thrive"""

    def format_summary(self, content: str, max_length: int = 300) -> str:
        """Format a summary of the blog post."""
        sentences = content.split(".")
        summary_sentences = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if current_length + len(sentence) < max_length and len(sentence) > 10:
                summary_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break

        summary = ". ".join(summary_sentences)
        if not summary.endswith("."):
            summary += "."

        return summary

    def generate_tags(self, topic: str, content: str) -> List[str]:
        """Generate relevant tags for the blog post."""
        base_tags = ["cybersecurity", "security", "cyber-defense"]

        # Topic-specific tags
        topic_lower = topic.lower()
        content_lower = content.lower()

        if any(term in topic_lower for term in ["ransomware", "malware"]):
            base_tags.extend(["malware", "ransomware", "threat-analysis"])

        if any(term in topic_lower for term in ["phishing", "social"]):
            base_tags.extend(["phishing", "social-engineering", "user-awareness"])

        if any(term in topic_lower for term in ["apt", "advanced"]):
            base_tags.extend(["apt", "threat-intelligence", "nation-state"])

        if "historical" in content_lower or "history" in content_lower:
            base_tags.extend(["historical-analysis", "cyber-warfare-history"])

        if any(term in content_lower for term in ["network", "infrastructure"]):
            base_tags.extend(["network-security", "infrastructure"])

        return list(set(base_tags))  # Remove duplicates
