@echo off
setlocal enabledelayedexpansion

:: Read the assigned system drive letter
if exist X:\windows\system32\systemdrive.txt (
    set /p systemdrive=<X:\windows\system32\systemdrive.txt
    :: Remove any trailing spaces and ensure it ends with a colon
    set systemdrive=!systemdrive: =!
    if not "!systemdrive:~-1!"==":" set systemdrive=!systemdrive!:
) else (
    echo Error: systemdrive.txt not found. Cannot proceed without knowing the system drive.
    goto end
)

:: Verify the Windows directory exists
if not exist "!systemdrive!\Windows" (
    echo Error: Windows directory not found on !systemdrive!
    echo This suggests a problem with drive letter assignment or disk detection.
    goto end
)

echo Windows installation found on !systemdrive!
echo Performing fix for our simulated oh-no-bsod issue...

if exist "!systemdrive!\Windows\System32\drivers\disk.sys.bak" (
    echo Renaming !systemdrive!\Windows\System32\drivers\disk.sys.bak to disk.sys
    ren "!systemdrive!\Windows\System32\drivers\disk.sys.bak" "disk.sys"
    if errorlevel 1 (
        echo Error: Failed to rename disk.sys.bak. Error code: !errorlevel!
        echo This might be due to file permissions or the file being in use.
    ) else (
        echo Successfully renamed disk.sys.bak to disk.sys
    )
) else (
    echo Error: disk.sys.bak not found on !systemdrive!
    echo Checked path: !systemdrive!\Windows\System32\drivers\disk.sys.bak
)

:end
echo Done performing fix.
echo System will shutdown after 30 seconds.
ping -n 30 127.0.0.1 > NUL
Wpeutil Shutdown
exit /b 0