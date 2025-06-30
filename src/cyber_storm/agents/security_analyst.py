"""
Security Analyst Agent for Cyber-Researcher.

This agent focuses on technical security aspects, defensive measures,
and current threat landscape analysis from a defender's perspective.
"""

from typing import Any, Dict, List, Optional

from .base import BaseCyberAgent, AgentRole, AgentContext, AgentResponse


class SecurityAnalystAgent(BaseCyberAgent):
    """
    Security Analyst Agent specializing in defensive cybersecurity analysis.
    
    This agent brings a technical security perspective focused on:
    - Defensive strategies and controls
    - Vulnerability analysis and mitigation
    - Security architecture and design
    - Incident response and forensics
    - Risk assessment and management
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(AgentRole.SECURITY_ANALYST, *args, **kwargs)
    
    def _get_perspective(self) -> str:
        """Return the Security Analyst's unique perspective."""
        return "defensive security and technical analysis"
    
    def _get_expertise_areas(self) -> List[str]:
        """Return the Security Analyst's areas of expertise."""
        return [
            "Network Security",
            "Endpoint Protection",
            "Vulnerability Management",
            "Security Architecture",
            "Incident Response",
            "Digital Forensics",
            "Risk Assessment",
            "Security Controls",
            "Threat Detection",
            "Compliance and Governance"
        ]
    
    def _get_response_style(self) -> Dict[str, Any]:
        """Return the Security Analyst's preferred response style."""
        return {
            "tone": "analytical and methodical",
            "focus": "technical accuracy and practical implementation",
            "citations": "security frameworks and standards",
            "examples": "real-world defensive scenarios",
            "depth": "technical with practical insights"
        }
    
    def analyze_topic(self, context: AgentContext) -> AgentResponse:
        """
        Analyze a cybersecurity topic from a defensive security perspective.
        
        Args:
            context: The analysis context
            
        Returns:
            AgentResponse with security analysis
        """
        # Retrieve relevant security information
        security_info = self.retrieve_information(
            f"cybersecurity defense {context.topic} vulnerabilities mitigation",
            max_results=context.max_sources
        )
        
        # Build analysis prompt
        prompt = self._format_prompt(
            """
            As a {role} with expertise in {expertise}, analyze the following cybersecurity topic from a defensive security perspective:
            
            Topic: {topic}
            Content Type: {content_type}
            Target Audience: {audience}
            Technical Depth: {depth}
            
            Please provide a comprehensive security analysis covering:
            1. Key security concerns and vulnerabilities
            2. Defensive strategies and controls
            3. Risk assessment considerations
            4. Implementation challenges
            5. Best practices and recommendations
            6. Relevant security frameworks or standards
            
            Focus on practical, actionable insights that help readers understand the defensive security implications.
            
            Retrieved Context:
            {context_info}
            """,
            topic=context.topic,
            content_type=context.content_type.value,
            audience=context.target_audience,
            depth=context.technical_depth,
            context_info=self._format_retrieval_context(security_info)
        )
        
        # Generate analysis
        analysis = self._generate_response(prompt)
        
        # Extract sources
        sources = [item.get("url", "") for item in security_info if item.get("url")]
        
        # Generate suggestions for further exploration
        suggestions = self._generate_security_suggestions(context)
        
        return AgentResponse(
            content=analysis,
            sources=sources,
            confidence=0.85,  # High confidence in security analysis
            suggestions=suggestions,
            metadata={
                "agent_role": self.role.value,
                "analysis_type": "defensive_security",
                "expertise_areas": self.expertise_areas,
                "retrieved_sources": len(security_info)
            }
        )
    
    def generate_questions(self, context: AgentContext) -> List[str]:
        """
        Generate security-focused questions about a topic.
        
        Args:
            context: The context for question generation
            
        Returns:
            List of security-focused questions
        """
        prompt = self._format_prompt(
            """
            As a {role} analyzing the cybersecurity topic "{topic}", generate 8-10 thought-provoking questions 
            that would help explore the defensive security aspects of this topic.
            
            Focus on questions about:
            - Vulnerabilities and attack vectors
            - Defensive measures and controls
            - Detection and monitoring strategies
            - Incident response considerations
            - Risk mitigation approaches
            - Security architecture implications
            
            Format each question on a new line starting with "Q:"
            """,
            topic=context.topic
        )
        
        response = self._generate_response(prompt)
        
        # Extract questions from response
        questions = []
        for line in response.split('\n'):
            if line.strip().startswith('Q:'):
                questions.append(line.strip()[2:].strip())
        
        return questions[:10]  # Limit to 10 questions
    
    def review_content(self, content: str, context: AgentContext) -> AgentResponse:
        """
        Review content from a security analyst perspective.
        
        Args:
            content: The content to review
            context: The review context
            
        Returns:
            AgentResponse with security-focused feedback
        """
        prompt = self._format_prompt(
            """
            As a {role} with expertise in {expertise}, please review the following content about "{topic}":
            
            CONTENT TO REVIEW:
            {content}
            
            Please provide feedback focusing on:
            1. Technical accuracy of security concepts
            2. Completeness of defensive perspectives
            3. Practical applicability of recommendations
            4. Missing security considerations
            5. Clarity for the target audience ({audience})
            
            Provide specific, actionable feedback to improve the security analysis.
            """,
            topic=context.topic,
            content=content,
            audience=context.target_audience
        )
        
        feedback = self._generate_response(prompt)
        
        # Generate improvement suggestions
        suggestions = [
            "Add more specific security controls and frameworks",
            "Include vulnerability assessment methodologies",
            "Provide implementation guidance for defensive measures",
            "Reference relevant security standards (NIST, ISO 27001, etc.)",
            "Include incident response and recovery considerations"
        ]
        
        return AgentResponse(
            content=feedback,
            sources=[],
            confidence=0.9,  # High confidence in security review
            suggestions=suggestions,
            metadata={
                "agent_role": self.role.value,
                "review_type": "security_analysis",
                "content_length": len(content),
                "focus_areas": ["technical_accuracy", "defensive_completeness", "practical_guidance"]
            }
        )
    
    def _generate_security_suggestions(self, context: AgentContext) -> List[str]:
        """Generate security-specific suggestions for further exploration."""
        base_suggestions = [
            f"Explore the MITRE ATT&CK framework for {context.topic}",
            f"Analyze defense-in-depth strategies for {context.topic}",
            f"Review NIST Cybersecurity Framework applications",
            f"Investigate threat modeling approaches for {context.topic}",
            f"Examine security monitoring and detection strategies"
        ]
        
        # Add content-type specific suggestions
        if context.content_type.value == "blog_post":
            base_suggestions.extend([
                "Include practical security tips for readers",
                "Add links to security tools and resources",
                "Provide real-world defensive case studies"
            ])
        elif context.content_type.value == "book_chapter":
            base_suggestions.extend([
                "Develop hands-on security exercises",
                "Include comprehensive security checklists",
                "Add detailed technical implementation guides"
            ])
        
        return base_suggestions
    
    def _format_retrieval_context(self, retrieved_info: List[Dict[str, Any]]) -> str:
        """Format retrieved information for prompt context."""
        if not retrieved_info:
            return "No additional context retrieved."
        
        formatted = []
        for i, item in enumerate(retrieved_info[:5], 1):  # Limit to top 5
            title = item.get("title", "Unknown Source")
            content = item.get("content", "")[:500]  # Limit content length
            url = item.get("url", "")
            
            formatted.append(f"Source {i} ({title}):\n{content}...\nURL: {url}\n")
        
        return "\n".join(formatted)
    
    def get_security_controls_for_topic(self, topic: str) -> List[str]:
        """
        Get relevant security controls for a specific topic.
        
        Args:
            topic: The cybersecurity topic
            
        Returns:
            List of applicable security controls
        """
        controls_map = {
            "ransomware": [
                "Backup and Recovery",
                "Endpoint Detection and Response",
                "Network Segmentation",
                "Access Controls",
                "Email Security",
                "User Training"
            ],
            "phishing": [
                "Email Filtering",
                "User Awareness Training",
                "Multi-Factor Authentication",
                "DNS Filtering",
                "Incident Response",
                "Threat Intelligence"
            ],
            "insider threat": [
                "Privileged Access Management",
                "Data Loss Prevention",
                "User Behavior Analytics",
                "Access Reviews",
                "Segregation of Duties",
                "Monitoring and Logging"
            ]
        }
        
        # Return relevant controls or generic ones
        topic_lower = topic.lower()
        for key, controls in controls_map.items():
            if key in topic_lower:
                return controls
        
        # Default security controls
        return [
            "Access Controls",
            "Network Security",
            "Endpoint Protection",
            "Monitoring and Logging",
            "Incident Response",
            "Security Awareness"
        ]