# Steam Icon Fixer

Steam Icon Fixer is a simple tool to fix Steam shortcuts that don't have an icon.

Normally, this issue occurs after reinstalling Steam and using an existing game
library, or after transferring games from one Steam library to another. The reason
this issue occurs is because the Steam client doesn't redownload the icon file
for games added to your library from another PC or drive.

Steam on Linux does not download icons at all, instead setting all shortcuts to show
the Steam icon.

This tool goes through all of your shortcuts, either on your desktop or better,
in your start folder, and downloads the icon for each shortcut. The end result
is the icons reappearing on your shortcuts.

## Usage (Windows)

For normal users, download the latest release build. Place the exe file somewhere,
doesn't really matter where. Open a terminal in the same folder as it (you can hold
shift and right click to reveal an "Open in PowerShell" option in any folder).

From this terminal, you can specify what directory you would like the tool to search
through. As stated earlier, the best folder to search is the start menu, since it
usually contains a shortcut for every installed game. You can find the folder for
Steam shortcuts in the start menu by searching for any game, and selecting the
"Open file location" option. You can also right-click any game in the start menu
for the same option. Once open, copy the folder path from the file explorer window.

Once you have the path to your shortcuts, you can invoke the tool by following the
syntax below:

```shell
sif.exe "path to file"
```

> Quotations are only necessary if the path contains spaces.

Some usage examples:

```shell
sif.exe C:\\Users\\user\\Desktop
sif.exe "C:\\Users\\user\\Desktop\\Steam Games"
sif.exe "C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Steam"
```

> If you are using PowerShell, you will need to put `./` in front of the executable
> name. Example: `./sif.exe`

Fatal errors:

- \<path> does not exist. (exit code 1): The specified directory does not exist.
- \<path> is a file. (exit code 2): The specified path is not a directory.

Any errors that occur during the process will be logged, so it is recommended to
read over the output in the terminal once it is complete to identify any errors
that may have occured.

## Usage (Linux)

Some usage examples:

```sh
sif ~/.local/share/applications $HOME/.icons
sif /usr/share/applications/ /usr/share/pixmaps
```

Please note that your desktop environment may not reload the new icons immediately.
Logging out and back in, restarting, or forcing your DE to reload the icons may be
necessary.

## Building

Steam Icon Fixer requires these dependencies to be built:

- Python 3.11.4 (or similar)
- Windows 7 or newer or Linux

After cloning, install Python dependencies with:

```shell
pip install -r requirements.txt
```

Make sure that your scripts directory is in your path, as it is not automatically
added during installation.

Finally, create the executable by running the build script:

```shell
build.cmd
```

> If you are using PowerShell, you will need to put `./` in front of the executable
> name. Example: `./build.cmd`

## Contributing

Contributions are welcome! If you find something that can be improved, we invite
you to open an issue or a pull request.

Please make sure that your pull requests comply with the GPL v3 license. More
details are available in LICENSE.md.
