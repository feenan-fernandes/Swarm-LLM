@echo off
echo ============================================================
echo   STARTING SWARM IDE & AUTONOMOUS AGENT STUDIO
echo ============================================================
echo.
echo [1/3] Ensuring Ollama Daemon is active...
start "" /B ollama serve >nul 2>&1

echo [2/3] Starting Swarm IDE Python Backend (Waitress WSGI)...
start "" /B python -u 6_builder_app.py

echo [3/3] Waiting for backend to initialize on http://127.0.0.1:5000...
set /a count=0

:wait_loop
timeout /t 1 /nobreak >nul
powershell -NoProfile -Command "(New-Object System.Net.Sockets.TcpClient).Connect('127.0.0.1', 5000)" >nul 2>&1
if %errorlevel% equ 0 goto server_ready
set /a count+=1
if %count% geq 15 goto server_timeout
goto wait_loop

:server_ready
echo.
echo [OK] Backend is live! Launching browser...
start http://127.0.0.1:5000
goto finished

:server_timeout
echo.
echo [!] Server startup took longer than expected. Opening browser now...
start http://127.0.0.1:5000

:finished
echo.
echo ============================================================
echo   Swarm IDE is active at http://127.0.0.1:5000
echo   Keep this window open while using the IDE.
echo   Press Ctrl+C or close this window when finished.
echo ============================================================
pause
