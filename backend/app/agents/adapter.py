import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
try:
    import anthropic
except ImportError:  # Optional: mock mode must work without the Claude SDK.
    anthropic = None

class AIResponse(BaseModel):
    content: str
    reasoning: str
    structured_data: Optional[Dict[str, Any]] = None
    is_mock: bool = False

class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str) -> AIResponse:
        pass

class ClaudeAdapter(LLMAdapter):
    def __init__(self, api_key: str):
        if anthropic is None:
            raise RuntimeError("The anthropic package is not installed; use AI_MODE=mock or install backend requirements.")
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str, system_prompt: str) -> AIResponse:
        # Simplified for prototype: in real use, we'd use tool_use or structured output
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        text = message.content[0].text
        # In a real impl, we would parse the response for reasoning and data
        return AIResponse(content=text, reasoning="Generated via Claude API", is_mock=False)

class MockAdapter(LLMAdapter):
    def generate(self, prompt: str, system_prompt: str) -> AIResponse:
        # Deterministic mock responses based on keywords in the prompt
        prompt_lower = prompt.lower()

        if "pothole" in prompt_lower:
            return AIResponse(
                content="Recommended Action: Immediate pothole filling and road surface leveling.",
                reasoning="Identified as a critical road safety hazard near a high-traffic zone.",
                structured_data={"category": "Road Safety", "severity": "High", "action": "Repair"},
                is_mock=True
            )
        elif "garbage" in prompt_lower or "waste" in prompt_lower:
            return AIResponse(
                content="Recommended Action: Schedule immediate waste collection and bin replacement.",
                reasoning="Overflowing waste creates health hazards and blockages.",
                structured_data={"category": "Waste Management", "severity": "Medium", "action": "Collection"},
                is_mock=True
            )
        elif "water" in prompt_lower or "leak" in prompt_lower:
            return AIResponse(
                content="Recommended Action: Dispatch leak detection team to isolate the burst pipe.",
                reasoning="High volume of water wastage observed; potential infrastructure risk.",
                structured_data={"category": "Water Conservation", "severity": "High", "action": "Inspection"},
                is_mock=True
            )
        elif "traffic" in prompt_lower or "congestion" in prompt_lower or "road safety" in prompt_lower or "crossing" in prompt_lower:
            return AIResponse(content="Recommended Action: Review traffic flow and share a safe alternate-route nudge for administrator approval.", reasoning="Traffic disruption reported. Suggested commute guidance is simulated and does not control traffic signals.", structured_data={"category": "Traffic Congestion", "severity": "Medium", "action": "Traffic review"}, is_mock=True)
        elif "flood" in prompt_lower or "drain" in prompt_lower:
            return AIResponse(
                content="Recommended Action: Clear drainage blockages and issue neighborhood alert.",
                reasoning="Combination of rainfall and blocked drains increases flood risk.",
                structured_data={"category": "Flood Risk", "severity": "Critical", "action": "Alert"},
                is_mock=True
            )

        return AIResponse(
            content="General action recommended based on civic guidelines.",
            reasoning="Generic incident classification.",
            structured_data={"category": "General", "severity": "Low", "action": "Review"},
            is_mock=True
        )

def get_llm_adapter():
    mode = os.getenv("AI_MODE", "mock")
    if mode == "llm":
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            print("Warning: LLM mode selected but no API key found. Falling back to mock.")
            return MockAdapter()
        return ClaudeAdapter(api_key)
    return MockAdapter()
