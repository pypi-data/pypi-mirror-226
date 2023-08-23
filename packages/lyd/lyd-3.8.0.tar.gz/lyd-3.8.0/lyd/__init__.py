import sys

if sys.version_info < (3, 9):
    raise ImportError("The lyg library supports only Python 3.9 and above. Please upgrade your Python version.")

suffix = None
if sys.platform == "win32":
    suffix = f"cp{sys.version_info.major}{sys.version_info.minor}-win_amd64.pyd"
else:
    suffix = f"cpython-{sys.version_info.major}{sys.version_info.minor}-x86_64-linux-gnu.so"

# For module1
from . import f"lyd_system_client.{suffix}" as system_client

# For module2
from . import f"lyd_user_client.{suffix}" as user_client
