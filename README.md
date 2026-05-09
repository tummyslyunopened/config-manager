# config-manager

Manage your home-directory configuration in one place without symlinks.

A small Python utility that copies files between a checked-out config repo and
their live locations under `~`. Used as a submodule by
[`tummyslyunopened/config`](https://github.com/tummyslyunopened/config).

## How it works

A CSV maps `repo-relative path` → `home-relative path`:

```csv
local, remote
alacritty\alacritty.toml, AppData\Roaming\alacritty\alacritty.toml
neovim\init.lua, AppData\Local\nvim\init.lua
```

Three operations work over that mapping:

| Command         | Direction              | Use case                                           |
|-----------------|------------------------|----------------------------------------------------|
| `deploy.py`     | repo → `~`             | Push tracked config out to the live system.        |
| `adopt.py`      | `~` → repo             | Pull live config back into the repo to commit.     |
| `diff.py`       | repo ⇄ `~`             | Show diffs between repo and live (files or trees). |

Each takes the CSV path as its first argument (defaults to `default_csv_file`
in `settings.py`).

## Why no symlinks

Symlinks break across OS boundaries (Windows / macOS / NixOS), confuse some
applications that rewrite their config files in place, and require admin
rights on Windows. Plain copies work everywhere.

## Requirements

Python 3.12+. No third-party dependencies.

## Run directly

```powershell
python deploy.py path\to\destinations.csv
python adopt.py  path\to\destinations.csv
python diff.py   path\to\destinations.csv
```

In the parent `config` repo these are wrapped by `deploy.ps1`, `adopt.ps1`,
and `diff.ps1`.
