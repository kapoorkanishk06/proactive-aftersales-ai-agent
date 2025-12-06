# proactive-aftersales-ai-agent
Prototype for EY Techathon 6.0 – Agentic AI Automotive Aftersales System
# Proactive Automotive Aftersales System – EY Techathon 6.0

This repository contains the working prototype for the "Proactive Automotive Aftersales System" built for EY Techathon 6.0.

## Overview
The system predicts vehicle failure risks using a rule-based engine, displays fleet health on a dashboard, and automatically books service appointments via an AI agent simulation.

## Tech Stack
- Python
- FastAPI
- Rule-based prediction engine
- HTML / CSS / JavaScript Dashboard
- SQLite (bookings & logs)

## Running the Prototype
pip install fastapi uvicorn
uvicorn main:app --reload

Then open: http://127.0.0.1:8000

## Folder Structure
- `main.py` – API & backend logic
- `data.py` – Mock telematics data + risk engine
- `static/index.html` – Frontend dashboard

## Demo Video
https://drive.google.com/drive/folders/1ehU_OpPwAM7zFmkBf5nAih9WLRnae2Ht?usp=drive_link
