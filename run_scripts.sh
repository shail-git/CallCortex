#!/bin/bash

# Run chat_ui.py in the background
chainlit run chat_ui_server/chat_ui.py --host 0.0.0.0 --port 80 &

# Run app.py
python fastapi_server/app.py
