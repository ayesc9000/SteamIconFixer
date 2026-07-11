# Task list

If you would like to help with this project, then here are some TODOs that would be great to start with.

- Detect installed apps directly via the Steam client or other means
  - Only really useful on Windows at the moment, but would allow for icons to be fixed without shortcuts being involved at all.
- Implement automatic Steam application folder detection
  - Core idea is that if no argument are specified, then SIF should automatically find eg. the start menu folder where Steam saves shortcuts by default.
  - This may not be viable on Linux.
- If possible, find a way to get a direct URL to an icon file with the Steam API, rather than having to maintain a list of known CDNs.
- Determine if the GTK icon cache always needs to be refreshed (for example on KDE).
  - If it doesn't need to be refreshed on some desktops, then this should be detected.
  - Additionally, check to make sure the GTK icon cache refresh command exists and that any GTK code we execute will actually work.

### RE: macOS

I have no idea if missing icons is an issue for macOS users. If it is, and you know how to fix it, then please consider writing an implementation to support it.
