import sys
import os
import django
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
import asyncio
import datetime
import pytz
from utils import update_from_czce


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        day = datetime.datetime.now().replace(tzinfo=pytz.FixedOffset(480))
        day = day - datetime.timedelta(days=1)
        loop.run_until_complete(update_from_czce(day))
        print("DONE!")
    except KeyboardInterrupt:
        pass

