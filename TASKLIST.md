# Task list

If you would like to help with this project, then here are some TODOs that would be great to start with.

## The List

- Detect installed apps directly via the Steam client/registry/library VDF
  - Only applies to Windows.
  - Would allow for shortcuts to become completely unnecessary for SIF on Windows.
- Implement automatic Steam shortcut folder detection
  - Core idea is that if no argument are specified, then SIF should automatically find eg. the start menu folder where Steam saves shortcuts by default.
  - This may not be viable on Linux.
- If possible, find a way to get a direct URL to an icon file with the Steam API, rather than having to maintain a list of known CDNs.
- Decouple GTK theme icons from the Linux implementation.
  - Determine whether it is necessary for users on KDE or other Qt-based desktops.
  - If it is not, then determine how to correct icons on those platforms.
  - Bypass any GTK-related code when not dealing with GTK theme icons.
- GUI with Tcl/Tk or similar.
  - Please no web-based GUIs.

## macOS

I have no idea if missing icons is an issue for macOS users. If it is, and you know how to fix it, then please consider writing an implementation to support it. Consider opening an issue to track your work as well.
