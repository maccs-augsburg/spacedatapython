#!/bin/sh

# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg

# Empty the dmg folder.
rm -r dist/dmg/*

# Copy the app bundle to the dmg folder.
cp -r "dist/MaccsApplication.app" dist/dmg

# If the DMG already exists, delete it.
test -f "dist/MaccsApplication.dmg" && rm "dist/MaccsApplication.dmg"

# Window settings, dictate size of dmg installer window
create-dmg \
  --volname "MaccsApplication" \
  --volicon "images/maccslogo_nobg.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "MaccsApplication.app" 175 120 \
  --hide-extension "MaccsApplication.app" \
  --app-drop-link 425 120 \
  "dist/MaccsApplication.dmg" \
  "dist/dmg/"
