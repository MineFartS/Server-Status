
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' Display a message box
response = MsgBox ( _
    "The server is shutting down" & vbNewLine & _
    "Would you like to abort?", _
    vbOKOnly, _
    "Server Alert" _
)

' Check the user's response
If response = vbOK Then    
    ' Abort Shutdown
    Shell.run "cmd.exe /C shutdown /a", 0, 0
End If