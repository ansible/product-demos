@echo off
setlocal enabledelayedexpansion

echo Identifying Windows installation drive...

:: Check for Windows installation partition (skipping X)
for %%D in (C D E F G H I J K L M N O P Q R S T U V W Y Z) do (
    if exist %%D:\Windows\System32 (
        set systemdrive=%%D:
        goto found
    )
)

echo Windows installation partition not found. Attempting to assign drive letter...

:: Parse the volume list to find a suitable Windows volume
for /f "tokens=2-9" %%a in ('@echo list volume ^| diskpart ^| find "NTFS"') do (
    set "volume_number=%%A"
    if %%g==Healthy if not %%h==Hidden (
        set "volume_number=%%a"
        echo Found unlabeled NTFS volume !volume_number!. Attempting to assign a drive letter...
        goto assign_letter
    )
)

echo No suitable unlabeled NTFS volumes found.
goto end

:assign_letter
:: Create a temporary diskpart script to assign a letter
echo select volume %volume_number% > "%temp%\assign_letter.txt"
echo assign letter=W >> "%temp%\assign_letter.txt"

:: Run the diskpart script
echo Assigning drive letter W to volume %volume_number%...
diskpart /s "%temp%\assign_letter.txt"
if errorlevel 1 (
    echo Failed to assign drive letter. Error level: !errorlevel!
    goto end
)

:: Check again for the Windows installation drive after assignment
if exist W:\Windows\System32 (
    set systemdrive=W:
    goto found
)

echo Windows installation partition still not found after attempting to assign drive letter.
goto end

:found
echo Windows installation found on %systemdrive%
echo %systemdrive% > X:\windows\system32\systemdrive.txt

:end
echo Preparation complete.
exit /b