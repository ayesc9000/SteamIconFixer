# Steam Icon Fixer

Steam Icon Fixer is a simple tool to fix Steam shortcuts that don't have an icon.
It supports both Windows and Linux and runs on Python 3.10 or later as a standalone
zipped package.

This tool goes through all of your shortcuts from a specified location such as
your desktop or your start folder and redownloads the icons for any shortcuts
that are missing it.

Normally, this issue occurs after reinstalling Steam and using an existing game
library, or after transferring games from one Steam library to another. The reason
this issue occurs is because the Steam client doesn't redownload the icon file
for games added to your library from another PC or drive.

## Usage

As of SIF 2.0, the general usage process is now the same for both Windows and Linux!

Start by [installing Python](https://wiki.python.org/moin/BeginnersGuide/Download), then
[download the latest release of SIF](https://github.com/ayesc9000/SteamIconFixer/releases/latest/download/sif.pyz).

Open a terminal in the same location as where you saved `sif.pyz` to. You can now
start SIF with this command:

```shell
python sif.pyz
```

SIF will inform you of the argument required to use it when you do not specify any.
Each argument is typically a path to the relevant folder. For Windows users looking
to scan their desktop shortcuts, then you may typically write something like this:

```shell
python sif.pyz "C:\Users\YourUsername\Desktop\"
```

> [!NOTE]
> Note the quotations surrounding the path in the last example. This must be specified
> if the path contains any spaces.

Typically, Steam saves a copy of each shortcut to your Start menu unless you choose not
to do so when downloading the app. This is typically located in your AppData folder:

```shell
python sif.pyz "C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam"
```

Linux users may want to scan the applications directory in their home folder, which
is usually `~/.local/share/applications`. When SIF is running on Linux, it can also
take a second argument for the location to store icons in. This is normally optional
though and should only be specified if you need to store the icons outside the
default location.

Any errors that occur during the process will be logged in the terminal, so you
should read it over once SIF has finished to check for any problems.

## Building
Steam Icon Fixer requires these dependencies to be built:

- Python 3.10 or later
- Windows 7 or later, or an in-support Linux distribution

After cloning, install the required Python dependencies:

```shell
python -m pip install -r requirements.txt
```

On Linux, you may need to install some dependencies through your package manager.

Additionally, make sure that your Python scripts directory is in your path, as it
is not automatically added during installation.

Finally, create the zip package by using the zipapp tool:

```shell
python -m zipapp build -m main -o sif.pyz
```

Linux users may add `-p "/path/to/python3"` as a parameter to
the zipapp tool to insert a shebang at the start of the archive. This will also
make the archive executable. Make sure to set the path to the location of Python
on your system. Note that the standard release builds on GitHub do not have this
option specified.

## Contributing

Contributions are welcome! If you find something that can be improved, please
consider opening an issue or pull request.

Additionally, you can refer to TASKLIST.md to see what work needs to be done.

Please make sure that your pull requests comply with the GPL v3 license. More
details are available in LICENSE.md.
