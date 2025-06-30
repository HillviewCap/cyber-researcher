"""
Threat Researcher Agent for Cyber-Researcher.

This agent focuses on threat intelligence, attack methodologies,
adversary analysis, and offensive security research from an intelligence perspective.
"""

from typing import Any, Dict, List, Optional

from .base import BaseCyberAgent, AgentRole, AgentContext, AgentResponse


class ThreatResearcherAgent(BaseCyberAgent):
    """
    Threat Researcher Agent specializing in threat intelligence and adversary analysis.
    
    This agent brings a threat intelligence perspective focused on:
    - Attack methodologies and techniques
    - Adversary tactics, techniques, and procedures (TTPs)
    - Threat actor attribution and campaigns
    - Malware analysis and indicators
    - Threat landscape evolution
    - Intelligence-driven security
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(AgentRole.THREAT_RESEARCHER, *args, **kwargs)
    
    def _get_perspective(self) -> str:
        """Return the Threat Researcher's unique perspective."""
        return "threat intelligence and adversary analysis"
    
    def _get_expertise_areas(self) -> List[str]:
        """Return the Threat Researcher's areas of expertise."""
        return [
            "Threat Intelligence",
            "Malware Analysis",
            "Attack Methodologies",
            "Adversary Attribution",
            "Threat Actor Profiling",
            "Campaign Analysis",
            "MITRE ATT&CK Framework",
            "Indicators of Compromise",
            "Threat Hunting",
            "Cyber Threat Landscape"
        ]
    
    def _get_response_style(self) -> Dict[str, Any]:
        """Return the Threat Researcher's preferred response style."""
        return {
            "tone": "investigative and analytical",
            "focus": "adversary behavior and attack patterns",
            "citations": "threat intelligence reports and IOCs",
            "examples": "real-world attack campaigns and TTPs",
            "depth": "detailed technical analysis with strategic context"
        }
    
    def analyze_topic(self, context: AgentContext) -> AgentResponse:
        """
        Analyze a cybersecurity topic from a threat intelligence perspective.
        
        Args:
            context: The analysis context
            
        Returns:
            AgentResponse with threat intelligence analysis
        """
        # Retrieve relevant threat intelligence
        threat_info = self.retrieve_information(
            f"threat intelligence {context.topic} attack campaigns malware TTPs",
            max_results=context.max_sources
        )
        
        # Build analysis prompt
        prompt = self._format_prompt(
            """
            As a {role} with expertise in {expertise}, analyze the following cybersecurity topic from a threat intelligence perspective:
            
            Topic: {topic}
            Content Type: {content_type}
            Target Audience: {audience}
            Technical Depth: {depth}
            
            Please provide a comprehensive threat intelligence analysis covering:
            1. Known threat actors and campaigns related to this topic
            2. Attack methodologies and techniques (map to MITRE ATT&CK if applicable)
            3. Indicators of compromise and detection opportunities
            4. Threat landscape evolution and trends
            5. Attribution challenges and considerations
            6. Intelligence gaps and research opportunities
            
            Focus on providing actionable threat intelligence that helps readers understand the adversary perspective.
            
            Retrieved Context:
            {context_info}
            """,
            topic=context.topic,
            content_type=context.content_type.value,
            audience=context.target_audience,
            depth=context.technical_depth,
            context_info=self._format_retrieval_context(threat_info)
        )
        
        # Generate analysis
        analysis = self._generate_response(prompt)
        
        # Extract sources
        sources = [item.get("url", "") for item in threat_info if item.get("url")]
        
        # Generate threat-specific suggestions
        suggestions = self._generate_threat_suggestions(context)
        
        return AgentResponse(
            content=analysis,
            sources=sources,
            confidence=0.88,  # High confidence in threat analysis
            suggestions=suggestions,
            metadata={
                "agent_role": self.role.value,
                "analysis_type": "threat_intelligence",
                "expertise_areas": self.expertise_areas,
                "retrieved_sources": len(threat_info),
                "threat_focus": self._identify_threat_focus(context.topic)
            }
        )
    
    def generate_questions(self, context: AgentContext) -> List[str]:
        """
        Generate threat intelligence-focused questions about a topic.
        
        Args:
            context: The context for question generation
            
        Returns:
            List of threat intelligence-focused questions
        """
        prompt = self._format_prompt(
            """
            As a {role} analyzing the cybersecurity topic "{topic}", generate 8-10 thought-provoking questions 
            that would help explore the threat intelligence aspects of this topic.
            
            Focus on questions about:
            - Threat actor motivations and capabilities
            - Attack techniques and methodologies
            - Campaign evolution and trends
            - Attribution challenges and indicators
            - Threat landscape dynamics
            - Intelligence collection and analysis
            
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
        Review content from a threat researcher perspective.
        
        Args:
            content: The content to review
            context: The review context
            
        Returns:
            AgentResponse with threat intelligence-focused feedback
        """
        prompt = self._format_prompt(
            """
            As a {role} with expertise in {expertise}, please review the following content about "{topic}":
            
            CONTENT TO REVIEW:
            {content}
            
            Please provide feedback focusing on:
            1. Accuracy of threat intelligence information
            2. Completeness of adversary perspective
            3. Currency of threat landscape information
            4. Attribution claims and evidence quality
            5. Missing threat intelligence considerations
            6. Technical accuracy of attack descriptions
            
            Provide specific, actionable feedback to improve the threat intelligence analysis.
            """,
            topic=context.topic,
            content=content
        )
        
        feedback = self._generate_response(prompt)
        
        # Generate improvement suggestions
        suggestions = [
            "Include more recent threat intelligence reports",
            "Add MITRE ATT&CK technique mappings",
            "Provide specific indicators of compromise",
            "Include threat actor attribution analysis",
            "Add campaign timeline and evolution details",
            "Reference authoritative threat intelligence sources"
        ]
        
        return AgentResponse(
            content=feedback,
            sources=[],
            confidence=0.92,  # Very high confidence in threat review
            suggestions=suggestions,
            metadata={
                "agent_role": self.role.value,
                "review_type": "threat_intelligence",
                "content_length": len(content),
                "focus_areas": ["threat_accuracy", "adversary_completeness", "intelligence_currency"]
            }
        )
    
    def _generate_threat_suggestions(self, context: AgentContext) -> List[str]:
        """Generate threat intelligence-specific suggestions for further exploration."""
        base_suggestions = [
            f"Research known threat actors targeting {context.topic}",
            f"Map attack techniques to MITRE ATT&CK framework",
            f"Analyze recent campaign trends related to {context.topic}",
            f"Investigate attribution indicators and techniques",
            f"Examine threat intelligence sharing initiatives"
        ]
        
        # Add content-type specific suggestions
        if context.content_type.value == "blog_post":
            base_suggestions.extend([
                "Include recent threat actor case studies",
                "Add interactive threat intelligence timelines",
                "Provide threat hunting guidance"
            ])
        elif context.content_type.value == "book_chapter":
            base_suggestions.extend([
                "Develop threat modeling exercises",
                "Include comprehensive IOC databases",
                "Add threat intelligence collection methodologies"
            ])
        
        return base_suggestions
    
    def _identify_threat_focus(self, topic: str) -> str:
        """Identify the primary threat focus for a given topic."""
        topic_lower = topic.lower()
        
        if any(term in topic_lower for term in ["ransomware", "crypto", "extortion"]):
            return "ransomware_groups"
        elif any(term in topic_lower for term in ["phishing", "email", "credential"]):
            return "phishing_campaigns"
        elif any(term in topic_lower for term in ["apt", "nation", "state", "government"]):
            return "advanced_persistent_threats"
        elif any(term in topic_lower for term in ["malware", "trojan", "backdoor"]):
            return "malware_families"
        elif any(term in topic_lower for term in ["supply chain", "software", "vendor"]):
            return "supply_chain_attacks"
        else:
            return "general_threats"
    
    def _format_retrieval_context(self, retrieved_info: List[Dict[str, Any]]) -> str:
        """Format retrieved information for prompt context."""
        if not retrieved_info:
            return "No additional threat intelligence retrieved."
        
        formatted = []
        for i, item in enumerate(retrieved_info[:5], 1):  # Limit to top 5
            title = item.get("title", "Unknown Threat Source")
            content = item.get("content", "")[:500]  # Limit content length
            url = item.get("url", "")
            
            formatted.append(f"Threat Intel Source {i} ({title}):\n{content}...\nURL: {url}\n")
        
        return "\n".join(formatted)
    
    def get_mitre_attack_techniques(self, topic: str) -> List[Dict[str, str]]:
        """
        Get relevant MITRE ATT&CK techniques for a specific topic.
        
        Args:
            topic: The cybersecurity topic
            
        Returns:
            List of relevant MITRE ATT&CK techniques with IDs and descriptions
        """
        techniques_map = {
            "ransomware": [
                {"id": "T1486", "name": "Data Encrypted for Impact", "tactic": "Impact"},
                {"id": "T1083", "name": "File and Directory Discovery", "tactic": "Discovery"},
                {"id": "T1490", "name": "Inhibit System Recovery", "tactic": "Impact"},
                {"id": "T1055", "name": "Process Injection", "tactic": "Defense Evasion"},
                {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution"}
            ],
            "phishing": [
                {"id": "T1566", "name": "Phishing", "tactic": "Initial Access"},
                {"id": "T1204", "name": "User Execution", "tactic": "Execution"},
                {"id": "T1056", "name": "Input Capture", "tactic": "Credential Access"},
                {"id": "T1036", "name": "Masquerading", "tactic": "Defense Evasion"},
                {"id": "T1566.001", "name": "Spearphishing Attachment", "tactic": "Initial Access"}
            ],
            "lateral_movement": [
                {"id": "T1021", "name": "Remote Services", "tactic": "Lateral Movement"},
                {"id": "T1550", "name": "Use Alternate Authentication Material", "tactic": "Lateral Movement"},
                {"id": "T1078", "name": "Valid Accounts", "tactic": "Lateral Movement"},
                {"id": "T1210", "name": "Exploitation of Remote Services", "tactic": "Lateral Movement"},
                {"id": "T1135", "name": "Network Share Discovery", "tactic": "Discovery"}
            ]
        }
        
        # Return relevant techniques or generic ones
        topic_lower = topic.lower()
        for key, techniques in techniques_map.items():
            if key in topic_lower:
                return techniques
        
        # Default techniques for general topics
        return [
            {"id": "T1566", "name": "Phishing", "tactic": "Initial Access"},
            {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution"},
            {"id": "T1055", "name": "Process Injection", "tactic": "Defense Evasion"},
            {"id": "T1083", "name": "File and Directory Discovery", "tactic": "Discovery"},
            {"id": "T1041", "name": "Exfiltration Over C2 Channel", "tactic": "Exfiltration"}
        ]
    
    def analyze_threat_actor_profile(self, actor_name: str) -> Dict[str, Any]:
        """
        Analyze a threat actor's profile and capabilities.
        
        Args:
            actor_name: Name or identifier of the threat actor
            
        Returns:
            Dictionary containing threat actor analysis
        """
        # This would typically query threat intelligence databases
        # For now, return a template structure
        return {
            "name": actor_name,
            "aliases": [],
            "motivation": "unknown",
            "sophistication": "unknown", 
            "geography": "unknown",
            "targets": [],
            "ttps": [],
            "campaigns": [],
            "tools": [],
            "attribution_confidence": "low",
            "first_observed": "unknown",
            "last_observed": "unknown"
        }