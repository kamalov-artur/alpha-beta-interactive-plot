import os

from alpha_beta import create_app
from dotenv import load_dotenv

load_dotenv()

app, server = create_app()

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
