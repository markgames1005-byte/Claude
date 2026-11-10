@echo off
cd /d "%~dp0"
set "DESTINO=%~dp0Abrir Organizador (Windows).bat"
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Organizador de Gmail.lnk'); $s.TargetPath='%DESTINO%'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.IconLocation='shell32.dll,156'; $s.Save()"
echo Listo: tienes "Organizador de Gmail" en el escritorio.
pause
