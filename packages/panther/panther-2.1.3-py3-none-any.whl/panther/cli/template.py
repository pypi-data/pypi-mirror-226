from datetime import datetime

from panther import version
from panther.utils import generate_secret_key

apis_py = """from datetime import datetime

from app.throttling import InfoThrottling

from panther import status, version
from panther.app import API
from panther.configs import config
from panther.request import Request
from panther.response import Response


@API()
async def hello_world_api():
    return {'detail': 'Hello World'}


@API(cache=True, throttling=InfoThrottling)
async def info_api(request: Request):
    data = {
        'version': version(),
        'datetime_now': datetime.now().isoformat(),
        'user_agent': request.headers.user_agent,
        'db_engine': config['db_engine'],
    }
    return Response(data=data, status_code=status.HTTP_202_ACCEPTED)
"""

models_py = """from panther.db import Model  # noqa: F401
"""

serializers_py = """from pydantic import BaseModel  # noqa: F401
"""

throttling_py = """from datetime import timedelta

from panther.throttling import Throttling

InfoThrottling = Throttling(rate=5, duration=timedelta(minutes=1))
"""

app_urls_py = """from app.apis import hello_world_api, info_api

urls = {
    '/': hello_world_api,
    'info/': info_api,
}
"""

configs_py = """\"""
{PROJECT_NAME} Project (Generated by Panther on %s)
\"""

from datetime import timedelta
from pathlib import Path

from panther.throttling import Throttling
from panther.utils import load_env

BASE_DIR = Path(__name__).resolve().parent
env = load_env(BASE_DIR / '.env')

SECRET_KEY = env['SECRET_KEY']

# # # More Info: Https://PantherPy.GitHub.io/middlewares/
MIDDLEWARES = [
    ('panther.middlewares.db.Middleware', {'url': f'pantherdb://{BASE_DIR}/database.pdb'}),
]

# More Info: https://PantherPy.GitHub.io/configs/#user_model
USER_MODEL = 'panther.db.models.BaseUser'

# More Info: https://PantherPy.GitHub.io/authentications/
AUTHENTICATION = 'panther.authentications.JWTAuthentication'

# More Info: https://PantherPy.GitHub.io/monitoring/
MONITORING = True

# More Info: https://PantherPy.GitHub.io/log_queries/
LOG_QUERIES = True

# More Info: https://PantherPy.GitHub.io/throttling/
THROTTLING = Throttling(rate=60, duration=timedelta(minutes=1))

# More Info: https://PantherPy.GitHub.io/urls/
URLs = 'core/urls.py'
""" % datetime.now().date().isoformat()

env = """
SECRET_KEY = '%s'
""" % generate_secret_key()

main_py = """from panther import Panther

app = Panther(__name__)
"""

urls_py = """from app.urls import urls as app_urls

urls = {
    '/': app_urls,
}
"""

git_ignore = """__pycache__/
.venv/
.idea/
logs/

.env
*.pdb
"""

requirements = """panther==%s
""" % version()

Template = {
    'app': {
        'apis.py': apis_py,
        'models.py': models_py,
        'serializers.py': serializers_py,
        'throttling.py': throttling_py,
        'urls.py': app_urls_py,
    },
    'core': {
        'configs.py': configs_py,
        'urls.py': urls_py,
    },
    'main.py': main_py,
    '.env': env,
    '.gitignore': git_ignore,
    'requirements.txt': requirements,
}
