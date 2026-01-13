#!/usr/bin/env python3
"""
Example demonstrating the Cognitive Orchestrator workflow.
This showcases the Augmented Intelligence pattern.
"""

import sys
sys.path.insert(0, '.')

from src.connectors import get_connector
from src.guardrails import Guardrails
from src.agents import ResearcherAgent, CriticAgent, EditorAgent

def example_workflow():
    """Demonstrate the orchestration workflow in auto-approve mode."""
    
    print("="*80)
    print("COGNITIVE ORCHESTRATOR - DEMONSTRATION")
    print("="*80)
    print("\nThis demonstrates the Augmented Intelligence workflow:")
    print("1. AI agents perform tasks (research, critique, edit)")
    print("2. Human oversight prevents cognitive atrophy")
    print("3. Final decisions remain with humans\n")
    
    # Initialize components (in demo mode - no actual API calls)
    print("Setting up components...")
    connector = get_connector(provider="openai", model="gpt-4")
    guardrails = Guardrails(auto_approve=True)  # Auto-approve for demo
    
    researcher = ResearcherAgent(connector)
    critic = CriticAgent(connector)
    editor = EditorAgent(connector)
    
    print(f"✓ Connector: {connector}")
    print(f"✓ Agents: {researcher.name}, {critic.name}, {editor.name}")
    print(f"✓ Guardrails: Configured with auto-approve for demo\n")
    
    # Demonstrate guardrails (human review checkpoint)
    print("-" * 80)
    print("DEMONSTRATING HUMAN REVIEW CHECKPOINT")
    print("-" * 80)
    
    sample_content = """
    Draft: AI systems should augment human intelligence.
    
    Critique: This draft is good but could be more specific about implementation.
    """
    
    print("\nContent to review:")
    print(sample_content)
    
    result = guardrails.require_human_review(
        content=sample_content,
        stage="Example Review",
        metadata={"demo": True}
    )
    
    print(f"\n✓ Review decision: {result['decision'].value}")
    print(f"✓ Feedback: {result['feedback']}")
    
    # Show review history
    history = guardrails.get_review_history()
    print(f"\n✓ Review history: {len(history)} review(s) recorded")
    
    print("\n" + "="*80)
    print("KEY CONCEPTS DEMONSTRATED")
    print("="*80)
    print("""
1. AUGMENTED INTELLIGENCE:
   - AI performs time-consuming tasks (research, critique, editing)
   - Humans make final decisions and provide oversight
   - Combines AI efficiency with human wisdom
   
2. PREVENTING COGNITIVE ATROPHY:
   - Mandatory human review checkpoints
   - Active engagement required from humans
   - Critical thinking skills maintained
   - Humans remain in control
   
3. WORKFLOW STRUCTURE:
   Researcher → Critic → [HUMAN REVIEW] → Editor → Output
   
The PAUSE at the human review checkpoint is critical - it ensures
humans remain engaged and prevents blind acceptance of AI outputs.
""")
    
    print("\n✓ Demonstration complete!")
    print("\nTo run with actual LLM calls, set your API key:")
    print("  export OPENAI_API_KEY='your-key'")
    print("  python main.py \"Your topic here\"")

if __name__ == "__main__":
    example_workflow()
