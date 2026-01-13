"""
Main orchestration script for the Cognitive Orchestrator.

This implements an Augmented Intelligence workflow where AI agents work
collaboratively with mandatory human review checkpoints to prevent cognitive atrophy.

Workflow:
1. Researcher agent drafts content
2. Critic agent reviews the draft
3. PAUSE for mandatory human review
4. Editor agent polishes based on feedback
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

from src.connectors import get_connector
from src.guardrails import Guardrails, ReviewDecision, HumanReviewRequired
from src.agents import ResearcherAgent, CriticAgent, EditorAgent


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def run_orchestration(
    topic: str,
    provider: str = "openai",
    auto_approve: bool = False
) -> dict:
    """
    Run the full orchestration workflow.
    
    This demonstrates "Augmented Intelligence" by combining AI capabilities
    with human oversight at critical decision points.
    
    Args:
        topic: The topic to research and write about
        provider: LLM provider to use ("openai" or "gemini")
        auto_approve: If True, auto-approves reviews (testing only)
        
    Returns:
        Dictionary with workflow results
    """
    print_header("Cognitive Orchestrator - Augmented Intelligence Workflow")
    print(f"Topic: {topic}")
    print(f"Provider: {provider}")
    print(f"Auto-approve mode: {auto_approve}")
    
    # Initialize components
    print("\n🔧 Initializing components...")
    connector = get_connector(provider=provider)
    guardrails = Guardrails(auto_approve=auto_approve)
    
    researcher = ResearcherAgent(connector)
    critic = CriticAgent(connector)
    editor = EditorAgent(connector)
    
    workflow_results = {
        "topic": topic,
        "stages": {}
    }
    
    # Stage 1: Researcher drafts content
    print_header("Stage 1: Researcher - Drafting Content")
    print(f"{researcher.name} is researching and drafting...")
    
    try:
        draft = researcher.execute(topic)
        print(f"\n✓ Draft completed ({len(draft)} characters)")
        workflow_results["stages"]["research"] = {
            "agent": researcher.name,
            "output": draft
        }
        
        # Display draft preview
        print("\n--- Draft Preview ---")
        print(draft[:300] + "..." if len(draft) > 300 else draft)
        print("--- End Preview ---\n")
        
    except Exception as e:
        print(f"\n✗ Error during research: {e}")
        workflow_results["error"] = str(e)
        return workflow_results
    
    # Stage 2: Critic reviews the draft
    print_header("Stage 2: Critic - Reviewing Draft")
    print(f"{critic.name} is reviewing the draft...")
    
    try:
        critique = critic.execute(draft, context={"topic": topic})
        print(f"\n✓ Review completed ({len(critique)} characters)")
        workflow_results["stages"]["critique"] = {
            "agent": critic.name,
            "output": critique
        }
        
        # Display critique preview
        print("\n--- Critique Preview ---")
        print(critique[:300] + "..." if len(critique) > 300 else critique)
        print("--- End Preview ---\n")
        
    except Exception as e:
        print(f"\n✗ Error during critique: {e}")
        workflow_results["error"] = str(e)
        return workflow_results
    
    # Stage 3: MANDATORY Human Review - Critical checkpoint!
    print_header("Stage 3: HUMAN REVIEW CHECKPOINT")
    print("This is a critical step in preventing cognitive atrophy.")
    print("Human oversight ensures quality and maintains human agency.\n")
    
    try:
        review_content = f"DRAFT:\n{draft}\n\nCRITIQUE:\n{critique}"
        review_result = guardrails.require_human_review(
            content=review_content,
            stage="Post-Critique Review",
            metadata={
                "topic": topic,
                "draft_length": len(draft),
                "critique_length": len(critique)
            }
        )
        
        workflow_results["stages"]["human_review"] = review_result
        
        # Handle review decision
        if review_result["decision"] == ReviewDecision.REJECT:
            print("\n✗ Content rejected by human reviewer")
            print(f"Reason: {review_result['feedback']}")
            workflow_results["status"] = "rejected"
            return workflow_results
        
        print(f"\n✓ Human review: {review_result['decision'].value}")
        print(f"Feedback: {review_result['feedback']}")
        
    except HumanReviewRequired as e:
        print(f"\n✗ Human review rejected: {e}")
        workflow_results["error"] = str(e)
        workflow_results["status"] = "rejected"
        return workflow_results
    except Exception as e:
        print(f"\n✗ Error during human review: {e}")
        workflow_results["error"] = str(e)
        return workflow_results
    
    # Stage 4: Editor polishes the content
    print_header("Stage 4: Editor - Polishing Content")
    print(f"{editor.name} is polishing the final content...")
    
    try:
        final_content = editor.execute(
            draft,
            context={
                "feedback": critique,
                "human_feedback": review_result["feedback"]
            }
        )
        print(f"\n✓ Editing completed ({len(final_content)} characters)")
        workflow_results["stages"]["editing"] = {
            "agent": editor.name,
            "output": final_content
        }
        workflow_results["final_content"] = final_content
        workflow_results["status"] = "completed"
        
        # Display final content
        print_header("FINAL OUTPUT")
        print(final_content)
        
    except Exception as e:
        print(f"\n✗ Error during editing: {e}")
        workflow_results["error"] = str(e)
        return workflow_results
    
    # Summary
    print_header("Workflow Summary")
    print(f"Status: {workflow_results['status'].upper()}")
    print(f"Total stages completed: {len(workflow_results['stages'])}")
    print(f"Final content length: {len(workflow_results.get('final_content', ''))} characters")
    
    review_history = guardrails.get_review_history()
    print(f"Human reviews conducted: {len(review_history)}")
    
    return workflow_results


def main():
    """Main entry point for the Cognitive Orchestrator."""
    # Load environment variables (for API keys)
    load_dotenv()
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Warning: No API keys found in environment variables.")
        print("Please set OPENAI_API_KEY or GEMINI_API_KEY in your .env file.")
        print("\nExample .env file:")
        print("OPENAI_API_KEY=your-key-here")
        print("# or")
        print("GEMINI_API_KEY=your-key-here")
        print("\nRunning in demo mode with auto-approve enabled.")
        auto_approve = True
    else:
        auto_approve = False
    
    # Get topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "The importance of human oversight in AI systems"
    
    # Determine provider
    provider = "openai"  # Default
    if os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        provider = "gemini"
    
    # Run the orchestration
    try:
        results = run_orchestration(
            topic=topic,
            provider=provider,
            auto_approve=auto_approve
        )
        
        # Exit with appropriate code
        if results.get("status") == "completed":
            print("\n✓ Orchestration completed successfully!")
            sys.exit(0)
        else:
            print("\n✗ Orchestration did not complete.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Orchestration interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
