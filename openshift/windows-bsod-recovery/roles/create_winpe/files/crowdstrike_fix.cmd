@echo off
set drive=C:
echo Using drive %drive%
echo If your device is BitLocker encrypted use your phone to log on to https://aka.ms/aadrecoverykey. Log on with your Email ID and domain account password to find the BitLocker recovery key associated with your device.
echo.
del %drive%\Windows\System32\drivers\CrowdStrike\C-00000291*.sys
echo Done performing cleanup operation.
echo System will shutdown after 30 seconds.
ping -n 30 127.0.0.1 > NUL
Wpeutil Shutdown
exit 0