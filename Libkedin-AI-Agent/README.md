# Linkedin_AI_Agent

This repository hosts the code for the LinkedIn AI Agent project. It automates post generation and publishing using AI and keeps a database of past posts to optimize future content.

**LinkedIn AI Agent**

A hybrid AI system that combines a deterministic workflow backbone with a bounded intelligence layer to generate, optimize, and adapt LinkedIn content based on engagement feedback.

**Core Features**

->Structured workflow orchestration

->Topic scoring engine

->LLM-based content generation

->Memory system with duplicate prevention

->Engagement tracking

->Feedback-driven optimization loop

->Adaptive posting time logic

This project demonstrates system design thinking by separating deterministic control logic from probabilistic AI-driven decision-making.

## Getting Started

1. Copy `config.example.py` to `config.py` and fill in your OpenRouter key, LinkedIn access token, and member ID.
2. Install requirements: `pip install -r requirements.txt`.
3. Run `python main.py` to start the scheduler; it will automatically generate and post to LinkedIn at the optimal hour.

Configuration and logs are printed to the console, and all post data is stored in `database/posts.db` for analysis.
