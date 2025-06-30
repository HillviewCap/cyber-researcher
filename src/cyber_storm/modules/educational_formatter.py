"""
Educational content formatter for Cyber-Researcher.

This module provides advanced educational formatting capabilities including
interactive elements, learning objectives tracking, and pedagogical enhancements.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import json


class LearningLevel(Enum):
    """Learning difficulty levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ContentType(Enum):
    """Types of educational content."""

    CONCEPT_EXPLANATION = "concept_explanation"
    STEP_BY_STEP_GUIDE = "step_by_step_guide"
    CASE_STUDY = "case_study"
    HANDS_ON_EXERCISE = "hands_on_exercise"
    ASSESSMENT = "assessment"
    SUMMARY = "summary"


@dataclass
class LearningObjective:
    """Represents a learning objective with measurable outcomes."""

    id: str
    description: str
    level: LearningLevel
    bloom_taxonomy_level: str  # remember, understand, apply, analyze, evaluate, create
    assessment_method: str
    success_criteria: str


@dataclass
class EducationalElement:
    """Represents an educational element within content."""

    element_type: ContentType
    title: str
    content: str
    learning_objectives: List[str]
    estimated_time: int  # minutes
    difficulty: LearningLevel
    prerequisites: List[str]
    metadata: Dict[str, Any]


