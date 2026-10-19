"""Run the registry locally:  python -m src.portal   then open http://localhost:5000"""
import os

from .app import create_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print(f"Demo registry: http://localhost:{port}   (fictional data only)")
    create_app().run(host="127.0.0.1", port=port, debug=False)
