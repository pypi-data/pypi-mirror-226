# Data Utility Packages: _Core_

[![test](https://github.com/korawica/dup-utils/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/dup-utils/actions/workflows/tests.yml)
[![python support version](https://img.shields.io/pypi/pyversions/dup-utils)](https://pypi.org/project/dup-utils/)
[![size](https://img.shields.io/github/languages/code-size/korawica/dup-utils)](https://github.com/korawica/dup-utils)

**Type**: `DUP` | **Tag**: `Data` `Utility` `Core` `CLI`

**Table of Contents:**:

- [Features](#features)
  - [Base Utility Functions](#base-utility-functions)
  - [Utility Functions](#utility-functions)
- [CLI](#cli)
  - [Extended Git](#extended-git)
  - [Version](#version)

The **Data Utility Core** package with the utility objects that was created with
sub-package namespace, `dup_utils`, for independent installation. This make this
package able to extend with any extension with this namespace. In the future,
this namespace able to scale out the coding with folder structure. You can add
any features that you want to install and import by `import dup_utils.{extension}`.

This package provide the Base Utility and Utility functions for any data package
and **CLI** tools for develop data package like extended git and version commands.

**Install from PyPI**:

```shell
pip install dup-utils
```

## Features

### Base Utility Functions

```text
core.base
    - cache
    - merge
    - split
```

### Utility Functions

```text
core
    - decorator
    - dtutils
    - randomly
```

## CLI

This Utility Package provide some CLI tools for handler development process.

### Extended Git

```shell
Usage: utils.exe git [OPTIONS] COMMAND [ARGS]...

  Extended Git commands

Options:
  --help  Show this message and exit.

Commands:
  bn               Show the Current Branch
  cl               Show the Commit Logs from the latest Tag to HEAD
  clear-branch     Clear Local Branches that sync from the Remote
  cm               Show the latest Commit message
  commit-previous  Commit changes to the Previous Commit with same message
  commit-revert    Revert the latest Commit on this Local
  tl               Show the Latest Tag
```

### Version

```shell
Usage: utils.exe vs [OPTIONS] COMMAND [ARGS]...

  Version commands

Options:
  --help  Show this message and exit.

Commands:
  bump       Bump Version
  changelog  Make Changelogs file
  conf       Return Configuration for Bump version
  current    Return Current Version

```

## License

This project was licensed under the terms of the [MIT license](LICENSE).
