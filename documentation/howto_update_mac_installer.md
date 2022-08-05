# Updating Disk Image Mac #

## Mac ##

For updating the disk image when main code is udpated:

1. You should have a MaccsPlotter_mac.spec file already. If it's gone, try following installer README or look at old branches.

2. There should be a file called builddmg_mac.sh already from following installer README.

If both of these are inside the folder you can update pretty fast.

Enter these commands from within spacedatapython folder.

```
pyinstaller MaccsApplication.spec
```

```
./builddmg_mac.sh
```

1st command: Rebuilds the application with new code, and any updates made in the .spec file.
2nd command: Script that turns our .app file into a dmg for macOs systems.
