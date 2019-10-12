@echo off
cd /d %~dp0
setlocal enabledelayedexpansion

set sourcePath=vanTools
set targetPath=C:\Users\%USERNAME%\Documents\maya\2018\prefs


xcopy  /e /c /y "%sourcePath%" "%targetPath%"


pause


