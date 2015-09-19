from app import app
import logging, sys
logging.basicConfig(stream=sys.stderr)

if __name__ == "__main__":
    app.run()