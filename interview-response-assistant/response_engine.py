"""
AI-powered response engine that generates interview answer suggestions
based on the user's experience profile and the transcribed conversation.
"""

import json
import os
from pathlib import Path

import anthropic


class ResponseEngine:
    """Generates real-time interview response suggestions using Claude."""

    def __init__(self, experience_path: str = "experience.json"):
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
        self.experience = self._load_experience(experience_path)
        self.conversation_history: list[dict] = []
        self.system_prompt = self._build_system_prompt()

    def _load_experience(self, path: str) -> dict:
        """Load the user's experience profile from JSON."""
        filepath = Path(__file__).parent / path
        with open(filepath) as f:
            return json.load(f)

    def _build_system_prompt(self) -> str:
        exp = self.experience
        return f"""You are a real-time interview coach. You are listening to a live phone interview and providing suggested responses for the candidate.

CANDIDATE PROFILE:
Name: {exp.get('name', 'N/A')}
Title: {exp.get('title', 'N/A')}
Summary: {exp.get('summary', 'N/A')}

WORK EXPERIENCE:
{json.dumps(exp.get('work_experience', []), indent=2)}

SKILLS:
{json.dumps(exp.get('skills', {}), indent=2)}

EDUCATION:
{json.dumps(exp.get('education', []), indent=2)}

KEY ACHIEVEMENTS:
{json.dumps(exp.get('achievements', []), indent=2)}

PROJECTS:
{json.dumps(exp.get('projects', []), indent=2)}

VALUES & MOTIVATIONS:
{json.dumps(exp.get('values_and_motivations', []), indent=2)}

PRE-WRITTEN ANSWERS:
{json.dumps(exp.get('common_answers', {}), indent=2)}

YOUR INSTRUCTIONS:
1. When the interviewer asks a question, immediately provide a suggested response.
2. Use the STAR method (Situation, Task, Action, Result) for behavioral questions.
3. Pull specific examples from the candidate's experience above.
4. Keep responses conversational - these will be spoken aloud, not read.
5. Include specific numbers and metrics from the experience when relevant.
6. If the interviewer is making small talk or a statement, note that no response is needed OR suggest a brief, natural reply.
7. Format your response as:
   - **TYPE**: [question_type] (behavioral / technical / situational / small_talk / follow_up)
   - **SUGGESTED RESPONSE**: The actual words to say
   - **KEY POINTS**: 2-3 bullet points to hit if candidate wants to freestyle
   - **AVOID**: Anything the candidate should NOT say

Keep responses concise and natural-sounding. The candidate needs to speak these words in real-time."""

    def add_to_history(self, speaker: str, text: str):
        """Track conversation history for context."""
        self.conversation_history.append({"speaker": speaker, "text": text})
        # Keep last 20 exchanges for context window management
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    async def generate_response(self, interviewer_text: str) -> str:
        """
        Generate a suggested response based on what the interviewer just said.

        Returns the full suggestion text with type, response, key points, etc.
        """
        self.add_to_history("Interviewer", interviewer_text)

        # Build the conversation context
        context_lines = []
        for entry in self.conversation_history:
            context_lines.append(f"{entry['speaker']}: {entry['text']}")
        conversation_context = "\n".join(context_lines)

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""LIVE INTERVIEW TRANSCRIPT SO FAR:
{conversation_context}

The interviewer just said: "{interviewer_text}"

Provide a suggested response for the candidate to say RIGHT NOW. Be concise and natural.""",
                }
            ],
        )

        response_text = message.content[0].text
        self.add_to_history("Suggested Response", response_text)
        return response_text

    async def generate_response_stream(self, interviewer_text: str):
        """
        Stream a suggested response token-by-token for faster display.

        Yields text chunks as they arrive from the API.
        """
        self.add_to_history("Interviewer", interviewer_text)

        context_lines = []
        for entry in self.conversation_history:
            context_lines.append(f"{entry['speaker']}: {entry['text']}")
        conversation_context = "\n".join(context_lines)

        full_response = ""

        with self.client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""LIVE INTERVIEW TRANSCRIPT SO FAR:
{conversation_context}

The interviewer just said: "{interviewer_text}"

Provide a suggested response for the candidate to say RIGHT NOW. Be concise and natural.""",
                }
            ],
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                yield text

        self.add_to_history("Suggested Response", full_response)
