# esomai
Elder Scrolls Online Manual AddOn Installer by Shane Ricci

This project aids users in manually tracking, unzipping, and installing addons
in Elder Scrolls Online.

By default the app will look for ZIP files in the user's Downloads folder, and
will search for an existing AddOns folder in the default ESO install directory.
The app will also save Downloads and AddOns paths to a simple TXT file, saved
to the same folder the script is run from (written this way to allow for better
functioning when packaged into a singular EXE). These paths can be changed from
the Settings menu.

Primary functional loop:
1) Set Downloads and AddOns paths.
2) Unzip addon files.
3) Install addons by moving unzipped files to AddOns folder.
