<<<<<<< HEAD
import os
from pathlib import Path
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')
TIMEZONE = ZoneInfo(os.getenv('APP_TIMEZONE', 'America/Mexico_City'))
SLOTS = {'07:00': '07:00 – 08:30', '08:30': '08:30 – 10:00',
         '10:00': '10:00 – 11:30', '11:30': '11:30 – 13:00',
         '13:00': '13:00 – 14:30', '14:30': '14:30 – 16:00'}
=======
WINDOW_WIDTH = 905
WINDOW_HEIGHT = 646

LEFT_WIDTH = 453
RIGHT_WIDTH = WINDOW_WIDTH - LEFT_WIDTH

BACKGROUND_PATH = "assets/background.jpg"

# Colores
BLUE = "#3B82F6"
DARK_BLUE = "#234372"

TEXT_DARK = "#202B3C"
TEXT_GRAY = "#718096"

LIGHT_GRAY = "#F4F6F9"
BORDER = "#E1E7EF"

WHITE = "#FFFFFF"
>>>>>>> 6bf3e3849a767736c47c0980fc08951d3a1dba9f
