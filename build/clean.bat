@echo off
REM ============================================================================
REM Script de Limpeza - Automacao RPCM
REM Remove todos os arquivos temporarios de build
REM ============================================================================

echo ========================================
echo   Limpeza de Arquivos de Build
echo ========================================
echo.

echo Este script ira remover:
echo - Pasta build\temp
echo - Pasta dist (raiz)
echo - Arquivos .spec (build)
echo - Cache Python (__pycache__)
echo.

set /p resposta="Deseja continuar? (S/N): "
if /i not "%resposta%"=="S" (
    echo Limpeza cancelada.
    pause
    exit /b 0
)
echo.

echo Limpando arquivos...
echo.

REM Remover pastas de build
if exist "temp" (
    echo Removendo build\temp...
    rmdir /s /q "temp"
)

REM Remover dist da raiz
if exist "..\dist" (
    echo Removendo dist...
    rmdir /s /q "..\dist"
)

REM Remover arquivos .spec
if exist "*.spec" (
    echo Removendo arquivos .spec...
    del /q "*.spec"
)

REM Remover cache Python
echo Removendo cache Python...
for /d /r "..\src" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo ========================================
echo   Limpeza concluida!
echo ========================================
echo.
pause
