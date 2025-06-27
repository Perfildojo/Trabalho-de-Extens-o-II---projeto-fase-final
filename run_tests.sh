#!/bin/bash

# Terminal 1 - Bot
gnome-terminal -- python3 bot/bot.py

# Terminal 2 - Dashboard
gnome-terminal -- streamlit run dashboard/dashboard.py

echo "Sistemas iniciados!"