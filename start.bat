@echo off
title Social Media Extractor API Server
echo Starting API Server on http://127.0.0.1:8000 ...
python -m uvicorn app.main:app --reload --port 8000
pause
