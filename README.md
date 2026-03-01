# Steam Icon Fixer

Steam Icon Fixer is a simple tool to fix Steam shortcuts that don't have an icon.

Normally, this issue occurs after reinstalling Steam and using an existing game
library, or after transferring games from one Steam library to another. The reason
this issue occurs is because the Steam client doesn't redownload the icon file
for games added to your library from another PC or drive.

This tool goes through all of your shortcuts, either on your desktop or better,
in your start folder, and downloads the icon for each shortcut. The end result
is the icons reappearing on your shortcuts.

Additionally, this tool can now work with Steam on Linux, where icons are
normally not downloaded at all. Icons will not only be downloaded, but can be
assigned to their corresponding shortcuts on your desktop automatically.

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

Once you have the path to your shortcuts, you can invoke the tool by providing
the path as the first argument:

```shell
sif.exe "path to shortcuts folder"
```

> [!NOTE]
> Quotations are only necessary if the path contains spaces.

Some usage examples:

```shell
sif.exe C:\\Users\\user\\Desktop
sif.exe "C:\\Users\\user\\Desktop\\Steam Games"
sif.exe "C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Steam"
```

> [!TIP]
> If you are using PowerShell, you will need to put `./` in front of the executable
> name. Example: `./sif.exe`

Fatal errors:

- \<path> does not exist. (exit code 1): The specified directory does not exist.
- \<path> is a file. (exit code 2): The specified path is not a directory.

Any errors that occur during the process will be logged, so it is recommended to
read over the output in the terminal once it is complete to identify any errors
that may have occured.

## Usage (Linux)

For Linux users, you will need to download the repository as binary versions of
SIF for Linux are currently not available. You can either use git or download
the repository as a ZIP file through GitHub. Clone/unzip SIF to any directory
(preferably in your home directory, but not required).

You will also need to make sure Python 3.13.0 or later is installed on your
system before proceeding. Most package managers should carry this version of
Python or newer. If you're not sure how to do this, please consult the
documentation provided by your distribution.

Open a terminal or change directory to the location of the SIF repository and
make the SIF script executable with `chmod +x sif.py`.

From this point you can use SIF the same way you would on Windows by providing
the location of the directory containing your Steam shortcuts as an argument.
You can also provide an optional second argument to the directory where you
would like the icon files to be saved. You should follow the XDG/FreeDesktop
directory specifications wherever possible to keep things organized. This
directory must be somewhere where your DE will have permissions to read from.
(Making/using a folder in your home directory is HIGHLY recommended)

```shell
./sif.py "path to shortcuts directory" ["path to icon storage directory"]
```

> [!NOTE]
> Quotations are only necessary if the paths contains spaces.

Some usage examples:

```shell
./sif.py ~/.local/share/applications $HOME/.icons
./sif.py /usr/share/applications/ /usr/share/pixmaps
```

> [!WARNING]
> Your desktop environment may not load the new icons immediately. Logging out
> and back in, restarting, or forcing your DE to reload the icons may be
> necessary.

## Building

> [!IMPORTANT]
> This is only relevant for Windows users. Binary versions of SIF for Linux are
> currently not supported.

Steam Icon Fixer requires these dependencies to be built:

- Python 3.13.0 or later
- Windows 7 or newer

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
