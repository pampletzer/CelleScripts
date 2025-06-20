; convert.ahk
; Converts .m4a and .opus files in the current directory to .mamr using ffmpeg.
; ffmpeg.exe is embedded and extracted to a temporary directory at runtime.
; Ampletzer - paul.ampletzer@gmail.com

ffmpegTemp := A_Temp "\ffmpeg.exe"

; Extract embedded ffmpeg.exe if not already extracted
if !FileExist(ffmpegTemp)
{
    FileInstall, ffmpeg.exe, %ffmpegTemp%, 1
}

SetWorkingDir, %A_ScriptDir%

; Process all .m4a files
Loop, Files, *.m4a
{
    convertFile(A_LoopFileFullPath)
}

; Process all .mp4 files
Loop, Files, *.mp4
{
    convertFile(A_LoopFileFullPath)
}


; Process all .opus files
Loop, Files, *.opus
{
    convertFile(A_LoopFileFullPath)
}

MsgBox, Done converting all audio files.

; Optional: Delete extracted ffmpeg after use
FileDelete, %ffmpegTemp%

ExitApp

; ---------- Function ----------
convertFile(inputFile)
{
    global ffmpegTemp
    ; Extract path and name components from input file
    SplitPath, inputFile, , dir, ext, nameNoExt
    nameNoExt := SanitizeFilename(nameNoExt) ; Sanitize the filename

    ; Construct full output path in the same directory
    outputFile := dir "\" nameNoExt ".amr"

    ; Ensure outputFile is an absolute path.
    ; This is a safeguard in case SplitPath doesn't return a full path (unlikely with A_LoopFileFullPath)
    ; but ensures absolute certainty.
    if !InStr(outputFile, ":\") && !InStr(outputFile, "/") ; Check for drive letter or root
    {
        outputFile := A_WorkingDir "\" outputFile ; Prepend working directory if it's a relative path
    }
    
    ; Temporary paths for log and batch file
    logFile := A_Temp "\ffmpeg_error.log"
    batFile := A_Temp "\ffmpeg_run.bat"

    ; Delete existing files if they exist
    if FileExist(logFile)
        FileDelete, %logFile%
    if FileExist(batFile)
        FileDelete, %batFile%
    if FileExist(outputFile)
    {
        FileDelete, %outputFile%
        Sleep, 100  ; Small delay in case file is still locked
    }

    ; Construct ffmpeg command line
    ; We are now explicitly giving ffmpeg the full path of the output file
    ;cmdLine := """" ffmpegTemp """ -y -i """ inputFile """ -codec:a libmp3lame -qscale:a 2 """ outputFile """ 2> """ logFile """"
    cmdLine := """" ffmpegTemp """ -y -i """ inputFile """ -codec:a libopencore_amrnb -ar 8000 -ac 1 -b:a 12.2k """ outputFile """ 2> """ logFile """"


    ; *** IMPORTANT: Temporary command output for inspection ***
    ; Keep this line active temporarily to verify the exact command.
    ;MsgBox, 64, FFmpeg Command, % "Input File: " . inputFile . "`n"
    ;                           . "Output File: " . outputFile . "`n"
    ;                           . "FFmpeg Command Line:`n" . cmdLine
    
    ; Save command to batch file and run it silently
    FileAppend, %cmdLine%, %batFile%
    
    ; *** IMPORTANT: Explicitly pass Working Directory to RunWait ***
    ; The third parameter (WorkingDir) of RunWait ensures the command is executed in the specified directory.
    ; While A_WorkingDir usually suffices, explicit is better for troubleshooting.
    RunWait, %ComSpec% /c ""%batFile%"", %dir%, Hide ; Pass %dir% as WorkingDir for the batch command
    exitCode := ErrorLevel

    ; Handle errors
    if (exitCode != 0 || !FileExist(outputFile))
    {
        errorMsg := ""
        if FileExist(logFile)
            FileRead, errorMsg, %logFile%

        MsgBox, 48, Conversion Failed, Failed to convert:`n%inputFile%`n`nCommand:`n%cmdLine%`n`nError:`n%errorMsg%
    }
    else
    {
        ToolTip, Converted:`n%inputFile%
        Sleep, 500
        ToolTip
    }
}

; Function to sanitize filename for special characters, including emoticons
SanitizeFilename(filename)
{
    ; This regex matches any character that is NOT:
    ; - an alphanumeric character (a-z, A-Z, 0-9)
    ; - a space (\s)
    ; - a dot (\.)
    ; - a hyphen (-)
    ; - an underscore (_)
    ; It will effectively catch emoticons and other special symbols.
    sanitized := RegExReplace(filename, "[^a-zA-Z0-9\s\.\-_]", "_")
    
    ; Optional: Replace multiple underscores with a single one (for cleaner filenames)
    sanitized := RegExReplace(sanitized, "__+", "_")
    
    ; Trim leading/trailing spaces or dots (Windows filename rules)
    ; This ensures filenames don't start/end with problematic characters.
    Loop
    {
        StringLeft, firstChar, sanitized, 1
        StringRight, lastChar, sanitized, 1
        if (firstChar = " " or firstChar = ".")
            StringTrimLeft, sanitized, sanitized, 1
        else if (lastChar = " " or lastChar = ".")
            StringTrimRight, sanitized, sanitized, 1
        else
            break
    }
    
    ; Ensure filename is not empty after sanitization (e.g., if original was just an emoticon)
    if (sanitized = "")
        sanitized := "unnamed_file" ; Fallback name

    return sanitized
}