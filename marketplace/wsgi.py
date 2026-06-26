import os
import sys

from django.core.wsgi import get_wsgi_application

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Load .env file for environment variables (used in production)
try:
    from dotenv import load_dotenv
    env_path = os.path.join(path, '.env')
    if os.path.isfile(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

application = get_wsgi_application()
