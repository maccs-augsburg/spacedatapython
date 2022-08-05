#!/bin/sh

# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg

# Empty the dmg folder.
rm -r dist/dmg/*

# Copy the app bundle to the dmg folder.
cp -r "dist/MACCS Plotter.app" dist/dmg

# If the DMG already exists, delete it.
test -f "dist/MACCS Plotter.dmg" && rm "dist/MACCS Plotter.dmg"

# Window settings, dictate size of dmg installer window
create-dmg \
  --volname "MACCS Plotter" \
  --volicon "images/maccslogo_nobg.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "MACCS Plotter.app" 175 120 \
  --hide-extension "MACCS Plotter.app" \
  --app-drop-link 425 120 \
  "dist/MACCS Plotter.dmg" \
  "dist/dmg/"
