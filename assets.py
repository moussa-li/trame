from pathlib import Path
from trame.assets.local import LocalFileManager

BASE = Path(__file__).parent
local_file_manager = LocalFileManager(__file__)

__all__ = [
    "loadFileToUrl"
]

def LoadFileToUrl(key, fileName):
    path = BASE / fileName
    if(path.exists()):
        return local_file_manager.url(key, path)
    return null