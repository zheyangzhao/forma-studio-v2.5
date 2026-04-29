@echo off
REM Forma Studio v2.5 Windows build script
REM 對應 PLAN-sprint-2.md §七

setlocal
cd /d "%~dp0"

if not exist "..\.venv\Scripts\python.exe" (
  echo Cannot find ..\.venv; please run: python -m venv ..\.venv ^&^& ..\.venv\Scripts\pip install -r requirements.txt
  exit /b 1
)

set VENV_PY=..\.venv\Scripts\python.exe

%VENV_PY% -c "import PyInstaller" 2>nul
if errorlevel 1 (
  echo Installing PyInstaller...
  %VENV_PY% -m pip install pyinstaller
)

echo Building Forma Studio.exe...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
%VENV_PY% -m PyInstaller forma-studio.spec --clean --noconfirm

if exist "dist\forma-studio\FormaStudio.exe" (
  echo Build complete: dist\forma-studio\
  echo.
  echo Next steps (optional):
  echo   1. Sign with signtool.exe
  echo   2. Test: dist\forma-studio\FormaStudio.exe
) else (
  echo Build failed
  exit /b 1
)

endlocal
