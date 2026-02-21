from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Accessibility Focus Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    text: str


class ActionItem(BaseModel):
    task: str
    owner: str
    priority: str
    deadline: str


class FocusSession(BaseModel):
    session_name: str
    duration_minutes: int
    instructions: List[str]
    break_minutes: int


class ProcessedOutput(BaseModel):
    simplified_text: str
    audio_narration_script: str
    visual_task_steps: List[str]
    action_items: List[ActionItem]
    guided_focus_sessions: List[FocusSession]


def call_ai_model(text: str) -> dict:
    """
    Placeholder function for AI processing.
    Replace this with actual AI API call (OpenAI, Anthropic, etc.)
    """
    api_key = os.getenv("AI_API_KEY")
    
    if not api_key:
        return generate_mock_response(text)
    
    # TODO: Implement actual AI API call here
    # Example:
    # response = openai.chat.completions.create(...)
    # return parse_ai_response(response)
    
    return generate_mock_response(text)


def generate_mock_response(text: str) -> dict:
    """Generate intelligent mock structured response for testing"""
    import re
    
    # Extract key information
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    words = text.lower()
    
    # Detect deadlines
    deadline = "Not specified"
    deadline_patterns = [
        (r'by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', lambda m: f"By {m.group(1).capitalize()}"),
        (r'by\s+(\w+\s+\d+)', lambda m: f"By {m.group(1)}"),
        (r'(tomorrow|today|tonight)', lambda m: m.group(1).capitalize()),
        (r'in\s+(\d+)\s+(day|week|hour)', lambda m: f"In {m.group(1)} {m.group(2)}s"),
        (r'(\d+)\s+(am|pm)', lambda m: f"By {m.group(1)} {m.group(2).upper()}")
    ]
    
    for pattern, formatter in deadline_patterns:
        match = re.search(pattern, words)
        if match:
            deadline = formatter(match)
            break
    
    # Detect priority keywords
    priority = "Medium"
    if any(word in words for word in ['urgent', 'asap', 'immediately', 'critical', 'important']):
        priority = "High"
    elif any(word in words for word in ['when you can', 'eventually', 'optional', 'if possible']):
        priority = "Low"
    
    # Extract action verbs and tasks
    action_verbs = ['prepare', 'create', 'write', 'send', 'submit', 'review', 'complete', 
                    'update', 'schedule', 'call', 'email', 'meet', 'present', 'analyze']
    
    detected_tasks = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for verb in action_verbs:
            if verb in sentence_lower:
                task = sentence.strip()
                if len(task) > 100:
                    task = task[:97] + "..."
                detected_tasks.append({
                    "task": task,
                    "owner": "User",
                    "priority": priority,
                    "deadline": deadline
                })
                break
    
    if not detected_tasks:
        detected_tasks = [{
            "task": sentences[0] if sentences else "Complete the described work",
            "owner": "User",
            "priority": priority,
            "deadline": deadline
        }]
    
    # Generate simplified text
    simplified_sentences = []
    for sentence in sentences[:5]:
        words_in_sentence = sentence.split()
        if len(words_in_sentence) > 15:
            chunks = [' '.join(words_in_sentence[i:i+12]) for i in range(0, len(words_in_sentence), 12)]
            simplified_sentences.extend(chunks)
        else:
            simplified_sentences.append(sentence)
    
    simplified_text = '. '.join(simplified_sentences[:6]) + '.'
    
    # Generate audio script
    audio_script = f"Hi. Let me help you understand this. {simplified_text} "
    if deadline != "Not specified":
        audio_script += f"Remember, this is due {deadline.lower()}. "
    audio_script += "Take it one step at a time. You've got this."
    
    # Generate visual steps
    visual_steps = []
    step_num = 1
    for sentence in sentences[:6]:
        if len(sentence) > 10:
            visual_steps.append(f"Step {step_num}: {sentence}")
            step_num += 1
    
    if not visual_steps:
        visual_steps = [
            "Step 1: Read the information carefully",
            "Step 2: Identify what needs to be done",
            "Step 3: Complete each task one at a time"
        ]
    
    # Generate focus sessions based on task complexity
    num_tasks = len(detected_tasks)
    sessions = []
    
    sessions.append({
        "session_name": "Planning & Understanding",
        "duration_minutes": 10 if num_tasks <= 2 else 15,
        "instructions": [
            "Find a quiet, comfortable space",
            "Read through all the information",
            "Identify the main tasks",
            "Note any questions or concerns",
            "Decide which task to start with"
        ],
        "break_minutes": 5
    })
    
    for i, task in enumerate(detected_tasks[:3], 1):
        task_name = task['task'][:40] + "..." if len(task['task']) > 40 else task['task']
        sessions.append({
            "session_name": f"Work Session {i}: {task_name}",
            "duration_minutes": 20 if task['priority'] == "High" else 15,
            "instructions": [
                f"Focus only on: {task['task']}",
                "Gather any materials you need",
                "Work at a steady pace",
                "Don't worry about perfection",
                "Save your progress regularly"
            ],
            "break_minutes": 10 if i < len(detected_tasks[:3]) else 5
        })
    
    sessions.append({
        "session_name": "Review & Wrap Up",
        "duration_minutes": 10,
        "instructions": [
            "Check what you completed",
            "Review for any errors or missing items",
            "Celebrate your progress",
            "Note anything left to do",
            "Plan your next steps if needed"
        ],
        "break_minutes": 5
    })
    
    return {
        "simplified_text": simplified_text,
        "audio_narration_script": audio_script,
        "visual_task_steps": visual_steps,
        "action_items": detected_tasks[:5],
        "guided_focus_sessions": sessions
    }


@app.get("/")
async def root():
    return {
        "message": "Accessibility Focus Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "process": "/process (POST)"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/process", response_model=ProcessedOutput)
async def process_text(input_data: TextInput):
    """
    Process input text and return accessible, structured output
    """
    if not input_data.text or len(input_data.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    
    if len(input_data.text) > 10000:
        raise HTTPException(status_code=400, detail="Text input too long (max 10000 characters)")
    
    try:
        result = call_ai_model(input_data.text)
        return ProcessedOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
