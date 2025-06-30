"""
Threat Intelligence Retrieval Module for Cyber-Researcher.

This module provides specialized retrieval capabilities for threat intelligence
reports and cybersecurity-focused content.
"""

import os
import csv
import json
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

from knowledge_storm.rm import VectorRM
from knowledge_storm.interface import Information


@dataclass
class ThreatIntelReport:
    """Structure for threat intelligence reports."""
    content: str
    title: str
    url: str
    description: str = ""
    date: str = ""
    threat_type: str = ""
    severity: str = ""
    targets: str = ""
    source: str = ""
    iocs: List[str] = None
    
    def __post_init__(self):
        if self.iocs is None:
            self.iocs = []


class ThreatIntelRM(VectorRM):
    """
    Threat Intelligence Retrieval Module.
    
    Extends STORM's VectorRM to provide specialized retrieval for
    threat intelligence reports and cybersecurity content.
    """
    
    def __init__(
        self,
        collection_name: str = "threat_intelligence",
        embedding_model: str = "BAAI/bge-m3",
        device: str = "cpu",
        k: int = 10,
        vector_store_path: Optional[str] = None,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Initialize the Threat Intelligence Retrieval Module.
        
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
        
        self.vector_store_path = vector_store_path
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        # Initialize embedding model
        self.encoder = SentenceTransformer(embedding_model, device=device)
        
        # Initialize vector store
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize the vector store (local or cloud)."""
        if self.qdrant_url and self.qdrant_api_key:
            # Cloud Qdrant
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key
            )
        elif self.vector_store_path:
            # Local Qdrant
            self.client = QdrantClient(path=self.vector_store_path)
        else:
            # In-memory Qdrant
            self.client = QdrantClient(":memory:")
        
        # Create collection if it doesn't exist
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self._create_collection()
    
    def _create_collection(self):
        """Create a new vector collection for threat intelligence."""
        vector_size = self.encoder.get_sentence_embedding_dimension()
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
    
    def ingest_threat_reports(self, reports_path: Union[str, Path]) -> int:
        """
        Ingest threat intelligence reports from a CSV file.
        
        Args:
            reports_path: Path to CSV file containing threat reports
            
        Returns:
            Number of reports ingested
        """
        reports_path = Path(reports_path)
        
        if not reports_path.exists():
            raise FileNotFoundError(f"Reports file not found: {reports_path}")
        
        # Read reports from CSV
        df = pd.read_csv(reports_path)
        
        # Validate required columns
        required_columns = ["content", "title", "url"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Process and ingest reports
        points = []
        for idx, row in df.iterrows():
            report = ThreatIntelReport(
                content=row.get("content", ""),
                title=row.get("title", ""),
                url=row.get("url", ""),
                description=row.get("description", ""),
                date=row.get("date", ""),
                threat_type=row.get("threat_type", ""),
                severity=row.get("severity", ""),
                targets=row.get("targets", ""),
                source=row.get("source", "")
            )
            
            # Create embedding
            embedding_text = self._create_embedding_text(report)
            embedding = self.encoder.encode(embedding_text).tolist()
            
            # Create point for vector store
            point = models.PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "content": report.content,
                    "title": report.title,
                    "url": report.url,
                    "description": report.description,
                    "date": report.date,
                    "threat_type": report.threat_type,
                    "severity": report.severity,
                    "targets": report.targets,
                    "source": report.source,
                    "type": "threat_intelligence"
                }
            )
            points.append(point)
        
        # Upsert points to collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return len(points)
    
    def _create_embedding_text(self, report: ThreatIntelReport) -> str:
        """Create text for embedding from threat report."""
        parts = [
            report.title,
            report.description,
            report.content[:1000],  # Limit content length
            f"Threat type: {report.threat_type}",
            f"Targets: {report.targets}"
        ]
        
        return " ".join(filter(None, parts))
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Information]:
        """
        Retrieve relevant threat intelligence information.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of Information objects
        """
        k = k or self.k
        
        # Create query embedding
        query_embedding = self.encoder.encode(query).tolist()
        
        # Search vector store
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
            with_payload=True
        )
        
        # Convert to Information objects
        information_list = []
        for hit in search_result:
            payload = hit.payload
            
            info = Information(
                snippet=payload.get("content", ""),
                title=payload.get("title", ""),
                url=payload.get("url", ""),
                meta={
                    "description": payload.get("description", ""),
                    "date": payload.get("date", ""),
                    "threat_type": payload.get("threat_type", ""),
                    "severity": payload.get("severity", ""),
                    "targets": payload.get("targets", ""),
                    "source": payload.get("source", ""),
                    "score": hit.score
                }
            )
            information_list.append(info)
        
        return information_list
    
    def retrieve_by_threat_type(self, threat_type: str, k: Optional[int] = None) -> List[Information]:
        """
        Retrieve threat intelligence by specific threat type.
        
        Args:
            threat_type: Type of threat (e.g., "ransomware", "phishing")
            k: Number of results to return
            
        Returns:
            List of Information objects
        """
        k = k or self.k
        
        # Search with filter
        search_result = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="threat_type",
                        match=models.MatchValue(value=threat_type)
                    )
                ]
            ),
            limit=k,
            with_payload=True
        )
        
        # Convert to Information objects
        information_list = []
        for hit in search_result[0]:  # scroll returns (points, next_page_offset)
            payload = hit.payload
            
            info = Information(
                snippet=payload.get("content", ""),
                title=payload.get("title", ""),
                url=payload.get("url", ""),
                meta={
                    "description": payload.get("description", ""),
                    "date": payload.get("date", ""),
                    "threat_type": payload.get("threat_type", ""),
                    "severity": payload.get("severity", ""),
                    "targets": payload.get("targets", ""),
                    "source": payload.get("source", "")
                }
            )
            information_list.append(info)
        
        return information_list
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the threat intelligence collection."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            
            # Get threat type distribution
            threat_types = self.client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Large limit to get all
                with_payload=["threat_type"]
            )[0]
            
            threat_type_counts = {}
            for point in threat_types:
                threat_type = point.payload.get("threat_type", "unknown")
                threat_type_counts[threat_type] = threat_type_counts.get(threat_type, 0) + 1
            
            return {
                "total_reports": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "threat_type_distribution": threat_type_counts
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_sample_data(self, output_path: Union[str, Path]):
        """
        Create sample threat intelligence data for testing.
        
        Args:
            output_path: Path to save the sample CSV file
        """
        sample_data = [
            {
                "content": "This ransomware campaign targets healthcare organizations using phishing emails with malicious attachments. The malware encrypts files and demands payment in cryptocurrency.",
                "title": "Healthcare Ransomware Campaign Analysis",
                "url": "https://example.com/report1",
                "description": "Analysis of targeted ransomware campaign against healthcare sector",
                "date": "2024-01-15",
                "threat_type": "ransomware",
                "severity": "high",
                "targets": "healthcare organizations",
                "source": "Security Vendor X"
            },
            {
                "content": "APT group using supply chain compromise to install backdoors in enterprise software. Long-term persistence achieved through legitimate update mechanisms.",
                "title": "Supply Chain APT Campaign",
                "url": "https://example.com/report2", 
                "description": "Advanced persistent threat using supply chain compromise",
                "date": "2024-01-20",
                "threat_type": "apt",
                "severity": "critical",
                "targets": "enterprise software users",
                "source": "Government CERT"
            },
            {
                "content": "Credential harvesting campaign using fake login pages for popular cloud services. High success rate due to convincing social engineering.",
                "title": "Cloud Service Phishing Campaign",
                "url": "https://example.com/report3",
                "description": "Phishing campaign targeting cloud service credentials", 
                "date": "2024-01-25",
                "threat_type": "phishing",
                "severity": "medium",
                "targets": "cloud service users",
                "source": "Email Security Vendor"
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_csv(output_path, index=False)
        
        return len(sample_data)