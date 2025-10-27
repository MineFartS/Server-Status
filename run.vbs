
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

Shell.CurrentDirectory = "C:/Scripts"

' Create a new File System Object
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get Method Name from first arguement
Method = LCase(WScript.Arguments(0))

if WScript.Arguments.Count = 2 then
    Visible = CBool(WScript.Arguments(1))
else
    Visible = False
end if

' Open Dictionary File
Set dictfile = FSO.OpenTextFile("C:/Scripts/config/commands.yaml", 1)

' Read the dictionary file line by line
Do Until dictfile.AtEndOfStream

    line = LCase(dictfile.ReadLine)

    ' Check if a colon is in the line
    if InStr(line, ":") Then

        ' Split the line by the first colon
        parts = Split(line, ":", 2)

        ' Check if dictionary key matches the method
        If parts(0) = Method Then

            Cmd = "python " & Trim(parts(1))

            Shell.Run Cmd, Visible, 0
            
        End If

    End If

Loop