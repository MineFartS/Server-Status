
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' Display a message box
response = MsgBox ( _
    "The server will soon restart because of an error." & vbNewLine & _
    "Would you like to abort the restart?", _
    vbOKOnly, _
    "Server Alert" _
)

' Check the user's response
If response = vbOK Then    
    ' Abort Shutdown
    Shell.run "cmd.exe /C shutdown /a", 0, 0
End If