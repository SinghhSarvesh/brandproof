"""Start API and Vite together. Install backend dependencies in .venv first."""

import os, subprocess, sys, signal
from pathlib import Path

root = Path(__file__).resolve().parents[1]
python = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
if not python.exists():
    python = Path(sys.executable)
npm = "npm.cmd" if os.name == "nt" else "npm"
processes = []


def stop(*args):
    for p in processes:
        p.terminate()
    sys.exit(0)


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    processes.append(
        subprocess.Popen(
            [
                str(python),
                "-m",
                "uvicorn",
                "app:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=root / "backend",
        )
    )
    processes.append(
        subprocess.Popen(
            [npm, "run", "dev", "--", "--port", "4173"], cwd=root / "frontend"
        )
    )
    processes[-1].wait()
finally:
    for p in processes:
        p.terminate()
