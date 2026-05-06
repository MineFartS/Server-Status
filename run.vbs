'=======================================================

' ARG[0]: str  = Script To Run
' ARG[1]: bool = Show Terminal Window (Default=True)
' ARG[2]: bool = Verbose (Default=False)

' EX: wscript run.vbs Interval.Startup True False

'=======================================================

' Create a new Shell Object
Set Shell = CreateObject("WScript.Shell")

'=======================================================

' Get Method Name from first arguement
' If the exe doesn't exist, try to build it (requires MSVC + CMake on PATH)
If fso.FileExists("C:\\Scripts_CPP\\ScriptsCPP.exe") = False Then
    Shell.CurrentDirectory = "C:\\Scripts_CPP\\"
' Build via cmake (Visual Studio generator)
    cmdPow = "powershell -NoProfile -Command \"& { if (Get-Command cmake -ErrorAction SilentlyContinue) {\n" & _
              "  cmake -S . -B build -G 'Visual Studio 17 2022' -A x64;\n" & _
              "  cmake --build build --config Release\n" & _
              "} else {\n" & _
              "    $cmakeExe = 'C:\\ProgramData\\chocolatey\\bin\\cmake.exe';\n" & _
              "    if (Test-Path $cmakeExe) {\n" & _
              "      & $cmakeExe -S . -B build -G 'Visual Studio 17 2022' -A x64;\n" & _
              "      & $cmakeExe --build build --config Release;\n" & _
              "    } else {\n" & _
              "      Write-Host 'cmake not found on PATH and no cmake.exe found; cannot build.';\n" & _
              "    }\n" & _
              "  }\n" & _
              "}\""
    Shell.Run cmdPow, 0, True
End If

CMD = "ScriptsCPP.exe " & WScript.Arguments(0)

'=======================================================
' VISIBLE [POSITIONAL ARG]

if WScript.Arguments.Count = 2 then
    Visible = CBool(WScript.Arguments(1))
else
    Visible = True
end if

'=======================================================
' VERBOSE [POSITIONAL ARG]

if WScript.Arguments.Count = 3 then
    Verbose = CBool(WScript.Arguments(2))
else
    Verbose = False
end if

if Verbose then
    CMD = CMD & " -v"
end if

'=======================================================

'
Shell.CurrentDirectory = "C:\Scripts_CPP\"

'
Shell.Run CMD, Visible, 0

'=======================================================