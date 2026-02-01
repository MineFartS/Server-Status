
' ARG[0]: str  = Script To Run
' ARG[1]: bool = Show Terminal Window (Default=True)

'=======================================================

' Get Method Name from first arguement
CMD = "python.exe -m Scripts " & WScript.Arguments(0)

'=======================================================
' VISIBLE PARG

if WScript.Arguments.Count = 2 then
    Visible = CBool(WScript.Arguments(1))
else
    Visible = True
end if

'=======================================================
' VERBOSE PARG

if WScript.Arguments.Count = 3 then
    Verbose = CBool(WScript.Arguments(2))
else
    Verbose = False
end if

if Verbose then
    CMD = CMD & " -v"
end if

'=======================================================

' Create a new Shell Object
Set Shell = CreateObject("WScript.Shell")

'
Shell.CurrentDirectory = "C:\"

'
Shell.Run CMD, Visible, 0

'=======================================================