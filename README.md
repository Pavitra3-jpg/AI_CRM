AI-First CRM – HCP Log Interaction Module

An AI-powered Healthcare Professional (HCP) interaction logging system** designed for **life sciences / pharmaceutical field representatives
This project enables users to log interactions with HCPs using either
Structured Form
Conversational Chat Interface
The system uses LangGraph + Groq LLM** to intelligently extract structured CRM data from natural language conversations.
Features
Dual Logging Modes
Chat-based interaction logging
Manual   structured form entry
AI-Powered Data Extraaction
Using LangGraph and Groq LLM the system extracts:
HCP Name
Interaction Type
Product Discussed
Notes / Summary
Sentiment
Concerns
Follow-up Actions

Database Storage
All logged interactions are stored in MySQL

CRM-Friendly UI
Simple and clean frontend using:
HTML
CSS
JavaScript
Google Inter Font
 Tech Stack

Frontend
HTML
CSS
JavaScript

 Backend
Python
FastAPI

AI / LLM
 LangGraph
Groq API
llama-3.3-70b-versatile

Database
 MySQL
 Project Structure

bash
AIVOA Task/
│
├── main.py
├── db.py
├── models.py
├── schemas.py
├── langgraph_agent.py
├── requirements.txt
├── .env
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
