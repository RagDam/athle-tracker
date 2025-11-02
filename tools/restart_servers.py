"""
Clean restart script for Athle Tracker servers.
Kills all existing processes and starts fresh servers.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

def kill_processes():
    """Kill all Python and Node processes."""
    print("[1/4] Arrêt de tous les processus existants...")

    try:
        # Kill Python processes
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"],
                      capture_output=True, shell=True)
        # Kill Node processes
        subprocess.run(["taskkill", "/F", "/IM", "node.exe"],
                      capture_output=True, shell=True)
        time.sleep(2)
        print("[OK] Tous les processus arrêtés\n")
    except Exception as e:
        print(f"[WARNING] Erreur lors de l'arrêt: {e}\n")

def start_backend():
    """Start FastAPI backend."""
    print("[2/4] Démarrage du backend FastAPI sur le port 8000...")

    project_root = Path(__file__).parent
    python_exe = project_root / "venv" / "Scripts" / "python.exe"

    # Start in new window
    cmd = f'start "FastAPI Backend" cmd /k "{python_exe} -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"'
    subprocess.Popen(cmd, shell=True, cwd=project_root)

    time.sleep(3)
    print("[OK] Backend démarré\n")

def start_frontend():
    """Start Next.js frontend."""
    print("[3/4] Démarrage du frontend Next.js sur le port 3000...")

    project_root = Path(__file__).parent
    frontend_dir = project_root / "frontend"

    # Start in new window with forced port 3000
    cmd = 'start "Next.js Frontend" cmd /k "npm run dev -- -p 3000"'
    subprocess.Popen(cmd, shell=True, cwd=frontend_dir)

    time.sleep(3)
    print("[OK] Frontend démarré\n")

def main():
    """Main function."""
    print("=" * 60)
    print("ATHLE TRACKER - Redémarrage des serveurs")
    print("=" * 60)
    print()

    kill_processes()
    start_backend()
    start_frontend()

    print("[4/4] Serveurs prêts!")
    print("=" * 60)
    print()
    print("FastAPI Backend:  http://localhost:8000")
    print("API Docs:         http://localhost:8000/docs")
    print("Next.js Frontend: http://localhost:3000")
    print()
    print("=" * 60)
    print()
    print("Les serveurs tournent dans des fenêtres séparées.")
    print("Fermez ces fenêtres pour arrêter les serveurs.")

if __name__ == "__main__":
    main()
