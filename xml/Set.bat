@echo off

cd %~dp0

schtasks.exe ^
    /create ^
    /xml "%1.xml" ^
    /tn "Server\%1" ^
    /ru %USERNAME% ^
    /it
