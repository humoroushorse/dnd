#!/bin/sh

# alembic upgrade head
# python app/main.py
uvicorn --reload --host=0.0.0.0 --port=8001 py_dnd.main:app
