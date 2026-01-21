@echo off
setlocal enabledelayedexpansion

REM 1) Install Cloudflare Tunnel (cloudflared) via Docker.
echo [1/6] Installing Cloudflare Tunnel (cloudflared) via Docker...
where docker >nul 2>nul
if errorlevel 1 (
  echo Docker not found. Installing Docker Desktop via winget...
  where winget >nul 2>nul
  if errorlevel 1 (
    echo winget not found. Please install Docker Desktop manually, then rerun this script.
    exit /b 1
  )
  winget install -e --id Docker.DockerDesktop
  echo Docker Desktop installed. Start Docker Desktop and rerun this script.
  exit /b 0
)
docker pull cloudflare/cloudflared:latest

REM 2) Verify Python is available.
echo [2/6] Checking Python...
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found. Install Python 3.11+ and rerun this script.
  exit /b 1
)

REM 3) Create/activate virtual environment.
echo [3/6] Creating virtual environment...
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate

REM 4) Install backend dependencies.
echo [4/6] Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install waitress

REM 5) Validate environment config.
echo [5/6] Checking .env configuration...
if not exist .env (
  echo .env not found. Create one with FRONTEND_ORIGIN and PORT before running the service.
)

REM 6) Next steps for secure run.
echo [6/6] Install complete.
echo To run securely on Windows, use Waitress:
echo   .venv\Scripts\waitress-serve --listen=0.0.0.0:9998 app:app
echo If you use Cloudflare Tunnel, run:
echo   docker run --rm --name cloudflared ^
echo     -v %CD%\.cloudflared:/etc/cloudflared ^
echo     cloudflare/cloudflared:latest tunnel run --token YOUR_TOKEN

endlocal
