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
        self.client = anthropic.AsyncAnthropic()  # async client for non-blocking streaming
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

CURRENT INTERVIEW CONTEXT:
{json.dumps(exp.get('current_interview', {}), indent=2)}

IMPORTANT CONTEXT:
- Michelle is interviewing for the Lead Client Experience Manager role at Phreesia's Network Solutions (Life Sciences) division
- This is an HR recruiter phone screen with Katie Oyola — CULTURE/MOTIVATION/FIT conversation, NOT a deep technical interview
- Keep answers warm, concise, enthusiastic — this is about chemistry and fit
- Her KEY NARRATIVE for this role: she's been on the AGENCY/BUYER side for 15 years — she deeply understands what pharma brands and media buyers need from a partner. Now she's ready to bring that perspective to the PLATFORM side at Phreesia. This is a natural career evolution, not a departure.
- She has deep HCP (Healthcare Professional) marketing expertise across oncology, cardiovascular, infectious disease, and more
- Her key differentiators: $22M+ budget management, team of 15, Merck/Keytruda portfolio, automation innovation, deep understanding of what agency buyers look for
- If there are PRE-WRITTEN ANSWERS above that match the question, use those as the foundation but adapt to feel natural
- SALARY: The range is $250K-$270K + equity. If asked, she's comfortable in that range but should keep it brief and redirect to fit/opportunity

YOUR INSTRUCTIONS:
1. When the interviewer asks a question, immediately provide a suggested response.
2. Use the STAR method (Situation, Task, Action, Result) for behavioral questions — pull SPECIFIC examples from her Merck/Keytruda/IPG Health experience.
3. Always include concrete numbers: $22M budget, team of 15, 50% reduction in manual tracking, 100% compliance, double-digit HCP engagement increases, 15+ years experience.
4. Keep responses conversational and confident — these will be spoken aloud on a phone call, not read from a script.
5. For pharma-specific questions (regulatory, compliance, HCP targeting), lean into her deep therapeutic area knowledge.
6. If the interviewer is making small talk or a statement, suggest a brief, warm, professional reply.
7. If the question matches a PRE-WRITTEN ANSWER, use it but make it feel natural for the flow of conversation.
8. Format your response as:
   - **TYPE**: [question_type] (behavioral / technical / situational / small_talk / follow_up)
   - **SUGGESTED RESPONSE**: The actual words to say (conversational, 30-90 seconds when spoken)
   - **KEY POINTS**: 2-3 bullet points to hit if she wants to freestyle
   - **AVOID**: Anything she should NOT say (badmouthing employers, salary specifics too early, etc.)

Keep responses concise, natural, and confident. She is a senior leader — responses should reflect executive presence."""

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

        message = await self.client.messages.create(
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

        async with self.client.messages.stream(
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
            async for text in stream.text_stream:
                full_response += text
                yield text

        self.add_to_history("Suggested Response", full_response)
