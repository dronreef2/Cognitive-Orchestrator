# Cognitive Orchestrator

An **Augmented Intelligence** system that orchestrates AI agents with mandatory human oversight to prevent **Cognitive Atrophy**.

## 🧠 What is Augmented Intelligence?

**Augmented Intelligence** is a design philosophy where AI systems are built to enhance and amplify human capabilities rather than replace them. Unlike fully autonomous AI that operates without human intervention, augmented intelligence:

- **Enhances** human decision-making rather than replacing it
- **Requires** human oversight at critical checkpoints
- **Preserves** human agency and judgment in the workflow
- **Combines** AI efficiency with human wisdom and ethics

This orchestrator implements augmented intelligence by using AI agents to perform time-consuming tasks (research, critique, editing) while **mandating human review** at critical decision points.

## ⚠️ Preventing Cognitive Atrophy

**Cognitive Atrophy** is the gradual loss of critical thinking skills and domain expertise that occurs when humans over-rely on automated systems without engaging their own judgment. It happens when:

- Humans blindly accept AI outputs without review
- Decision-making is delegated entirely to algorithms
- Critical thinking muscles aren't exercised
- Domain expertise fades due to lack of practice

### How This System Prevents Cognitive Atrophy

1. **Mandatory Review Checkpoints**: The workflow PAUSES for human review before proceeding
2. **Active Engagement**: Humans must evaluate AI outputs and make decisions
3. **Preserved Agency**: Final approval always rests with humans
4. **Skill Maintenance**: Regular human oversight maintains critical thinking skills
5. **Transparent Process**: Humans see each step and can intervene at any point

## 🏗️ Architecture

The system consists of four main components:

### 1. Connectors (`src/connectors.py`)
Multi-provider LLM setup supporting:
- **OpenAI** (GPT-4, GPT-3.5)
- **Gemini** (Gemini Pro)

Uses `litellm` for unified interface across providers.

### 2. Guardrails (`src/guardrails.py`)
Human-in-the-loop control system that:
- **PAUSES** execution at critical checkpoints
- Requires explicit human review and approval
- Tracks review history and decisions
- Prevents autonomous operation without oversight

### 3. Agents (`src/agents.py`)
Three specialized AI personas:

- **Researcher Agent**: Drafts comprehensive content based on research
- **Critic Agent**: Reviews and provides constructive feedback
- **Editor Agent**: Polishes content to final form

### 4. Orchestrator (`main.py`)
Chains agents together in a workflow:

```
Researcher → Critic → [HUMAN REVIEW] → Editor → Final Output
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key or Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dronreef2/Cognitive-Orchestrator.git
cd Cognitive-Orchestrator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
# Create a .env file
echo "OPENAI_API_KEY=your-key-here" > .env
# OR for Gemini
echo "GEMINI_API_KEY=your-key-here" > .env
```

### Usage

Run the orchestrator with a topic:

```bash
python main.py "The future of renewable energy"
```

Or use the default topic:

```bash
python main.py
```

### Example Workflow

```
================================================================================
  Stage 1: Researcher - Drafting Content
================================================================================

Researcher is researching and drafting...
✓ Draft completed (1247 characters)

================================================================================
  Stage 2: Critic - Reviewing Draft
================================================================================

Critic is reviewing the draft...
✓ Review completed (891 characters)

================================================================================
  Stage 3: HUMAN REVIEW CHECKPOINT
================================================================================

🛑 HUMAN REVIEW REQUIRED - Stage: Post-Critique Review

[You review the draft and critique, then decide:]
1. Approve (continue)
2. Reject (stop)
3. Modify (provide feedback)

Your decision (1/2/3): 1

✓ Human review: approve

================================================================================
  Stage 4: Editor - Polishing Content
================================================================================

Editor is polishing the final content...
✓ Editing completed (1156 characters)

✓ Orchestration completed successfully!
```

## 📁 Project Structure

```
Cognitive-Orchestrator/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── connectors.py        # Multi-provider LLM setup
│   ├── guardrails.py        # Human review & control
│   └── agents.py            # Researcher, Critic, Editor agents
├── main.py                  # Orchestration workflow
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your API credentials:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# OR Gemini
GEMINI_API_KEY=...
```

### Customization

You can customize the orchestrator by:

- **Changing providers**: Pass `provider="gemini"` to use Gemini instead of OpenAI
- **Modifying agents**: Edit `src/agents.py` to adjust agent behavior and prompts
- **Adding validators**: Add custom validation functions in `src/guardrails.py`
- **Extending workflow**: Modify `main.py` to add more stages or agents

## 🎯 Use Cases

This augmented intelligence pattern is ideal for:

- **Content Creation**: Research, write, and refine articles with human oversight
- **Decision Support**: Generate recommendations that humans review and approve
- **Code Review**: AI analyzes code, humans make final judgment
- **Research Synthesis**: AI compiles information, humans validate and direct
- **Policy Development**: AI drafts proposals, humans review and decide

## 🔒 Safety & Ethics

This system embodies several safety principles:

1. **Human-in-the-Loop**: Mandatory human review prevents runaway automation
2. **Transparency**: Each step is visible and explainable
3. **Preserved Agency**: Humans retain final decision authority
4. **Skill Preservation**: Regular engagement prevents cognitive atrophy
5. **Fail-Safe**: System cannot proceed without human approval

## 📚 Learn More

### Key Concepts

- **Augmented Intelligence**: AI as a tool to enhance human capability
- **Cognitive Atrophy**: Skill degradation from over-reliance on automation
- **Human-in-the-Loop**: Design pattern requiring human oversight
- **Agent Orchestration**: Coordinating multiple AI agents for complex tasks

### Further Reading

- [Augmented Intelligence vs Artificial Intelligence](https://www.gartner.com/en/information-technology/glossary/augmented-intelligence)
- [The Risks of Cognitive Atrophy](https://hbr.org/2023/04/ai-and-the-automation-of-work)
- [Human-in-the-Loop ML](https://www.oreilly.com/library/view/human-in-the-loop-machine/9781617296741/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [LiteLLM](https://github.com/BerriAI/litellm) - Unified LLM interface
- OpenAI GPT-4
- Google Gemini

---

**Remember**: AI should augment human intelligence, not replace it. Keep humans in the loop! 🧠✨