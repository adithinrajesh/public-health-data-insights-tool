# src/logging_setup.py
import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_PATH, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_PATH, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="a"
)

logger = logging.getLogger("HealthDataApp")
