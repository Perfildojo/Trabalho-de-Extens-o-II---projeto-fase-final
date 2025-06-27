import sys
from pathlib import Path
import webbrowser
import threading

def main():
    url = "http://localhost:8501"
    threading.Timer(1.5, lambda: webbrowser.open_new(url)).start()

    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "dashboard/app.py"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
