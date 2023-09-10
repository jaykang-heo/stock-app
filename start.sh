#!/bin/bash

# Navigate to backend and start FastAPI
cd backend && uvicorn main:app --reload &

# Navigate to frontend and start React app
cd frontend && npm start
