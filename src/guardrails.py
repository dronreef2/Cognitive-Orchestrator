"""
Guardrails module for human-in-the-loop control.
Implements PAUSE functionality for mandatory human review.
"""

from typing import Optional, Callable, Dict, Any, List
from enum import Enum


class ReviewDecision(Enum):
    """Possible decisions from human review."""
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"


class HumanReviewRequired(Exception):
    """
    Exception raised when human review is required.
    This pauses the orchestration flow.
    """
    def __init__(self, content: str, context: Optional[Dict[str, Any]] = None):
        self.content = content
        self.context = context or {}
        super().__init__(f"Human review required for: {content[:100]}...")


class Guardrails:
    """
    Implements guardrails for AI orchestration.
    Provides mandatory human review checkpoints.
    """
    
    def __init__(self, auto_approve: bool = False):
        """
        Initialize guardrails.
        
        Args:
            auto_approve: If True, automatically approves content (for testing only)
        """
        self.auto_approve = auto_approve
        self.review_history = []
    
    def require_human_review(
        self,
        content: str,
        stage: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Pause execution and require human review.
        
        This is a critical checkpoint in the "Augmented Intelligence" workflow
        that prevents cognitive atrophy by ensuring human oversight.
        
        Args:
            content: The content to review
            stage: The stage/checkpoint name
            metadata: Additional metadata about the content
            
        Returns:
            Review result with decision and optional modifications
        """
        review_context = {
            "stage": stage,
            "content": content,
            "metadata": metadata or {}
        }
        
        if self.auto_approve:
            # Auto-approve for testing purposes only
            result = {
                "decision": ReviewDecision.APPROVE,
                "content": content,
                "feedback": "Auto-approved (testing mode)"
            }
            self.review_history.append(result)
            return result
        
        # In production, this would trigger actual human review
        print("\n" + "="*80)
        print(f"🛑 HUMAN REVIEW REQUIRED - Stage: {stage}")
        print("="*80)
        print(f"\nContent to review:\n{content}\n")
        print("="*80)
        
        # Get human input
        print("\nOptions:")
        print("1. Approve (continue)")
        print("2. Reject (stop)")
        print("3. Modify (provide feedback)")
        
        choice = input("\nYour decision (1/2/3): ").strip()
        
        if choice == "1":
            decision = ReviewDecision.APPROVE
            feedback = "Approved by human reviewer"
            final_content = content
        elif choice == "2":
            decision = ReviewDecision.REJECT
            feedback = input("Rejection reason: ").strip()
            final_content = content
        else:  # choice == "3" or any other input
            decision = ReviewDecision.MODIFY
            feedback = input("Modification feedback: ").strip()
            final_content = content  # In real implementation, would re-process
        
        result = {
            "decision": decision,
            "content": final_content,
            "feedback": feedback,
            "stage": stage
        }
        
        self.review_history.append(result)
        return result
    
    def validate_and_pause(
        self,
        content: str,
        stage: str,
        validators: Optional[List[Callable[[str], bool]]] = None
    ) -> str:
        """
        Validate content and pause for human review.
        
        Args:
            content: Content to validate
            stage: Current stage name
            validators: Optional list of validation functions
            
        Returns:
            Approved content (possibly modified)
            
        Raises:
            HumanReviewRequired: If review rejects the content
        """
        # Run validators if provided
        if validators:
            for validator in validators:
                if not validator(content):
                    raise ValueError(f"Validation failed at stage: {stage}")
        
        # Require human review
        review_result = self.require_human_review(content, stage)
        
        if review_result["decision"] == ReviewDecision.REJECT:
            raise HumanReviewRequired(content, {"stage": stage, "reason": review_result["feedback"]})
        
        return review_result["content"]
    
    def get_review_history(self) -> List[Dict[str, Any]]:
        """Get the history of all reviews."""
        return self.review_history.copy()
