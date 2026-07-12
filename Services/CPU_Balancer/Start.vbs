
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "C:\Scripts\Services"

' Run the command
Shell.run "python -m CPU_Balancer", 0, 0