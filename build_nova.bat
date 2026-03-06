@echo off
echo ✦ Nova Language v0.5.7 Build System ✦
echo -------------------------------------

:: 1. Clean and Build
echo [1/3] Running Gradle build...
call gradlew.bat clean installDist
if %ERRORLEVEL% NEQ 0 (
    echo Error during Gradle build!
    pause
    exit /b %ERRORLEVEL%
)

:: 2. Create Distribution ZIP
echo [2/3] Creating ZIP archive...
powershell -Command "if (Test-Path 'release') { Remove-Item -Recurse -Force 'release\nova-v0.5.7-windows.zip' -ErrorAction SilentlyContinue }; Compress-Archive -Path 'build\install\nova\*' -DestinationPath 'release\nova-v0.5.7-windows.zip' -Force"
if %ERRORLEVEL% NEQ 0 (
    echo Error during ZIP creation!
    pause
    exit /b %ERRORLEVEL%
)

:: 3. Optional: MSI Generation (Requires WiX Toolset)
echo [3/3] Checking for WiX to generate MSI...
where candle.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Building MSI installer...
    jpackage --input build/install/nova/lib --main-jar nova-0.5.7.jar --main-class com.luminar.nova.Main --type msi --name "Nova" --app-version 0.5.7 --vendor "Luminar" --win-dir-chooser --win-menu --win-shortcut --dest release
    echo ✓ MSI generated in release/
) else (
    echo [!] WiX Toolset not in PATH. Skipping MSI generation.
)

echo.
echo ✦ BUILD COMPLETE ✦
echo Your artifacts (ZIP, MSI) are in the 'release/' folder.
pause
