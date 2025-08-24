AI Chatbot
A sleek AI-powered chatbot built with Flask, featuring a modern, dark-mode chat interface that mimics real messaging apps.
The bot can answer questions, render Markdown, display syntax-highlighted code blocks, and even simulate a typing effect for natural conversation flow.

https://github.com/user-attachments/assets/5191db67-4224-493d-bbe0-c1eb84fc043d


✨ Features
⚡ Real-time chat powered by Flask backend & OpenRouter API
🎨 Modern Dark UI/UX (chat bubbles, avatars, smooth scrolling)
👤 User messages (right) & 🤖 Bot messages (left)
⌨️ Typing indicator for a realistic chat experience
📜 Markdown support for formatted responses
💻 Code highlighting using Highlight.js for coding answers
📱 Responsive design (works on desktop & mobile)
📂 Project Structure


AI_chatbot/
│── app.py                # Flask backend
│── .env                  # API keys (OpenRouter, Serper, etc.)
│── templates/
│    └── index.html       # Frontend UI
│── static/
│    ├── style.css        # Styles
│    └── script.js        # Client-side logic


🛠️ Tech Stack
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript
APIs: OpenRouter (AI responses), Serper (optional live search)
Libraries: Marked.js (Markdown), Highlight.js (code highlighting)
