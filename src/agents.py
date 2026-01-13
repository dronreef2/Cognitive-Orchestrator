"""
Agent personas for the AI orchestration system.
Implements Researcher, Critic, and Editor agents.
"""

from typing import Optional, Dict, Any
from src.connectors import LLMConnector


class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, connector: LLMConnector, name: str, role: str):
        """
        Initialize the base agent.
        
        Args:
            connector: LLM connector to use
            name: Agent name
            role: Agent role description
        """
        self.connector = connector
        self.name = name
        self.role = role
        self.history = []
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute the agent's task.
        
        Args:
            task: The task description
            context: Optional context information
            
        Returns:
            The agent's output
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def _log_execution(self, task: str, output: str):
        """Log the execution for history tracking."""
        self.history.append({
            "task": task,
            "output": output,
            "agent": self.name
        })


class ResearcherAgent(BaseAgent):
    """
    Researcher agent that drafts initial content.
    Focuses on gathering information and creating comprehensive drafts.
    """
    
    def __init__(self, connector: LLMConnector):
        super().__init__(
            connector=connector,
            name="Researcher",
            role="Research and draft comprehensive content"
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Research and draft content based on the task.
        
        Args:
            task: The research task/topic
            context: Optional context for the research
            
        Returns:
            A comprehensive draft
        """
        system_prompt = """You are an expert Researcher agent. Your role is to:
1. Thoroughly research the given topic
2. Gather relevant information
3. Create comprehensive, well-structured drafts
4. Provide detailed and accurate content
5. Include facts, examples, and supporting evidence

Be thorough and informative in your research and drafting."""
        
        context_info = ""
        if context:
            context_info = f"\n\nAdditional context: {context}"
        
        full_prompt = f"Research and draft content for: {task}{context_info}"
        
        output = self.connector.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1500
        )
        
        self._log_execution(task, output)
        return output


class CriticAgent(BaseAgent):
    """
    Critic agent that reviews and provides feedback.
    Focuses on identifying issues, suggesting improvements, and ensuring quality.
    """
    
    def __init__(self, connector: LLMConnector):
        super().__init__(
            connector=connector,
            name="Critic",
            role="Review content and provide constructive feedback"
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Review content and provide critical feedback.
        
        Args:
            task: The content to review
            context: Optional context about the content
            
        Returns:
            Critical review and suggestions
        """
        system_prompt = """You are an expert Critic agent. Your role is to:
1. Carefully review the provided content
2. Identify strengths and weaknesses
3. Point out errors, inconsistencies, or gaps
4. Suggest specific improvements
5. Provide constructive feedback

Be thorough, fair, and constructive in your criticism."""
        
        context_info = ""
        if context:
            context_info = f"\n\nContext: {context}"
        
        full_prompt = f"Review and critique the following content:\n\n{task}{context_info}"
        
        output = self.connector.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=1200
        )
        
        self._log_execution(task, output)
        return output


class EditorAgent(BaseAgent):
    """
    Editor agent that polishes and finalizes content.
    Focuses on refining, improving clarity, and ensuring professional quality.
    """
    
    def __init__(self, connector: LLMConnector):
        super().__init__(
            connector=connector,
            name="Editor",
            role="Polish and finalize content to professional standards"
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Edit and polish content to final form.
        
        Args:
            task: The content to edit
            context: Optional context including feedback
            
        Returns:
            Polished, final content
        """
        system_prompt = """You are an expert Editor agent. Your role is to:
1. Polish and refine content
2. Improve clarity and readability
3. Ensure consistent tone and style
4. Fix grammar and formatting issues
5. Incorporate feedback and suggestions
6. Produce professional, publication-ready content

Make the content clear, concise, and compelling."""
        
        context_info = ""
        if context and "feedback" in context:
            context_info = f"\n\nFeedback to incorporate: {context['feedback']}"
        
        full_prompt = f"Edit and polish the following content:\n\n{task}{context_info}"
        
        output = self.connector.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=1500
        )
        
        self._log_execution(task, output)
        return output
