import os, sys

import streamlit

import streamlit.web.cli as stcli
import shutil

streamlit_path = os.path.expanduser("~/.streamlit")

if not os.path.exists(streamlit_path):
        os.makedirs(streamlit_path)

creds = os.path.join(os.path.dirname(os.path.realpath(__file__)),"utils/data/credentials.toml")

if not os.path.isfile(os.path.join(streamlit_path, "credentials.toml")):
    shutil.copy2(creds, streamlit_path)


def resolve_path(path):
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
        # "--server.headless", "true"
    ]
    sys.exit(stcli.main())