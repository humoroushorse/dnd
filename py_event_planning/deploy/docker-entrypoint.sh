#!/bin/sh

# alembic upgrade head
# python app/main.py
uvicorn --reload --host=0.0.0.0 --port=8002 py_event_planning.main:app
