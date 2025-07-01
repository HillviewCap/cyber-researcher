"""
Historian Agent for Cyber-Researcher.

This agent focuses on historical context, narrative frameworks,
and drawing parallels between historical events and modern cybersecurity incidents.
"""

from typing import Any, Dict, List, Optional, Tuple

from .base import BaseCyberAgent, AgentRole, AgentContext, AgentResponse


class HistorianAgent(BaseCyberAgent):
    """
    Historian Agent specializing in historical context and narrative generation.

    This agent brings a historical perspective focused on:
    - Historical parallels to modern cyber incidents
    - Narrative frameworks and storytelling
    - Evolution of information warfare and espionage
    - Lessons from past conflicts and intelligence operations
    - Cultural and societal context for security events
    - Educational storytelling techniques
    """

    def __init__(self, *args, **kwargs):
        super().__init__(AgentRole.HISTORIAN, *args, **kwargs)

    def _get_perspective(self) -> str:
        """Return the Historian's unique perspective."""
        return "historical context and narrative storytelling"

    def _get_expertise_areas(self) -> List[str]:
        """Return the Historian's areas of expertise."""
        return [
            "Historical Analysis",
            "Information Warfare History",
            "Espionage and Intelligence History",
            "Military History and Strategy",
            "Narrative Construction",
            "Storytelling Techniques",
            "Cultural Context Analysis",
            "Technology Evolution",
            "Communications History",
            "Educational Methodology",
        ]

    def _get_response_style(self) -> Dict[str, Any]:
        """Return the Historian's preferred response style."""
        return {
            "tone": "engaging and educational",
            "focus": "narrative coherence and historical parallels",
            "citations": "historical sources and academic references",
            "examples": "historical events and analogies",
            "depth": "contextual with engaging storytelling",
        }

    def analyze_topic(self, context: AgentContext) -> AgentResponse:
        """
        Analyze a cybersecurity topic from a historical perspective.

        Args:
            context: The analysis context

        Returns:
            AgentResponse with historical analysis and narrative elements
        """
        # Retrieve relevant historical information
        historical_info = self.retrieve_information(
            f"history {context.topic} espionage intelligence warfare communication",
            max_results=context.max_sources,
        )

        # Find historical parallels
        parallels = self._find_historical_parallels(context.topic)

        # Build analysis prompt
        prompt = self._format_prompt(
            """
            As a {role} with expertise in {expertise}, analyze the following cybersecurity topic from a historical perspective:
            
            Topic: {topic}
            Content Type: {content_type}
            Target Audience: {audience}
            Narrative Style: {narrative_style}
            
            Please provide a comprehensive historical analysis covering:
            1. Historical parallels and analogies to modern cyber incidents
            2. Evolution of information warfare and espionage techniques
            3. Lessons learned from past conflicts and intelligence operations
            4. Cultural and societal context that enhances understanding
            5. Narrative frameworks that make technical concepts accessible
            6. Educational storytelling opportunities
            
            Focus on creating engaging narratives that help readers connect historical events to modern cybersecurity.
            
            Historical Parallels Identified:
            {parallels}
            
            Retrieved Context:
            {context_info}
            """,
            topic=context.topic,
            content_type=context.content_type.value,
            audience=context.target_audience,
            narrative_style=context.narrative_style,
            parallels=self._format_parallels(parallels),
            context_info=self._format_retrieval_context(historical_info),
        )

        # Generate analysis
        analysis = self._generate_response(prompt)

        # Extract and filter sources
        raw_sources = [item.get("url", "") for item in historical_info if item.get("url")]
        sources = self._filter_placeholder_urls(raw_sources)

        # Generate narrative suggestions
        suggestions = self._generate_narrative_suggestions(context)

        return AgentResponse(
            content=analysis,
            sources=sources,
            confidence=0.82,  # Good confidence in historical analysis
            suggestions=suggestions,
            metadata={
                "agent_role": self.role.value,
                "analysis_type": "historical_narrative",
                "expertise_areas": self.expertise_areas,
                "retrieved_sources": len(historical_info),
                "historical_parallels": len(parallels),
                "narrative_elements": self._identify_narrative_elements(context.topic),
            },
        )

    def generate_questions(self, context: AgentContext) -> List[str]:
        """
        Generate historically-informed questions about a topic.

        Args:
            context: The context for question generation

        Returns:
            List of historically-informed questions
        """
        prompt = self._format_prompt(
            """
            As a {role} analyzing the cybersecurity topic "{topic}", generate 8-10 thought-provoking questions 
            that would help explore the historical context and narrative potential of this topic.
            
            Focus on questions about:
            - Historical parallels and analogies
            - Evolution of similar techniques over time
            - Lessons from past conflicts and operations
            - Cultural and societal implications
            - Narrative and storytelling opportunities
            - Educational frameworks and analogies
            
            Format each question on a new line starting with "Q:"
            """,
            topic=context.topic,
        )

        response = self._generate_response(prompt)

        # Extract questions from response
        questions = []
        for line in response.split("\n"):
            if line.strip().startswith("Q:"):
                questions.append(line.strip()[2:].strip())

        return questions[:10]  # Limit to 10 questions

    def review_content(self, content: str, context: AgentContext) -> AgentResponse:
        """
        Review content from a historian's perspective.

        Args:
            content: The content to review
            context: The review context

        Returns:
            AgentResponse with historically-informed feedback
        """
        prompt = self._format_prompt(
            """
            As a {role} with expertise in {expertise}, please review the following content about "{topic}":
            
            CONTENT TO REVIEW:
            {content}
            
            Please provide feedback focusing on:
            1. Historical accuracy and context
            2. Narrative coherence and flow
            3. Accessibility for the target audience ({audience})
            4. Opportunities for historical parallels and analogies
            5. Storytelling effectiveness
            6. Educational value and engagement
            
            Provide specific, actionable feedback to improve the historical narrative elements.
            """,
            topic=context.topic,
            content=content,
            audience=context.target_audience,
        )

        feedback = self._generate_response(prompt)

        # Generate improvement suggestions
        suggestions = [
            "Add more compelling historical analogies",
            "Include timeline visualizations",
            "Strengthen narrative arc and story structure",
            "Add character-driven historical examples",
            "Include cultural context and broader implications",
            "Enhance educational storytelling elements",
        ]

        return AgentResponse(
            content=feedback,
            sources=[],
            confidence=0.85,  # Good confidence in narrative review
            suggestions=suggestions,
            metadata={
                "agent_role": self.role.value,
                "review_type": "historical_narrative",
                "content_length": len(content),
                "focus_areas": ["historical_accuracy", "narrative_coherence", "educational_value"],
            },
        )

    def _find_historical_parallels(self, topic: str) -> List[Dict[str, str]]:
        """Find historical parallels for a cybersecurity topic."""
        topic_lower = topic.lower()

        parallels_database = {
            "ransomware": [
                {
                    "event": "Barbary Coast Pirates (16th-19th century)",
                    "parallel": "Demanded ransom for captured ships and crews",
                    "lesson": "Economic extortion as a persistent threat model",
                },
                {
                    "event": "Kidnapping for Ransom (19th-20th century)",
                    "parallel": "Holding valuable assets hostage for payment",
                    "lesson": "Negotiation dynamics and law enforcement response",
                },
            ],
            "phishing": [
                {
                    "event": "Trojan Horse (Ancient Greece)",
                    "parallel": "Deceptive gift concealing hostile intent",
                    "lesson": "Social engineering and trust exploitation",
                },
                {
                    "event": "World War II Deception Operations",
                    "parallel": "False communications to mislead enemies",
                    "lesson": "Information warfare and credibility manipulation",
                },
            ],
            "supply_chain": [
                {
                    "event": "Operation Bernhard (WWII)",
                    "parallel": "Counterfeiting currency to undermine economy",
                    "lesson": "Attacking trust in fundamental systems",
                },
                {
                    "event": "Cold War Industrial Espionage",
                    "parallel": "Infiltrating manufacturing and technology supply chains",
                    "lesson": "Long-term strategic compromise of critical infrastructure",
                },
            ],
            "insider_threat": [
                {
                    "event": "Benedict Arnold (American Revolution)",
                    "parallel": "Trusted insider betraying confidential information",
                    "lesson": "Motivations for betrayal and detection challenges",
                },
                {
                    "event": "Cambridge Five (Cold War)",
                    "parallel": "Long-term penetration of intelligence services",
                    "lesson": "Recruitment, handling, and counterintelligence",
                },
            ],
            "encryption": [
                {
                    "event": "Enigma Machine (WWII)",
                    "parallel": "Strategic importance of cryptographic security",
                    "lesson": "Balance between security and operational efficiency",
                },
                {
                    "event": "Telegraph and Diplomatic Codes (19th century)",
                    "parallel": "Protecting sensitive communications over distance",
                    "lesson": "Evolution of communication security needs",
                },
            ],
        }

        # Find relevant parallels
        relevant_parallels = []
        for key, parallels in parallels_database.items():
            if key in topic_lower:
                relevant_parallels.extend(parallels)

        # If no specific parallels found, use general ones
        if not relevant_parallels:
            relevant_parallels = [
                {
                    "event": "Art of War by Sun Tzu",
                    "parallel": "Strategic thinking about conflict and deception",
                    "lesson": "Timeless principles of strategy and intelligence",
                },
                {
                    "event": "Industrial Revolution Security Challenges",
                    "parallel": "Rapid technological change creating new vulnerabilities",
                    "lesson": "Technology adoption outpacing security considerations",
                },
            ]

        return relevant_parallels[:3]  # Limit to top 3 parallels

    def _format_parallels(self, parallels: List[Dict[str, str]]) -> str:
        """Format historical parallels for prompt inclusion."""
        if not parallels:
            return "No specific historical parallels identified."

        formatted = []
        for i, parallel in enumerate(parallels, 1):
            formatted.append(
                f"{i}. {parallel['event']}\n"
                f"   Parallel: {parallel['parallel']}\n"
                f"   Lesson: {parallel['lesson']}\n"
            )

        return "\n".join(formatted)

    def _identify_narrative_elements(self, topic: str) -> List[str]:
        """Identify key narrative elements for a topic."""
        elements = []
        topic_lower = topic.lower()

        # Universal narrative elements
        elements.extend(["conflict", "resolution", "character_development"])

        # Topic-specific elements
        if "war" in topic_lower or "attack" in topic_lower:
            elements.extend(["adversary_motivation", "strategic_objectives", "tactical_evolution"])

        if "espionage" in topic_lower or "intelligence" in topic_lower:
            elements.extend(["secrecy", "betrayal", "information_value"])

        if "technology" in topic_lower:
            elements.extend(["innovation", "adaptation", "unintended_consequences"])

        return elements

    def _generate_narrative_suggestions(self, context: AgentContext) -> List[str]:
        """Generate narrative-specific suggestions for content enhancement."""
        base_suggestions = [
            f"Develop a compelling narrative arc for {context.topic}",
            f"Include character-driven historical examples",
            f"Add timeline visualizations showing evolution",
            f"Create engaging opening hooks with historical context",
            f"Include 'lessons learned' sections connecting past and present",
        ]

        # Add content-type specific suggestions
        if context.content_type.value == "blog_post":
            base_suggestions.extend(
                [
                    "Start with an engaging historical anecdote",
                    "Use sidebar boxes for historical context",
                    "Include interactive timeline elements",
                ]
            )
        elif context.content_type.value == "book_chapter":
            base_suggestions.extend(
                [
                    "Develop detailed character profiles from history",
                    "Include comprehensive historical background sections",
                    "Add thought-provoking discussion questions",
                    "Create comparative analysis tables (historical vs. modern)",
                ]
            )

        return base_suggestions

    def _format_retrieval_context(self, retrieved_info: List[Dict[str, Any]]) -> str:
        """Format retrieved historical information for prompt context."""
        if not retrieved_info:
            return "No additional historical context retrieved."

        formatted = []
        for i, item in enumerate(retrieved_info[:5], 1):  # Limit to top 5
            title = item.get("title", "Unknown Historical Source")
            content = item.get("content", "")[:500]  # Limit content length
            url = item.get("url", "")

            formatted.append(f"Historical Source {i} ({title}):\n{content}...\nURL: {url}\n")

        return "\n".join(formatted)

    def create_narrative_framework(self, topic: str, target_audience: str) -> Dict[str, Any]:
        """
        Create a narrative framework for a cybersecurity topic.

        Args:
            topic: The cybersecurity topic
            target_audience: The intended audience

        Returns:
            Dictionary containing narrative framework elements
        """
        framework = {
            "opening_hook": f"Historical event that parallels {topic}",
            "conflict": "The central challenge or threat",
            "characters": ["Historical figures", "Modern cybersecurity professionals"],
            "setting": "Both historical and contemporary contexts",
            "rising_action": "Escalation of the threat or challenge",
            "climax": "Key moment of decision or breakthrough",
            "resolution": "Lessons learned and modern applications",
            "themes": ["Trust", "Innovation", "Adaptation", "Human nature"],
            "educational_objectives": [
                f"Understand the evolution of threats like {topic}",
                "Recognize patterns across historical periods",
                "Apply historical lessons to modern challenges",
            ],
        }

        return framework

    def get_historical_timeline(self, topic: str) -> List[Tuple[str, str, str]]:
        """
        Get a historical timeline for a cybersecurity topic.

        Args:
            topic: The cybersecurity topic

        Returns:
            List of tuples (period, event, relevance)
        """
        # This would typically query a historical database
        # For now, return example timeline entries
        return [
            (
                "Ancient Times",
                "Development of secret codes and ciphers",
                "Foundation of cryptography",
            ),
            (
                "Medieval Period",
                "Use of carrier pigeons for secure communication",
                "Early secure communication methods",
            ),
            (
                "Industrial Revolution",
                "Telegraph and early electronic communication",
                "Birth of electronic information security",
            ),
            (
                "World Wars",
                "Systematic codebreaking and intelligence operations",
                "Modern intelligence tradecraft",
            ),
            (
                "Cold War",
                "Electronic surveillance and computer espionage",
                "Digital age security challenges",
            ),
            (
                "Internet Age",
                "Rise of cyber warfare and digital threats",
                "Contemporary cybersecurity landscape",
            ),
        ]

    def _filter_placeholder_urls(self, urls: List[str]) -> List[str]:
        """
        Filter out placeholder/test URLs and replace with real historical sources.

        Args:
            urls: List of URLs to filter

        Returns:
            List of filtered URLs with real sources
        """
        # Define placeholder URL patterns to filter out
        placeholder_patterns = ["example.com", "test.com", "placeholder.com", "sample.com"]

        # Filter out placeholder URLs
        real_urls = []
        for url in urls:
            if url and not any(pattern in url for pattern in placeholder_patterns):
                real_urls.append(url)

        # If we have no real URLs, add some well-known historical sources
        if not real_urls:
            real_urls = [
                "https://www.nsa.gov/about/cryptologic-heritage/",
                "https://www.cia.gov/library/",
                "https://www.history.com/topics/world-war-ii/enigma-machine",
                "https://www.britannica.com/topic/cryptography",
                "https://www.nytimes.com/column/retropolis",
                "https://www.smithsonianmag.com/history/",
            ]

        return real_urls
