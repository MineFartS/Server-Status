
'=======================================================

' Get Method Name from first arguement
Method = LCase(WScript.Arguments(0))

'=======================================================

' Create a new File System Object
Set FSO = CreateObject("Scripting.FileSystemObject")

' Create a new htmlfile object
Set html = CreateObject("htmlfile")

' Declare parentWindow
Set window = html.parentWindow

'
strJson = FSO.OpenTextFile("C:\Scripts\config\commands.json").ReadAll

'
window.execScript "var cmd = "&strJson&"."&Method, "JScript"

'=======================================================

if WScript.Arguments.Count = 2 then
    Visible = CBool(WScript.Arguments(1))
else
    Visible = True
end if

'=======================================================

' Create a new Shell Object
Set Shell = CreateObject("WScript.Shell")

'
Shell.CurrentDirectory = "C:/Scripts/exec"

'
Shell.Run window.cmd, Visible, 0

'=======================================================