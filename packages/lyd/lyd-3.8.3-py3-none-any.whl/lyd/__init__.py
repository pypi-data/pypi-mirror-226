import sys
import importlib.util
import os

if sys.version_info < (3, 9):
    raise ImportError("The lyg library supports only Python 3.9 and above. Please upgrade your Python version.")

suffix = None
if sys.platform == "win32":
    suffix = f"cp{sys.version_info.major}{sys.version_info.minor}-win_amd64.pyd"
else:
    suffix = f"cpython-{sys.version_info.major}{sys.version_info.minor}-x86_64-linux-gnu.so"

# Dynamic import for lyd_system_client
system_client_path = os.path.join(os.path.dirname(__file__), f"lyd_system_client.{suffix}")
spec = importlib.util.spec_from_file_location("system_client", system_client_path)
system_client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(system_client)

# Dynamic import for lyd_user_client
user_client_path = os.path.join(os.path.dirname(__file__), f"lyd_user_client.{suffix}")
spec = importlib.util.spec_from_file_location("user_client", user_client_path)
user_client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(user_client)

