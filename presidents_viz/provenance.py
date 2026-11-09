import datetime, hashlib, platform
from . import __version__


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def record(inputs, config):
    return {"script": "hnd_presidents_viz", "version": __version__, "python": platform.python_version(),
            "inputs": {k: {"file": str(v), "sha256": sha256(v)} for k, v in inputs.items()},
            "config": config,
            "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
