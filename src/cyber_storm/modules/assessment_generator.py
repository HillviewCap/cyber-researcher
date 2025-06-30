"""
Assessment generator for Cyber-Researcher educational content.

This module generates various types of assessments including quizzes,
practical exercises, and scenario-based evaluations.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import json


class QuestionType(Enum):
    """Types of assessment questions."""

    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    PRACTICAL = "practical"
    SCENARIO = "scenario"
    MATCHING = "matching"
    FILL_IN_BLANK = "fill_in_blank"


class DifficultyLevel(Enum):
    """Assessment difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


@dataclass
class AssessmentQuestion:
    """Represents a single assessment question."""

    id: str
    question_type: QuestionType
    difficulty: DifficultyLevel
    question_text: str
    options: Optional[List[str]] = None  # For multiple choice
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    points: int = 1
    time_limit: Optional[int] = None  # seconds
    learning_objectives: List[str] = None
    bloom_level: str = "understand"
    cybersecurity_domain: str = "general"


@dataclass
class Assessment:
    """Represents a complete assessment."""

    id: str
    title: str
    description: str
    questions: List[AssessmentQuestion]
    total_points: int
    time_limit: int  # minutes
    passing_score: int  # percentage
    metadata: Dict[str, Any]


class AssessmentGenerator:
    """
    Generates comprehensive assessments for cybersecurity education content.
    """

    def __init__(self):
        """Initialize the assessment generator."""
        self.question_templates = self._load_question_templates()
        self.cybersecurity_concepts = self._load_cybersecurity_concepts()
        self.scenario_templates = self._load_scenario_templates()

    def generate_assessment(
        self,
        topic: str,
        content: str,
        difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
        question_count: int = 10,
        question_types: Optional[List[QuestionType]] = None,
        learning_objectives: Optional[List[str]] = None,
    ) -> Assessment:
        """
        Generate a comprehensive assessment for given content.

        Args:
            topic: The main topic of the assessment
            content: The content to base questions on
            difficulty: Overall difficulty level
            question_count: Number of questions to generate
            question_types: Types of questions to include
            learning_objectives: Learning objectives to assess

        Returns:
            Complete assessment with questions and metadata
        """

        if question_types is None:
            question_types = [
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.TRUE_FALSE,
                QuestionType.SHORT_ANSWER,
                QuestionType.SCENARIO,
            ]

        # Extract key concepts from content
        key_concepts = self._extract_concepts_from_content(content)

        # Generate questions
        questions = []
        concepts_covered = set()

        for i in range(question_count):
            # Distribute question types
            question_type = question_types[i % len(question_types)]

            # Select concept to test
            available_concepts = [c for c in key_concepts if c not in concepts_covered]
            if not available_concepts:
                available_concepts = key_concepts
                concepts_covered.clear()

            concept = random.choice(available_concepts)
            concepts_covered.add(concept)

            # Generate question
            question = self._generate_question(
                question_type=question_type,
                concept=concept,
                difficulty=difficulty,
                content=content,
                question_id=f"q_{i+1}",
                learning_objectives=learning_objectives,
            )

            questions.append(question)

        # Calculate assessment metadata
        total_points = sum(q.points for q in questions)
        time_limit = self._calculate_time_limit(questions)
        passing_score = 70  # 70% default

        assessment = Assessment(
            id=f"assessment_{topic.lower().replace(' ', '_')}",
            title=f"{topic} Assessment",
            description=f"Comprehensive assessment covering key concepts in {topic}",
            questions=questions,
            total_points=total_points,
            time_limit=time_limit,
            passing_score=passing_score,
            metadata={
                "topic": topic,
                "difficulty": difficulty.value,
                "concept_coverage": list(concepts_covered),
                "question_type_distribution": {
                    qt.value: sum(1 for q in questions if q.question_type == qt)
                    for qt in question_types
                },
            },
        )

        return assessment

    def _generate_question(
        self,
        question_type: QuestionType,
        concept: str,
        difficulty: DifficultyLevel,
        content: str,
        question_id: str,
        learning_objectives: Optional[List[str]] = None,
    ) -> AssessmentQuestion:
        """Generate a single question based on parameters."""

        if question_type == QuestionType.MULTIPLE_CHOICE:
            return self._generate_multiple_choice(concept, difficulty, content, question_id)
        elif question_type == QuestionType.TRUE_FALSE:
            return self._generate_true_false(concept, difficulty, content, question_id)
        elif question_type == QuestionType.SHORT_ANSWER:
            return self._generate_short_answer(concept, difficulty, content, question_id)
        elif question_type == QuestionType.ESSAY:
            return self._generate_essay(concept, difficulty, content, question_id)
        elif question_type == QuestionType.PRACTICAL:
            return self._generate_practical(concept, difficulty, content, question_id)
        elif question_type == QuestionType.SCENARIO:
            return self._generate_scenario(concept, difficulty, content, question_id)
        elif question_type == QuestionType.MATCHING:
            return self._generate_matching(concept, difficulty, content, question_id)
        else:  # FILL_IN_BLANK
            return self._generate_fill_in_blank(concept, difficulty, content, question_id)

    def _generate_multiple_choice(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a multiple choice question."""

        templates = self.question_templates["multiple_choice"][concept]
        template = random.choice(templates.get(difficulty.value, templates["medium"]))

        question_text = template["question"].format(concept=concept)
        correct_answer = template["correct_answer"]
        distractors = template["distractors"]

        # Randomize option order
        options = [correct_answer] + distractors
        random.shuffle(options)
        correct_letter = chr(65 + options.index(correct_answer))  # A, B, C, D

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=difficulty,
            question_text=question_text,
            options=[f"{chr(65+i)}. {option}" for i, option in enumerate(options)],
            correct_answer=correct_letter,
            explanation=template.get("explanation", ""),
            points=self._get_points_for_difficulty(difficulty),
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_true_false(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a true/false question."""

        # True statement about the concept
        true_statements = {
            "malware": [
                "Malware is designed to harm or exploit computer systems",
                "Antivirus software can help detect and remove malware",
                "Malware can spread through email attachments",
            ],
            "phishing": [
                "Phishing attacks attempt to steal sensitive information",
                "Users should verify sender identity before clicking links",
                "Phishing emails often create a sense of urgency",
            ],
            "encryption": [
                "Encryption converts data into an unreadable format",
                "Strong encryption uses complex mathematical algorithms",
                "Encrypted data requires a key to decrypt",
            ],
        }

        # False statements (common misconceptions)
        false_statements = {
            "malware": [
                "Antivirus software provides 100% protection against all malware",
                "Only Windows computers can be infected with malware",
                "Malware always shows visible symptoms on infected systems",
            ],
            "phishing": [
                "Phishing attacks only target individuals, not businesses",
                "Modern email filters eliminate all phishing attempts",
                "Phishing emails are always easy to identify",
            ],
            "encryption": [
                "Encryption slows down systems significantly in all cases",
                "Only government agencies use encryption",
                "Encrypted files can never be recovered if the key is lost",
            ],
        }

        # Choose true or false
        is_true = random.choice([True, False])

        if is_true:
            statement = random.choice(
                true_statements.get(concept, ["True statement about cybersecurity"])
            )
            correct_answer = "True"
        else:
            statement = random.choice(
                false_statements.get(concept, ["False statement about cybersecurity"])
            )
            correct_answer = "False"

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.TRUE_FALSE,
            difficulty=difficulty,
            question_text=f"True or False: {statement}",
            options=["True", "False"],
            correct_answer=correct_answer,
            explanation=f"This statement is {correct_answer.lower()}.",
            points=self._get_points_for_difficulty(difficulty),
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_short_answer(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a short answer question."""

        questions = {
            "malware": {
                "easy": "What is malware and how does it affect computer systems?",
                "medium": "Describe three different types of malware and their characteristics.",
                "hard": "Analyze how malware detection techniques have evolved to address new threats.",
            },
            "phishing": {
                "easy": "What is phishing and how can users protect themselves?",
                "medium": "Explain the psychological techniques used in phishing attacks.",
                "hard": "Evaluate the effectiveness of different anti-phishing technologies.",
            },
            "encryption": {
                "easy": "What is encryption and why is it important for data security?",
                "medium": "Compare symmetric and asymmetric encryption methods.",
                "hard": "Assess the impact of quantum computing on current encryption standards.",
            },
        }

        question_text = questions.get(concept, {}).get(
            difficulty.value, f"Explain the importance of {concept} in cybersecurity."
        )

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.SHORT_ANSWER,
            difficulty=difficulty,
            question_text=question_text,
            correct_answer=None,  # Requires manual grading
            explanation="Answer should demonstrate understanding of key concepts and practical applications.",
            points=self._get_points_for_difficulty(difficulty) * 2,  # More points for open-ended
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_essay(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate an essay question."""

        essay_prompts = {
            "network security": "Analyze the evolution of network security threats and defenses over the past decade. Discuss how organizations can adapt their security strategies to address emerging challenges.",
            "incident response": "Design a comprehensive incident response plan for a medium-sized organization. Include roles, responsibilities, procedures, and success metrics.",
            "risk management": "Evaluate different approaches to cybersecurity risk management. Compare quantitative and qualitative methods and recommend best practices.",
        }

        prompt = essay_prompts.get(
            concept, f"Critically analyze the role of {concept} in modern cybersecurity strategy."
        )

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.ESSAY,
            difficulty=difficulty,
            question_text=prompt,
            correct_answer=None,  # Requires manual grading
            explanation="Essay should demonstrate critical thinking, comprehensive understanding, and practical application of concepts.",
            points=self._get_points_for_difficulty(difficulty) * 5,  # Highest points for essays
            time_limit=1800,  # 30 minutes
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_practical(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a practical exercise question."""

        practical_exercises = {
            "network security": {
                "easy": "Configure a basic firewall rule to block unauthorized access from external networks.",
                "medium": "Set up network segmentation to isolate critical systems from general user networks.",
                "hard": "Design and implement a zero-trust network architecture for a distributed organization.",
            },
            "malware analysis": {
                "easy": "Use antivirus software to scan and remove malware from a test system.",
                "medium": "Analyze malware behavior in a controlled sandbox environment.",
                "hard": "Reverse engineer a malware sample to understand its attack methodology.",
            },
            "incident response": {
                "easy": "Document the initial steps for responding to a suspected security incident.",
                "medium": "Conduct a tabletop exercise simulating a ransomware attack scenario.",
                "hard": "Lead a full-scale incident response including forensic analysis and recovery.",
            },
        }

        exercise = practical_exercises.get(concept, {}).get(
            difficulty.value, f"Complete a hands-on exercise related to {concept}."
        )

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.PRACTICAL,
            difficulty=difficulty,
            question_text=exercise,
            correct_answer=None,  # Requires practical demonstration
            explanation="Assessment based on successful completion of practical steps and demonstration of understanding.",
            points=self._get_points_for_difficulty(difficulty) * 3,
            time_limit=3600,  # 60 minutes
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_scenario(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a scenario-based question."""

        scenario = self._create_cybersecurity_scenario(concept, difficulty)

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.SCENARIO,
            difficulty=difficulty,
            question_text=scenario["description"] + "\n\nQuestion: " + scenario["question"],
            correct_answer=scenario.get("suggested_answer"),
            explanation=scenario.get("explanation", ""),
            points=self._get_points_for_difficulty(difficulty) * 3,
            time_limit=1200,  # 20 minutes
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_matching(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a matching question."""

        matching_pairs = {
            "cybersecurity_tools": {
                "Firewall": "Controls network traffic based on security rules",
                "Antivirus": "Detects and removes malicious software",
                "IDS": "Monitors network traffic for suspicious activity",
                "VPN": "Creates secure tunnel for remote connections",
                "SIEM": "Collects and analyzes security event data",
            },
            "attack_types": {
                "Phishing": "Social engineering via deceptive emails",
                "DDoS": "Overwhelming services with traffic",
                "SQL Injection": "Exploiting database vulnerabilities",
                "Man-in-the-Middle": "Intercepting communications",
                "Zero-day": "Exploiting unknown vulnerabilities",
            },
        }

        category = "cybersecurity_tools" if "tool" in concept.lower() else "attack_types"
        pairs = matching_pairs[category]

        items = list(pairs.keys())
        definitions = list(pairs.values())
        random.shuffle(definitions)

        question_text = "Match each item with its correct definition:\n\nItems:\n"
        question_text += "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
        question_text += "\n\nDefinitions:\n"
        question_text += "\n".join(
            [f"{chr(65+i)}. {definition}" for i, definition in enumerate(definitions)]
        )

        # Create answer key
        correct_matches = []
        for item in items:
            correct_def = pairs[item]
            letter = chr(65 + definitions.index(correct_def))
            correct_matches.append(f"{item}: {letter}")

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.MATCHING,
            difficulty=difficulty,
            question_text=question_text,
            correct_answer="; ".join(correct_matches),
            explanation="Match each cybersecurity concept with its correct definition.",
            points=len(items),
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _generate_fill_in_blank(
        self, concept: str, difficulty: DifficultyLevel, content: str, question_id: str
    ) -> AssessmentQuestion:
        """Generate a fill-in-the-blank question."""

        templates = {
            "encryption": "_______ is the process of converting readable data into an unreadable format to protect it from unauthorized access.",
            "firewall": "A _______ is a network security device that monitors and controls incoming and outgoing network traffic.",
            "malware": "_______ is malicious software designed to harm, exploit, or otherwise compromise computer systems.",
            "phishing": "_______ is a type of social engineering attack that uses deceptive emails to trick users into revealing sensitive information.",
        }

        template = templates.get(
            concept,
            f"_______ is an important concept in cybersecurity that helps protect systems and data.",
        )
        correct_answer = concept.title()

        return AssessmentQuestion(
            id=question_id,
            question_type=QuestionType.FILL_IN_BLANK,
            difficulty=difficulty,
            question_text=template,
            correct_answer=correct_answer,
            explanation=f"The correct answer is '{correct_answer}'.",
            points=self._get_points_for_difficulty(difficulty),
            cybersecurity_domain=self._get_domain_for_concept(concept),
        )

    def _create_cybersecurity_scenario(
        self, concept: str, difficulty: DifficultyLevel
    ) -> Dict[str, str]:
        """Create a realistic cybersecurity scenario for assessment."""

        scenarios = {
            "incident_response": {
                "easy": {
                    "description": "You arrive at work to find that several employees report their computers are running slowly and displaying pop-up advertisements. The IT help desk has received multiple similar complaints.",
                    "question": "What are your first three steps in responding to this potential security incident?",
                    "suggested_answer": "1. Isolate affected systems, 2. Document the incident, 3. Notify the security team",
                },
                "medium": {
                    "description": "Your organization's SIEM system has triggered multiple alerts indicating unusual network traffic to external IP addresses. Log analysis shows several servers connecting to unknown domains at regular intervals. Users report no performance issues.",
                    "question": "Analyze this scenario and develop an incident response plan including investigation steps and communication strategy.",
                    "suggested_answer": "Comprehensive incident response including technical analysis, stakeholder communication, and containment measures",
                },
                "hard": {
                    "description": "A sophisticated APT group has been discovered in your organization's network after 8 months of persistence. Evidence suggests data exfiltration, compromised administrative accounts, and lateral movement across multiple business units. Media attention is likely.",
                    "question": "Design a comprehensive recovery strategy addressing technical remediation, business continuity, legal considerations, and public relations.",
                    "suggested_answer": "Multi-faceted recovery strategy addressing all organizational impacts and stakeholder concerns",
                },
            },
            "risk_assessment": {
                "easy": {
                    "description": "A small accounting firm wants to allow employees to work remotely using their personal devices to access client financial data.",
                    "question": "Identify the top 3 security risks and propose basic mitigation strategies.",
                    "suggested_answer": "Data loss, unauthorized access, and device security - mitigate with VPN, MDM, and training",
                }
            },
        }

        scenario_category = "incident_response" if "incident" in concept else "risk_assessment"
        return scenarios[scenario_category].get(
            difficulty.value, scenarios[scenario_category]["medium"]
        )

    def _extract_concepts_from_content(self, content: str) -> List[str]:
        """Extract key cybersecurity concepts from content."""

        concepts = [
            "malware",
            "phishing",
            "encryption",
            "firewall",
            "authentication",
            "authorization",
            "incident response",
            "risk management",
            "vulnerability",
            "threat intelligence",
            "network security",
            "endpoint security",
            "social engineering",
            "zero-day",
            "ransomware",
            "DDoS",
            "VPN",
        ]

        found_concepts = []
        content_lower = content.lower()

        for concept in concepts:
            if concept in content_lower:
                found_concepts.append(concept)

        # Ensure we have at least some concepts
        if not found_concepts:
            found_concepts = ["cybersecurity", "information security", "data protection"]

        return found_concepts

    def _get_points_for_difficulty(self, difficulty: DifficultyLevel) -> int:
        """Get point value based on difficulty level."""
        points = {
            DifficultyLevel.EASY: 1,
            DifficultyLevel.MEDIUM: 2,
            DifficultyLevel.HARD: 3,
            DifficultyLevel.EXPERT: 5,
        }
        return points.get(difficulty, 2)

    def _get_domain_for_concept(self, concept: str) -> str:
        """Map concept to cybersecurity domain."""
        domain_mapping = {
            "malware": "threat_analysis",
            "phishing": "social_engineering",
            "encryption": "cryptography",
            "firewall": "network_security",
            "incident response": "incident_management",
            "risk management": "governance",
            "authentication": "identity_management",
            "authorization": "access_control",
        }
        return domain_mapping.get(concept, "general")

    def _calculate_time_limit(self, questions: List[AssessmentQuestion]) -> int:
        """Calculate total time limit for assessment in minutes."""
        total_seconds = sum(
            q.time_limit or self._default_time_for_question_type(q.question_type) for q in questions
        )
        return max(30, total_seconds // 60)  # Minimum 30 minutes

    def _default_time_for_question_type(self, question_type: QuestionType) -> int:
        """Get default time in seconds for question type."""
        defaults = {
            QuestionType.MULTIPLE_CHOICE: 90,
            QuestionType.TRUE_FALSE: 60,
            QuestionType.SHORT_ANSWER: 300,
            QuestionType.ESSAY: 1800,
            QuestionType.PRACTICAL: 3600,
            QuestionType.SCENARIO: 1200,
            QuestionType.MATCHING: 180,
            QuestionType.FILL_IN_BLANK: 120,
        }
        return defaults.get(question_type, 180)

    def _load_question_templates(self) -> Dict[str, Any]:
        """Load question templates for different concepts."""
        # Simplified template structure
        return {
            "multiple_choice": {
                "malware": {
                    "easy": [
                        {
                            "question": "What is {concept}?",
                            "correct_answer": "Malicious software designed to harm systems",
                            "distractors": [
                                "A type of computer hardware",
                                "A network protocol",
                                "A security certification",
                            ],
                            "explanation": "Malware is malicious software created to damage or exploit computer systems.",
                        }
                    ],
                    "medium": [
                        {
                            "question": "Which of the following is NOT a common type of {concept}?",
                            "correct_answer": "Firewall",
                            "distractors": ["Virus", "Trojan", "Ransomware"],
                            "explanation": "A firewall is a security device, not a type of malware.",
                        }
                    ],
                }
            }
        }

    def _load_cybersecurity_concepts(self) -> Dict[str, List[str]]:
        """Load cybersecurity concept hierarchies."""
        return {
            "threats": ["malware", "phishing", "social engineering", "insider threats"],
            "controls": ["firewall", "antivirus", "encryption", "authentication"],
            "processes": ["incident response", "risk management", "compliance", "auditing"],
        }

    def _load_scenario_templates(self) -> Dict[str, Any]:
        """Load scenario templates for realistic assessments."""
        return {
            "corporate_incident": "Template for corporate security incidents",
            "personal_security": "Template for personal cybersecurity scenarios",
            "compliance_audit": "Template for compliance and audit scenarios",
        }

    def format_assessment_for_web(self, assessment: Assessment) -> Dict[str, Any]:
        """Format assessment for web-based delivery."""
        return {
            "id": assessment.id,
            "title": assessment.title,
            "description": assessment.description,
            "instructions": "Read each question carefully and select the best answer.",
            "time_limit": assessment.time_limit,
            "total_points": assessment.total_points,
            "passing_score": assessment.passing_score,
            "questions": [
                {
                    "id": q.id,
                    "type": q.question_type.value,
                    "question": q.question_text,
                    "options": q.options,
                    "points": q.points,
                    "time_limit": q.time_limit,
                }
                for q in assessment.questions
            ],
            "metadata": assessment.metadata,
        }

    def format_assessment_for_print(self, assessment: Assessment) -> str:
        """Format assessment for print delivery."""
        formatted = f"# {assessment.title}\n\n"
        formatted += f"**Description**: {assessment.description}\n\n"
        formatted += f"**Time Limit**: {assessment.time_limit} minutes\n"
        formatted += f"**Total Points**: {assessment.total_points}\n"
        formatted += f"**Passing Score**: {assessment.passing_score}%\n\n"
        formatted += "---\n\n"

        for i, question in enumerate(assessment.questions, 1):
            formatted += f"## Question {i} ({question.points} points)\n\n"
            formatted += f"{question.question_text}\n\n"

            if question.options:
                for option in question.options:
                    formatted += f"{option}\n"
                formatted += "\n"

            if question.question_type in [QuestionType.SHORT_ANSWER, QuestionType.ESSAY]:
                formatted += "_" * 50 + "\n\n"
                formatted += "_" * 50 + "\n\n"

            formatted += "---\n\n"

        return formatted
