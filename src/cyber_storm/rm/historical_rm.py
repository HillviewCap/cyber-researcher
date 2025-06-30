"""
Historical Context Retrieval Module for Cyber-Researcher.

This module provides specialized retrieval capabilities for historical
events and context relevant to cybersecurity narratives.
"""

import os
import csv
import json
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from knowledge_storm.rm import VectorRM
from knowledge_storm.interface import Information


@dataclass
class HistoricalEvent:
    """Structure for historical events and context."""
    content: str
    title: str
    url: str
    description: str = ""
    date_period: str = ""
    category: str = ""
    relevance_theme: str = ""
    geographic_region: str = ""
    key_figures: str = ""
    lessons_learned: str = ""


class HistoricalRM(VectorRM):
    """
    Historical Context Retrieval Module.
    
    Extends STORM's VectorRM to provide specialized retrieval for
    historical events and context relevant to cybersecurity topics.
    """
    
    def __init__(
        self,
        collection_name: str = "historical_context",
        embedding_model: str = "BAAI/bge-m3",
        device: str = "cpu",
        k: int = 10,
        vector_store_path: Optional[str] = None,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Initialize the Historical Context Retrieval Module.
        
        Args:
            collection_name: Name of the vector collection
            embedding_model: Embedding model to use
            device: Device for model inference
            k: Number of results to retrieve
            vector_store_path: Path for local vector store
            qdrant_url: URL for cloud Qdrant instance
            qdrant_api_key: API key for cloud Qdrant
        """
        super().__init__(collection_name, embedding_model, device, k)
        
        # Initialize like ThreatIntelRM but for historical data
        self.vector_store_path = vector_store_path
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        # Default historical themes relevant to cybersecurity
        self.cybersec_themes = [
            "espionage", "intelligence", "warfare", "communication",
            "cryptography", "deception", "strategy", "technology",
            "innovation", "betrayal", "security", "trust"
        ]
    
    def find_parallels(self, query: str, k: Optional[int] = None) -> List[Information]:
        """
        Find historical parallels to a cybersecurity concept.
        
        Args:
            query: The cybersecurity concept or topic
            k: Number of parallels to return
            
        Returns:
            List of Information objects with historical parallels
        """
        k = k or self.k
        
        # Enhance query with parallel-finding keywords
        enhanced_query = f"{query} parallels analogies similar patterns history lessons"
        
        return self.retrieve(enhanced_query, k)
    
    def retrieve_by_theme(self, theme: str, k: Optional[int] = None) -> List[Information]:
        """
        Retrieve historical events by theme.
        
        Args:
            theme: Historical theme (e.g., "espionage", "warfare")
            k: Number of results to return
            
        Returns:
            List of Information objects
        """
        # This would use the same pattern as ThreatIntelRM but filter by theme
        # For now, use regular retrieve with theme-specific query
        theme_query = f"historical {theme} events examples cases"
        return self.retrieve(theme_query, k)
    
    def retrieve_by_time_period(self, period: str, k: Optional[int] = None) -> List[Information]:
        """
        Retrieve historical events from a specific time period.
        
        Args:
            period: Time period (e.g., "Cold War", "World War II", "Ancient")
            k: Number of results to return
            
        Returns:
            List of Information objects
        """
        period_query = f"{period} historical events intelligence warfare communication"
        return self.retrieve(period_query, k)
    
    def get_narrative_framework(self, cybersec_topic: str) -> Dict[str, Any]:
        """
        Get a narrative framework for a cybersecurity topic based on historical patterns.
        
        Args:
            cybersec_topic: The cybersecurity topic
            
        Returns:
            Dictionary containing narrative framework elements
        """
        # Find relevant historical parallels
        parallels = self.find_parallels(cybersec_topic, k=3)
        
        # Extract narrative elements from parallels
        framework = {
            "historical_parallels": [],
            "narrative_themes": [],
            "character_archetypes": [],
            "conflict_patterns": [],
            "resolution_strategies": []
        }
        
        for parallel in parallels:
            framework["historical_parallels"].append({
                "title": parallel.title,
                "relevance": parallel.meta.get("relevance_theme", ""),
                "lessons": parallel.meta.get("lessons_learned", "")
            })
        
        # Add default narrative elements based on topic
        topic_lower = cybersec_topic.lower()
        
        if "attack" in topic_lower or "war" in topic_lower:
            framework["narrative_themes"].extend(["conflict", "strategy", "adaptation"])
            framework["character_archetypes"].extend(["aggressor", "defender", "strategist"])
        
        if "espionage" in topic_lower or "intelligence" in topic_lower:
            framework["narrative_themes"].extend(["secrecy", "betrayal", "information"])
            framework["character_archetypes"].extend(["spy", "analyst", "double_agent"])
        
        return framework
    
    def create_sample_historical_data(self, output_path: Union[str, Path]):
        """
        Create sample historical data for testing.
        
        Args:
            output_path: Path to save the sample CSV file
        """
        sample_data = [
            {
                "content": "During World War II, the Enigma machine was used by Nazi Germany to encrypt military communications. The breaking of the Enigma code by Allied cryptographers at Bletchley Park was crucial to the war effort, demonstrating the strategic importance of cryptographic security and the devastating impact of cryptographic failure.",
                "title": "Enigma Machine and Bletchley Park",
                "url": "https://example.com/enigma",
                "description": "World War II cryptographic breakthrough",
                "date_period": "1939-1945",
                "category": "cryptography",
                "relevance_theme": "encryption security importance",
                "geographic_region": "Europe",
                "key_figures": "Alan Turing, Gordon Welchman",
                "lessons_learned": "Cryptographic security is crucial for military and strategic operations"
            },
            {
                "content": "The Trojan Horse of ancient Greek mythology and history represents one of the earliest examples of deception tactics in warfare. Greek soldiers hid inside a wooden horse presented as a gift to Troy, allowing them to infiltrate and conquer the city from within.",
                "title": "The Trojan Horse",
                "url": "https://example.com/trojan-horse", 
                "description": "Ancient deception tactic in warfare",
                "date_period": "Ancient Greece",
                "category": "deception",
                "relevance_theme": "social engineering trusted delivery",
                "geographic_region": "Mediterranean",
                "key_figures": "Odysseus",
                "lessons_learned": "Deception through trusted channels can bypass strong defenses"
            },
            {
                "content": "Benedict Arnold's betrayal during the American Revolution exemplifies the insider threat problem. As a trusted Continental Army general, Arnold attempted to surrender the strategic fort at West Point to the British, demonstrating how authorized insiders can pose the greatest security risks.",
                "title": "Benedict Arnold's Betrayal",
                "url": "https://example.com/benedict-arnold",
                "description": "Insider threat in American Revolution",
                "date_period": "1780",
                "category": "betrayal",
                "relevance_theme": "insider threat trusted access",
                "geographic_region": "North America", 
                "key_figures": "Benedict Arnold, John André",
                "lessons_learned": "Trusted insiders require continuous monitoring and loyalty verification"
            },
            {
                "content": "The Cambridge Five were a ring of British intelligence officers who secretly worked for the Soviet Union during the Cold War. Their long-term infiltration of British intelligence services provided the Soviets with crucial intelligence for decades, highlighting the challenges of detecting long-term insider threats.",
                "title": "The Cambridge Five Spy Ring",
                "url": "https://example.com/cambridge-five",
                "description": "Cold War intelligence penetration",
                "date_period": "1930s-1960s",
                "category": "espionage",
                "relevance_theme": "long-term infiltration intelligence compromise",
                "geographic_region": "United Kingdom",
                "key_figures": "Kim Philby, Guy Burgess, Donald Maclean, Anthony Blunt, John Cairncross",
                "lessons_learned": "Long-term insider threats can evade detection through careful operational security"
            },
            {
                "content": "During World War II, Operation Bernhard was a Nazi counterfeiting operation that produced fake British pounds to destabilize the British economy. This operation demonstrates early attempts at economic warfare through the compromise of trusted financial systems.",
                "title": "Operation Bernhard",
                "url": "https://example.com/operation-bernhard",
                "description": "WWII economic warfare through counterfeiting",
                "date_period": "1942-1945", 
                "category": "economic_warfare",
                "relevance_theme": "supply chain trust compromise economic",
                "geographic_region": "Europe",
                "key_figures": "Bernhard Krüger",
                "lessons_learned": "Attacks on fundamental trust systems can have wide-reaching economic impacts"
            },
            {
                "content": "The Telegraph era brought new challenges in secure long-distance communication. Diplomatic cables were often intercepted and decoded, leading to the development of diplomatic ciphers and codes. The famous Zimmermann Telegram interception helped bring the US into World War I.",
                "title": "Telegraph Security and the Zimmermann Telegram",
                "url": "https://example.com/zimmermann-telegram",
                "description": "Early electronic communication security",
                "date_period": "1917",
                "category": "communication",
                "relevance_theme": "communication interception intelligence",
                "geographic_region": "Global",
                "key_figures": "Arthur Zimmermann, Admiral Hall",
                "lessons_learned": "Electronic communications require end-to-end security considerations"
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_csv(output_path, index=False)
        
        return len(sample_data)