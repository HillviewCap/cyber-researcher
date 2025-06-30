#!/usr/bin/env python3
"""
Basic usage example for Cyber-Researcher.

This script demonstrates how to use the CyberStormRunner to generate
cybersecurity content that blends historical narratives with technical analysis.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import cyber_storm
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cyber_storm import CyberStormRunner, CyberStormConfig


def main():
    """Main function demonstrating basic usage."""

    print("🚀 Cyber-Researcher Basic Usage Example")
    print("=" * 50)

    # Check if secrets.toml exists
    secrets_file = Path(__file__).parent.parent / "secrets.toml"
    if not secrets_file.exists():
        print("❌ Error: secrets.toml not found!")
        print("Please copy secrets.toml.example to secrets.toml and configure your API keys.")
        print(f"Expected location: {secrets_file}")
        return

    try:
        # Initialize configuration
        print("📋 Initializing configuration...")
        config = CyberStormConfig()

        # Initialize the runner
        print("🤖 Initializing CyberStormRunner...")
        runner = CyberStormRunner(config)

        # Get system status
        print("📊 System Status:")
        status = runner.get_system_status()

        print(
            f"  Agents: {', '.join([k for k, v in status['agents'].items() if v == 'initialized'])}"
        )
        print(
            f"  Retrieval: {', '.join([k for k, v in status['retrieval'].items() if v == 'initialized'])}"
        )
        print(f"  Output Directory: {status['output_directory']}")
        print()

        # Example 1: Generate a blog post
        print("📝 Example 1: Generating a blog post")
        print("-" * 30)

        topic = "Ransomware: Evolution and Defense Strategies"
        print(f"Topic: {topic}")

        try:
            blog_post = runner.generate_blog_post(topic, style="educational")
            print(f"✅ Blog post generated successfully!")
            print(f"   Title: {blog_post.title}")
            print(f"   Length: {len(blog_post.content)} characters")
            print(f"   Tags: {', '.join(blog_post.tags)}")
            print(f"   Sources: {len(blog_post.sources)} sources")
            print()

            # Show a snippet of the content
            print("📄 Content Preview:")
            print(
                blog_post.content[:500] + "..."
                if len(blog_post.content) > 500
                else blog_post.content
            )
            print()

        except Exception as e:
            print(f"❌ Error generating blog post: {e}")
            print()

        # Example 2: Start an interactive research session
        print("🔍 Example 2: Interactive research session")
        print("-" * 30)

        research_topic = "Supply Chain Attacks and Historical Parallels"
        print(f"Research Topic: {research_topic}")

        try:
            session = runner.interactive_research(research_topic)
            print(f"✅ Research session created: {session.session_id}")
            print(f"   Generated Questions: {len(session.generated_questions)}")
            print()

            # Show some example questions
            print("❓ Sample Research Questions:")
            for i, question in enumerate(session.generated_questions[:5], 1):
                print(f"   {i}. {question}")
            print()

        except Exception as e:
            print(f"❌ Error creating research session: {e}")
            print()

        # Example 3: Create sample data (if retrieval modules are available)
        if hasattr(runner, "threat_intel_rm") and runner.threat_intel_rm:
            print("📊 Example 3: Creating sample threat intelligence data")
            print("-" * 30)

            try:
                sample_data_path = (
                    Path(__file__).parent.parent / "data" / "threat_intel" / "sample_reports.csv"
                )
                sample_data_path.parent.mkdir(parents=True, exist_ok=True)

                # Create sample data
                num_samples = runner.threat_intel_rm.create_sample_data(sample_data_path)
                print(f"✅ Created {num_samples} sample threat intelligence reports")
                print(f"   File: {sample_data_path}")

                # Ingest the sample data
                success = runner.ingest_threat_report(str(sample_data_path))
                if success:
                    print("✅ Sample data ingested successfully")

                    # Get collection stats
                    stats = runner.threat_intel_rm.get_collection_stats()
                    print(f"   Collection Stats: {stats}")
                else:
                    print("❌ Failed to ingest sample data")
                print()

            except Exception as e:
                print(f"❌ Error with sample data: {e}")
                print()

        # Example 4: Generate a book chapter
        print("📚 Example 4: Generating a book chapter")
        print("-" * 30)

        chapter_topic = "Phishing: From Trojan Horse to Modern Social Engineering"
        learning_objectives = [
            "Understand the historical evolution of deception tactics",
            "Analyze modern phishing techniques and methodologies",
            "Develop effective defense strategies against social engineering",
            "Apply lessons from historical cases to contemporary threats",
        ]

        print(f"Chapter Topic: {chapter_topic}")
        print(f"Learning Objectives: {len(learning_objectives)} objectives")

        try:
            chapter = runner.generate_book_chapter(
                topic=chapter_topic, chapter_num=3, learning_objectives=learning_objectives
            )
            print(f"✅ Book chapter generated successfully!")
            print(f"   Title: {chapter.title}")
            print(f"   Word Count: {chapter.metadata.get('word_count', 'N/A')}")
            print(f"   Exercises: {len(chapter.exercises)}")
            print(f"   Key Concepts: {len(chapter.key_concepts)}")
            print()

        except Exception as e:
            print(f"❌ Error generating book chapter: {e}")
            print()

        print("🎉 Basic usage demonstration completed!")
        print("Check the output directory for generated files.")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
