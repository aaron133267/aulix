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
