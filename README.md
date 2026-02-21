# Accessibility-First AI Focus Assistant

An accessibility-first AI assistant for people with disabilities that converts complex work content into accessible text, audio, and visual task cues, extracts action items, and generates guided focus sessions to enable inclusive task understanding and completion.

## Hackathon Track
AI for Social Good

## Project Description

An AI-powered tool that transforms complex work content into accessible, actionable workflows for people with disabilities. The assistant removes cognitive and accessibility barriers by converting meeting notes, documents, emails, and instructions into multiple accessible formats tailored for blind, deaf, and neurodivergent users.

## Problem Statement

People with disabilities face significant barriers in workplace productivity:

- Blind and low-vision users struggle with poorly formatted documents that aren't screen-reader friendly
- Deaf and hard-of-hearing users miss context from audio-only meetings
- Neurodivergent users (ADHD, dyslexia, autism) are overwhelmed by complex instructions and long blocks of text
- Traditional productivity tools assume neurotypical cognitive patterns and full sensory access

These barriers lead to:
- Increased cognitive load and mental fatigue
- Difficulty prioritizing and starting tasks
- Reduced workplace participation and productivity
- Exclusion from standard workflows

## Solution Overview

Our AI assistant processes any work-related text input and generates five accessibility-focused outputs:

1. **Simplified Text Summary** - Plain language version using short sentences and clear structure
2. **Audio Narration Script** - Calm, spoken-friendly text optimized for text-to-speech and audio playback
3. **Visual Task Cues** - Step-by-step instructions with one clear action per line
4. **Action Items Table** - Structured task list with priority, owner, and deadline
5. **Guided Focus Sessions** - Work broken into short 10-20 minute blocks with scheduled breaks

The tool is designed with universal design principles, ensuring usability for people with diverse abilities while remaining helpful for all users.

## Features

### Accessibility Features
- High contrast interface (black text on white background)
- Large, readable fonts (18px+ body text)
- Keyboard navigation support
- Screen reader compatible HTML structure
- ARIA labels and live regions
- Skip navigation links
- Focus indicators on all interactive elements

### Cognitive Support Features
- Complex content simplified into plain language
- Tasks broken into manageable steps
- Built-in break reminders
- One focus area at a time
- Supportive, non-judgmental tone
- Visual and text-based task cues

### Output Formats
- Multiple representation modes (text, audio script, visual steps)
- Structured action items with clear priorities
- Time-boxed focus sessions with breaks
- Mobile-responsive design

## Tech Stack

### Frontend
- HTML5
- CSS3 (accessible design patterns)
- Vanilla JavaScript
- Fetch API for backend communication

### Backend
- Python 3.9+
- FastAPI (REST API framework)
- Pydantic (data validation)
- Uvicorn (ASGI server)

### AI Integration
- Placeholder AI function (ready for OpenAI, Anthropic, or other LLM APIs)
- Structured prompt engineering for accessibility-first outputs
- Mock response generator for testing without API keys

## Project Structure

```
.
├── index.html                    # Frontend interface
├── main.py                       # FastAPI backend
├── accessibility_prompt.txt      # Master AI prompt
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## How to Run

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Modern web browser

### Backend Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Open `index.html` in a web browser, or serve it using a local server:
```bash
python -m http.server 3000
```

2. Navigate to `http://localhost:3000` in your browser

### Testing the Application

1. Enter sample text in the textarea:
```
You need to prepare a short presentation explaining the project progress.
Include three main points and keep the language simple.
Submit the slides by Friday evening.
After submission, send a confirmation email.
```

2. Click "Make It Accessible"

3. Review the generated accessible outputs

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /process` - Process text input and return structured output

Example API request:
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
```

## Future Enhancements

- Integration with real AI models (OpenAI GPT-4, Claude, etc.)
- Voice input for hands-free operation
- Text-to-speech audio playback
- Calendar integration for deadline tracking
- Browser extension for in-context processing
- Multi-language support
- Customizable focus session durations
- Progress tracking and completion analytics

## Accessibility Compliance

This project follows WCAG 2.1 Level AA guidelines including:
- Sufficient color contrast ratios
- Keyboard accessibility
- Screen reader compatibility
- Clear focus indicators
- Semantic HTML structure
- Descriptive labels and instructions

## License

MIT License

## Team

Built for the AI for Social Good hackathon track.

## Acknowledgments

This project is dedicated to improving workplace accessibility and supporting neurodivergent and disabled professionals in achieving their full potential.
