import tomli
from pathlib import Path

with open(Path(__file__).parent.parent / "pyproject.toml", 'rb') as pyproject:
    __version__ = str(tomli.load(pyproject)['tool']['poetry']['version'])