class EducationalFormatter:
    """
    Advanced educational content formatter that enhances cybersecurity content
    with pedagogical features and interactive elements.
    """

    def __init__(self):
        """Initialize the educational formatter."""
        self.learning_taxonomy = {
            "remember": ["identify", "recall", "define", "list", "name"],
            "understand": ["explain", "describe", "interpret", "summarize", "compare"],
            "apply": ["implement", "demonstrate", "use", "execute", "solve"],
            "analyze": ["examine", "investigate", "categorize", "differentiate", "dissect"],
            "evaluate": ["assess", "critique", "judge", "validate", "evaluate"],
            "create": ["design", "develop", "create", "compose", "construct"],
        }

    def format_educational_content(
        self,
        content: str,
        learning_objectives: List[LearningObjective],
        target_level: LearningLevel = LearningLevel.INTERMEDIATE,
        include_assessments: bool = True,
        include_interactive: bool = True,
    ) -> str:
        """
        Format content with educational enhancements.

        Args:
            content: Raw content to format
            learning_objectives: List of learning objectives
            target_level: Target learning level
            include_assessments: Whether to include assessment elements
            include_interactive: Whether to include interactive elements

        Returns:
            Enhanced educational content
        """

        # Parse and structure content
        structured_content = self._structure_content(content, target_level)

        # Add learning objectives tracking
        enhanced_content = self._add_learning_objectives(structured_content, learning_objectives)

        # Add pedagogical elements
        enhanced_content = self._add_pedagogical_elements(enhanced_content, target_level)

        # Add knowledge checks
        if include_assessments:
            enhanced_content = self._add_knowledge_checks(enhanced_content, learning_objectives)

        # Add interactive elements
        if include_interactive:
            enhanced_content = self._add_interactive_elements(enhanced_content, target_level)

        # Add progress tracking
        enhanced_content = self._add_progress_tracking(enhanced_content, learning_objectives)

        return enhanced_content

    def _structure_content(self, content: str, level: LearningLevel) -> str:
        """Structure content based on learning level and pedagogical principles."""

        # Split content into sections
        sections = self._identify_sections(content)

        structured_sections = []
        for section in sections:
            # Add level-appropriate formatting
            formatted_section = self._format_section_for_level(section, level)

            # Add learning scaffolding
            scaffolded_section = self._add_scaffolding(formatted_section, level)

            structured_sections.append(scaffolded_section)

        return "\n\n".join(structured_sections)

    def _add_learning_objectives(self, content: str, objectives: List[LearningObjective]) -> str:
        """Add learning objectives tracking and alignment."""

        objectives_section = "## 🎯 Learning Objectives\n\n"
        objectives_section += "By completing this content, you will be able to:\n\n"

        for i, objective in enumerate(objectives, 1):
            level_indicator = self._get_level_indicator(objective.level)
            bloom_indicator = self._get_bloom_indicator(objective.bloom_taxonomy_level)

            objectives_section += f"{i}. **{objective.description}**\n"
            objectives_section += (
                f"   - *Level*: {level_indicator} {objective.level.value.title()}\n"
            )
            objectives_section += f"   - *Cognitive Level*: {bloom_indicator} {objective.bloom_taxonomy_level.title()}\n"
            objectives_section += f"   - *Assessment*: {objective.assessment_method}\n"
            objectives_section += f"   - *Success Criteria*: {objective.success_criteria}\n\n"

        # Add objective mapping throughout content
        mapped_content = self._map_objectives_to_content(content, objectives)

        return objectives_section + mapped_content

    def _add_pedagogical_elements(self, content: str, level: LearningLevel) -> str:
        """Add pedagogical elements like examples, analogies, and explanations."""

        enhanced_content = content

        # Add concept boxes for key terms
        enhanced_content = self._add_concept_boxes(enhanced_content)

        # Add examples and analogies
        enhanced_content = self._add_examples_and_analogies(enhanced_content, level)

        # Add reflection prompts
        enhanced_content = self._add_reflection_prompts(enhanced_content, level)

        # Add practical applications
        enhanced_content = self._add_practical_applications(enhanced_content)

        return enhanced_content

    def _add_knowledge_checks(self, content: str, objectives: List[LearningObjective]) -> str:
        """Add knowledge check questions throughout the content."""

        sections = content.split("\n\n")
        enhanced_sections = []

        for i, section in enumerate(sections):
            enhanced_sections.append(section)

            # Add knowledge checks after major sections
            if self._is_major_section(section) and i < len(sections) - 1:
                knowledge_check = self._generate_knowledge_check(section, objectives)
                enhanced_sections.append(knowledge_check)

        return "\n\n".join(enhanced_sections)

    def _add_interactive_elements(self, content: str, level: LearningLevel) -> str:
        """Add interactive elements like simulations, exercises, and activities."""

        enhanced_content = content

        # Add hands-on exercises
        enhanced_content = self._add_hands_on_exercises(enhanced_content, level)

        # Add scenario-based learning
        enhanced_content = self._add_scenarios(enhanced_content, level)

        # Add collaborative elements
        enhanced_content = self._add_collaborative_elements(enhanced_content)

        return enhanced_content

    def _add_progress_tracking(self, content: str, objectives: List[LearningObjective]) -> str:
        """Add progress tracking and completion indicators."""

        progress_section = """
---

## 📊 Learning Progress Tracker

Track your progress through this content:

### Completion Checklist

"""

        for i, objective in enumerate(objectives, 1):
            progress_section += f"- [ ] **Objective {i}**: {objective.description}\n"
            progress_section += f"  - [ ] Read related content\n"
            progress_section += f"  - [ ] Complete practice exercises\n"
            progress_section += f"  - [ ] Pass knowledge checks\n"
            progress_section += f"  - [ ] Apply concepts practically\n\n"

        progress_section += """
### Self-Assessment Questions

Before moving to the next topic, ask yourself:

1. **Understanding**: Can I explain the key concepts in my own words?
2. **Application**: Can I apply these concepts to real-world scenarios?
3. **Integration**: How do these concepts connect to what I already know?
4. **Confidence**: Do I feel confident using these skills in practice?

### Next Steps

- [ ] Review any areas where confidence is low
- [ ] Seek additional resources for challenging concepts
- [ ] Practice applying concepts in different contexts
- [ ] Connect with peers or mentors for discussion

---
"""

        return content + progress_section

    def _identify_sections(self, content: str) -> List[str]:
        """Identify major sections in the content."""
        # Split by markdown headers
        sections = re.split(r"\n(?=##\s)", content)
        return [section.strip() for section in sections if section.strip()]

    def _format_section_for_level(self, section: str, level: LearningLevel) -> str:
        """Format section content based on learning level."""

        if level == LearningLevel.BEGINNER:
            return self._format_for_beginner(section)
        elif level == LearningLevel.INTERMEDIATE:
            return self._format_for_intermediate(section)
        elif level == LearningLevel.ADVANCED:
            return self._format_for_advanced(section)
        else:  # EXPERT
            return self._format_for_expert(section)

    def _format_for_beginner(self, section: str) -> str:
        """Format content for beginner level."""
        # Add more explanations, simpler language, more examples
        formatted = section

        # Add beginner callouts
        if "cybersecurity" in section.lower():
            formatted += "\n\n> 💡 **For Beginners**: Cybersecurity is the practice of protecting computers, networks, and data from unauthorized access or attacks."

        return formatted

    def _format_for_intermediate(self, section: str) -> str:
        """Format content for intermediate level."""
        # Balanced approach with technical depth and practical examples
        return section

    def _format_for_advanced(self, section: str) -> str:
        """Format content for advanced level."""
        # More technical detail, complex scenarios
        formatted = section

        # Add advanced considerations
        if "## " in section:
            formatted += "\n\n### Advanced Considerations\n"
            formatted += "- Implementation complexity and edge cases\n"
            formatted += "- Integration with enterprise architectures\n"
            formatted += "- Performance and scalability implications\n"

        return formatted

    def _format_for_expert(self, section: str) -> str:
        """Format content for expert level."""
        # Highly technical, research-oriented, cutting-edge topics
        formatted = section

        # Add expert-level research references
        if "## " in section:
            formatted += "\n\n### Research and Development\n"
            formatted += "- Current research directions and open problems\n"
            formatted += "- Industry best practices and lessons learned\n"
            formatted += "- Future trends and emerging technologies\n"

        return formatted

    def _add_scaffolding(self, section: str, level: LearningLevel) -> str:
        """Add learning scaffolding based on level."""

        if level in [LearningLevel.BEGINNER, LearningLevel.INTERMEDIATE]:
            # Add more scaffolding for lower levels
            scaffolded = section

            # Add prerequisite reminders
            if "## " in section:
                scaffolded += "\n\n> 📚 **Prerequisites**: Before diving in, make sure you're familiar with basic cybersecurity concepts."

            return scaffolded

        return section

    def _add_concept_boxes(self, content: str) -> str:
        """Add concept definition boxes for key terms."""

        # Define key cybersecurity terms that need explanation
        key_terms = {
            "malware": "Malicious software designed to harm, exploit, or otherwise compromise computer systems.",
            "phishing": "A type of social engineering attack that tricks users into revealing sensitive information.",
            "zero-day": "A vulnerability in software that is unknown to security vendors and has no available patch.",
            "apt": "Advanced Persistent Threat - a sophisticated, long-term cyberattack by well-resourced adversaries.",
            "encryption": "The process of converting data into a coded format to prevent unauthorized access.",
            "firewall": "A network security device that monitors and controls incoming and outgoing network traffic.",
        }

        enhanced_content = content

        for term, definition in key_terms.items():
            # Look for first occurrence of term and add definition box
            pattern = re.compile(rf"\b{term}\b", re.IGNORECASE)
            match = pattern.search(enhanced_content)

            if match and f"**{term.title()}**" not in enhanced_content:
                concept_box = f"\n\n> 📖 **Key Concept: {term.title()}**\n> {definition}\n"

                # Insert after the paragraph containing the term
                paragraphs = enhanced_content.split("\n\n")
                for i, paragraph in enumerate(paragraphs):
                    if pattern.search(paragraph):
                        paragraphs.insert(i + 1, concept_box.strip())
                        break

                enhanced_content = "\n\n".join(paragraphs)

        return enhanced_content

    def _add_examples_and_analogies(self, content: str, level: LearningLevel) -> str:
        """Add relevant examples and analogies."""

        enhanced_content = content

        # Add analogies for complex concepts
        if "network security" in content.lower():
            analogy = """
### 🏰 Real-World Analogy: Castle Defense

Think of network security like protecting a medieval castle:

- **Firewalls** = Castle walls and gates that control who enters
- **Intrusion Detection** = Guards watching for suspicious activity  
- **Access Controls** = Keys and permissions for different areas
- **Monitoring** = Watchtowers providing visibility over the domain
- **Incident Response** = Emergency protocols when under attack

Just as a castle needs multiple layers of defense, networks require comprehensive security measures.
"""
            enhanced_content += analogy

        return enhanced_content

    def _add_reflection_prompts(self, content: str, level: LearningLevel) -> str:
        """Add reflection prompts to encourage deeper thinking."""

        prompts = [
            "\n\n🤔 **Reflection Question**: How does this concept apply to your current work environment?",
            "\n\n💭 **Think About It**: What are the potential risks if this security measure fails?",
            "\n\n🎯 **Consider This**: How would you explain this concept to a non-technical colleague?",
            "\n\n🔍 **Deep Dive**: What additional questions does this raise about cybersecurity?",
        ]

        # Add prompts at strategic points
        sections = content.split("\n\n")
        enhanced_sections = []

        for i, section in enumerate(sections):
            enhanced_sections.append(section)

            # Add reflection prompts after substantial content sections
            if len(section) > 500 and i % 3 == 2:  # Every third substantial section
                prompt_index = i % len(prompts)
                enhanced_sections.append(prompts[prompt_index])

        return "\n\n".join(enhanced_sections)

    def _add_practical_applications(self, content: str) -> str:
        """Add practical application examples."""

        applications_section = """
### 💼 Practical Applications

#### In the Workplace
- How security teams implement these concepts daily
- Common challenges and solutions in enterprise environments
- Integration with existing business processes

#### Real-World Impact
- Case studies of successful implementations
- Lessons learned from security incidents
- Industry-specific considerations

#### Personal Application
- How individuals can apply these concepts
- Home network and personal device security
- Building security awareness and skills
"""

        return content + applications_section

    def _is_major_section(self, section: str) -> bool:
        """Determine if a section is substantial enough for a knowledge check."""
        return section.startswith("##") and len(section) > 300

    def _generate_knowledge_check(self, section: str, objectives: List[LearningObjective]) -> str:
        """Generate a knowledge check based on section content."""

        knowledge_check = """
---

### ✅ Knowledge Check

Before continuing, test your understanding:

1. **Quick Review**: Can you summarize the key points from this section in 2-3 sentences?

2. **Application**: How would you apply this knowledge in a real cybersecurity scenario?

3. **Connection**: How does this information relate to the learning objectives for this content?

*Take a moment to reflect on these questions before moving forward. If you're unsure about any concepts, review the material above.*

---
"""

        return knowledge_check

    def _add_hands_on_exercises(self, content: str, level: LearningLevel) -> str:
        """Add hands-on exercises appropriate for the level."""

        exercises_section = """
### 🛠️ Hands-On Exercise

#### Exercise Setup
Choose one of the following exercises based on your current skill level:

**Beginner Exercise**: 
- Set up a home lab environment
- Practice basic security configurations
- Document your learning process

**Intermediate Exercise**:
- Analyze a cybersecurity case study
- Develop a security improvement plan
- Create implementation documentation

**Advanced Exercise**:
- Design a comprehensive security architecture
- Perform a risk assessment
- Present findings to stakeholders

#### Exercise Guidelines
1. **Preparation**: Gather necessary tools and resources
2. **Implementation**: Follow security best practices
3. **Documentation**: Record your process and findings
4. **Reflection**: Analyze what you learned and areas for improvement

#### Success Criteria
- [ ] Exercise completed successfully
- [ ] Key concepts demonstrated
- [ ] Documentation created
- [ ] Lessons learned identified
"""

        return content + exercises_section

    def _add_scenarios(self, content: str, level: LearningLevel) -> str:
        """Add scenario-based learning elements."""

        scenario_section = """
### 📋 Scenario-Based Learning

#### Scenario: Corporate Security Incident

**Background**: 
You are a cybersecurity analyst at a mid-sized financial services company. This morning, your SIEM system triggered multiple alerts indicating suspicious network activity.

**Your Task**:
Using the concepts from this content, work through this scenario:

1. **Initial Assessment**: What are your first steps?
2. **Investigation**: How would you investigate the alerts?
3. **Response**: What immediate actions would you take?
4. **Communication**: How would you communicate with stakeholders?
5. **Follow-up**: What long-term improvements would you recommend?

**Discussion Points**:
- What information would you need to make decisions?
- How do the concepts from this content apply to this situation?
- What challenges might you face in a real-world scenario?

**Extension Activities**:
- Research similar real-world incidents
- Develop standard operating procedures
- Create a presentation for management
"""

        return content + scenario_section

    def _add_collaborative_elements(self, content: str) -> str:
        """Add elements that encourage collaboration and discussion."""

        collaboration_section = """
### 👥 Collaborative Learning

#### Discussion Forum Topics
Share your thoughts and learn from others:

1. **Experience Sharing**: Have you encountered similar cybersecurity challenges?
2. **Best Practices**: What approaches have worked well in your organization?
3. **Lessons Learned**: What would you do differently based on this content?
4. **Future Trends**: How might these concepts evolve in the coming years?

#### Group Activities
Consider organizing with peers:

- **Study Groups**: Review complex concepts together
- **Case Study Analysis**: Collaborate on real-world scenarios
- **Skill Building**: Practice techniques in safe environments
- **Knowledge Sharing**: Teach concepts to reinforce your own learning

#### Professional Networking
- Connect with cybersecurity professionals
- Join relevant professional organizations
- Attend conferences and local meetups
- Participate in online communities
"""

        return content + collaboration_section

    def _map_objectives_to_content(self, content: str, objectives: List[LearningObjective]) -> str:
        """Map learning objectives to specific content sections."""

        # This is a simplified implementation
        # In practice, would use NLP to better match objectives to content

        mapped_content = content

        for i, objective in enumerate(objectives, 1):
            # Add objective references throughout content
            objective_marker = f"\n\n> 🎯 **Learning Objective {i}**: {objective.description}\n"

            # Insert markers at relevant sections (simplified logic)
            sections = mapped_content.split("\n\n")
            if len(sections) > i:
                sections.insert(i * 2, objective_marker)
                mapped_content = "\n\n".join(sections)

        return mapped_content

    def _get_level_indicator(self, level: LearningLevel) -> str:
        """Get emoji indicator for learning level."""
        indicators = {
            LearningLevel.BEGINNER: "🟢",
            LearningLevel.INTERMEDIATE: "🟡",
            LearningLevel.ADVANCED: "🟠",
            LearningLevel.EXPERT: "🔴",
        }
        return indicators.get(level, "⚪")

    def _get_bloom_indicator(self, bloom_level: str) -> str:
        """Get emoji indicator for Bloom's taxonomy level."""
        indicators = {
            "remember": "🧠",
            "understand": "💡",
            "apply": "🔧",
            "analyze": "🔍",
            "evaluate": "⚖️",
            "create": "🎨",
        }
        return indicators.get(bloom_level.lower(), "📝")

    def generate_learning_objectives(
        self, topic: str, content: str, level: LearningLevel = LearningLevel.INTERMEDIATE
    ) -> List[LearningObjective]:
        """Generate appropriate learning objectives for given content."""

        objectives = []

        # Analyze content to identify key concepts
        key_concepts = self._extract_key_concepts(content)

        # Generate objectives based on Bloom's taxonomy and learning level
        for i, concept in enumerate(key_concepts[:5], 1):  # Limit to 5 objectives

            if level == LearningLevel.BEGINNER:
                verb = "explain"
                bloom_level = "understand"
            elif level == LearningLevel.INTERMEDIATE:
                verb = "apply"
                bloom_level = "apply"
            elif level == LearningLevel.ADVANCED:
                verb = "analyze"
                bloom_level = "analyze"
            else:  # EXPERT
                verb = "evaluate"
                bloom_level = "evaluate"

            objective = LearningObjective(
                id=f"obj_{i}",
                description=f"{verb.title()} {concept} in cybersecurity contexts",
                level=level,
                bloom_taxonomy_level=bloom_level,
                assessment_method="Knowledge check and practical application",
                success_criteria=f"Demonstrate understanding of {concept} through examples and application",
            )

            objectives.append(objective)

        return objectives

    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key cybersecurity concepts from content."""

        # Common cybersecurity concepts to look for
        concepts = [
            "network security",
            "malware",
            "phishing",
            "encryption",
            "authentication",
            "authorization",
            "firewall",
            "intrusion detection",
            "incident response",
            "risk management",
            "vulnerability",
            "threat intelligence",
            "zero-day",
            "social engineering",
            "access control",
            "data protection",
            "compliance",
        ]

        found_concepts = []
        content_lower = content.lower()

        for concept in concepts:
            if concept in content_lower:
                found_concepts.append(concept)

        return found_concepts[:10]  # Return top 10
