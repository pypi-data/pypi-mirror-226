import sys
import importlib

if sys.version_info < (3, 9):
    raise ImportError("The lyg library supports only Python 3.9 and above. Please upgrade your Python version.")

suffix = None
if sys.platform == "win32":
    suffix = f"cp{sys.version_info.major}{sys.version_info.minor}-win_amd64.pyd"
else:
    suffix = f"cpython-{sys.version_info.major}{sys.version_info.minor}-x86_64-linux-gnu.so"

# For module1
system_client_module = importlib.import_module(f".lyd_system_client.{suffix}", package=__package__)
system_client = system_client_module

# For module2
user_client_module = importlib.import_module(f".lyd_user_client.{suffix}", package=__package__)
user_client = user_client_module

