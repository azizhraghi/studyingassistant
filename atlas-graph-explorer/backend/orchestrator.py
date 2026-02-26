from typing import Dict, Any, List
from mistralai import Mistral
from backend.agents import Agent, ProfessorAtlas, CoachRex, NovaSummarizer, ZedFlashcardForge, DrSage

class Orchestrator:
    """Manages all actively instantiated AI agents and routes user requests."""
    
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)
        self.agents: Dict[str, Agent] = {
            "professor": ProfessorAtlas(),
            "coach": CoachRex(),
            "librarian": NovaSummarizer(), # 'librarian' is the frontend ID for Nova
            "hacker": ZedFlashcardForge(), # 'hacker' is the frontend ID for Zed
            "therapist": DrSage()          # 'therapist' is the frontend ID for Sage
        }
    
    def process_request(self, avatar_id: str, message: str, mode: str, material: str = "") -> str:
        """Routes a request to the appropriate agent and returns its response."""
        
        if avatar_id not in self.agents:
            return "Error: Unknown avatar requested."
            
        agent = self.agents[avatar_id]
        
        # 1. Construct the specific mode prompt dynamically
        current_prompt = self._construct_prompt(agent, message, mode, material)
        
        # 2. Add user message to the agent's memory (so it remembers the conversation)
        # Note: We append the raw message if it's a chat, or the formatted prompt if it's an action
        display_message = message if message else f"[{mode} action initiated]"
        agent.add_to_memory("user", display_message)
        
        # 3. Get the full message array including system prompt, memory, and current prompt
        messages_payload = agent.get_messages_for_api(current_prompt)
        
        # 4. Call Mistral API
        try:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=messages_payload,
                temperature=agent.temperature,
                max_tokens=agent.max_tokens
            )
            
            ai_reply = response.choices[0].message.content
            
            # 5. Add AI response to memory
            agent.add_to_memory("assistant", ai_reply)
            
            return ai_reply
            
        except Exception as e:
            return f"Error connecting to Mistral API: {str(e)}"
            
    def reset_agent(self, avatar_id: str):
        """Clears the memory of a specific agent."""
        if avatar_id in self.agents:
            self.agents[avatar_id].reset_memory()

    def _construct_prompt(self, agent: Agent, message: str, mode: str, material: str) -> str:
        """Constructs the exact string to send based on the current UI 'mode'."""
        
        # Flashcard Forge (Zed)
        if mode == "flashcard":
            return f"Generate flashcards in raw JSON format for the following material:\n\n{material}"
            
        # Quizmaster (Coach Rex)
        if mode == "quiz":
            return f"Generate 5 quiz questions based on this material:\n\n{material}"
            
        # Summarizer (Nova)
        if mode == "auto_summary":
            return f"Create a structured Markdown summary of this material:\n\n{material}"
        if mode == "guided_summary":
            return f"I have uploaded new material. Please read it and suggest an outline so we can summarize it section by section together.\n\nMaterial:\n{material}"
            
        # Reflector (Dr. Sage)
        if mode == "reflection_start":
            return "Let's start a reflection session. I just finished studying."
        
        # Study Buddy (Prof. Atlas) — Teach Me mode
        if mode == "teach":
            # If this is the first exchange (no memory yet), the user's message IS the topic
            if len(agent.memory) == 0:
                return (
                    f"The student wants to teach you about: \"{message}\". "
                    f"You are now in 'Teach Me' mode. Act like a curious beginner who knows NOTHING about {message}. "
                    f"Ask the student to start explaining {message} to you in simple terms. "
                    f"Do NOT ask what the topic is — they just told you. Jump right in as a confused newbie."
                )
            else:
                return message
            
        # Default Chat mode (just pass the user's message)
        return message
