import logging 
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True ,exist_ok=True)

log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

logging.basicConfig(
    filename=log_file,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    level=logging.INFO,
)

def info(message: str):
    logging.info(message)

def error(message: str):
    logging.error(message)    