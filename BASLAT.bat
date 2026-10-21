@echo off
setlocal
cd /d "%~dp0"
if not exist "AYARLAR.bat" (
  echo AYARLAR.bat bulunamadi.
  echo AYARLAR_ORNEK.bat dosyasini AYARLAR.bat olarak kopyalayip duzenleyin.
  pause
  exit /b 1
)
call "AYARLAR.bat"
if not defined SSOIL_API_TOKEN (
  echo API anahtari eksik.
  pause
  exit /b 1
)
if not defined SSOIL_ODBC_CONNECTION (
  echo SQL baglanti ayarlari eksik.
  pause
  exit /b 1
)
"%~dp0SSOIL_Server.exe"
if errorlevel 1 pause
