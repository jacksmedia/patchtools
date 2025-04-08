@echo off

:: this is used in Step 3
set "DEST_DIR=corrupted"
:: Let's create the /corrupted folder if it doesn't exist
if not exist "%DEST_DIR%" mkdir "%DEST_DIR%"

:: Step 1: unzip archives from ff6tools
python unzipper.py
echo All .zip archives available were opened to folders...

:: Step 2: grab al .sfc files from the unzipped archives
python file-finder.py
echo All sfc files retrieved from archive folders...

:: Step 3: copy all .sfc files to /corrupted
copy *.sfc "%DEST_DIR%" /Y
echo All .sfc files were copied to /%DEST_DIR%!

:: Step 3: remove all local .sfc files after copying
del /Q *.sfc
echo All .sfc files were removed from this directory.


:: Step 4: use "cookie cutter" to move sprite bytes to new roms
python rom-salvager.py
echo ff6tools sprite changes moved over to clean roms!

:: Step 5: make patches from these new, uncorrupted roms
python patchmaker.py
echo Patches created from fresh clean roms!

:: Step 6: remove the working files
python directory-cleaner.py
echo All working files removed!

pause

