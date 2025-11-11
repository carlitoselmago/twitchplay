@echo off
:: === CONFIGURATION ===
:: Folder where your videos are located
set "VIDEO_DIR=C:\Users\Administrator\videos"

:: Path to VLC executable (adjust if installed elsewhere)
set "VLC_PATH=C:\Program Files\VideoLAN\VLC\vlc.exe"

:: === FIND LATEST VIDEO ===
echo Searching for latest video in %VIDEO_DIR%...
for /f "delims=" %%a in ('dir "%VIDEO_DIR%\*.mp4" /b /a-d /o-d') do (
    set "LATEST_VIDEO=%VIDEO_DIR%\%%a"
    goto :found
)

echo No video files found in %VIDEO_DIR%
pause
exit /b

:found
echo Found latest video: %LATEST_VIDEO%

:: === PLAY VIDEO IN VLC FULLSCREEN LOOP ===
start "" "%VLC_PATH%" "%LATEST_VIDEO%" --fullscreen --loop --no-video-title-show
exit /b
