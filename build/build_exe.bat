@echo off
REM ============================================================================
REM Script de Build - Automacao RPCM
REM Gera o executavel da aplicacao usando PyInstaller
REM ============================================================================

echo ========================================
echo   Automacao RPCM - Build do Executavel
echo ========================================
echo.

REM Verificar se o PyInstaller esta instalado
echo [1/4] Verificando PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller nao encontrado. Instalando...
    python -m pip install pyinstaller
) else (
    echo PyInstaller encontrado!
)
echo.

REM Verificar e instalar dependencias do jaraco
echo [2/4] Verificando dependencias...
python -m pip show jaraco.text >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias jaraco...
    python -m pip install jaraco.text jaraco.functools jaraco.context
) else (
    echo Dependencias OK!
)
echo.

REM Limpar builds anteriores
echo [3/4] Limpando builds anteriores...
if exist "temp" rmdir /s /q "temp"
if exist "build" rmdir /s /q "build"
if exist "..\dist" rmdir /s /q "..\dist"
if exist "*.spec" del /q "*.spec"
echo Diretorios limpos!
echo.

REM Gerar o executavel
echo [4/4] Gerando executavel...
echo.
python -m PyInstaller ^
    --name="AutomacaoRPCM" ^
    --onefile ^
    --windowed ^
    --distpath="..\dist" ^
    --workpath="temp" ^
    --specpath="." ^
    --add-data="..\templates;templates" ^
    --hidden-import="customtkinter" ^
    --hidden-import="tkinter" ^
    --hidden-import="docx" ^
    --hidden-import="docxtpl" ^
    --hidden-import="pandas" ^
    --hidden-import="openpyxl" ^
    --hidden-import="xlrd" ^
    --hidden-import="bs4" ^
    --hidden-import="lxml" ^
    --hidden-import="PIL" ^
    --hidden-import="pyperclip" ^
    --hidden-import="win32com.client" ^
    --hidden-import="docx2pdf" ^
    --hidden-import="jaraco.text" ^
    --hidden-import="jaraco.functools" ^
    --hidden-import="jaraco.context" ^
    --hidden-import="platformdirs" ^
    --collect-all="customtkinter" ^
    --collect-all="jaraco" ^
    --noconsole ^
    "..\src\main.py"

if %errorlevel% neq 0 (
    echo.
    echo ERRO: Falha ao gerar o executavel!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build concluido com sucesso!
echo ========================================
echo.
echo Executavel criado em: dist\AutomacaoRPCM.exe
echo.
pause
