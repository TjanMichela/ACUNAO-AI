
import streamlit

import streamlit.web.cli as stcli
import os, sys


def resolve_path(path):
    # resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    resolved_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), path))
    return resolved_path


if __name__ == "__main__":
    port = os.environ.get("PORT", 8501)
    
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("utils/app.py"),
        "--server.port", str(port),
        "--global.developmentMode=false",
        "os.devnull"
    ]
    sys.exit(stcli.main())