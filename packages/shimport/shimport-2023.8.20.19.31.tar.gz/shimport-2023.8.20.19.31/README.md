<!--- This is a markdown file.  Comments look like this --->
<table>
  <tr>
    <td colspan=2><strong>
    shimport
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
      <small><small>
      </small></small>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
    Import utilities for python
    <br/><br/>
    <a href=https://pypi.python.org/pypi/shimport/><img src="https://img.shields.io/pypi/l/shimport.svg"></a>
    <a href=https://pypi.python.org/pypi/shimport/><img src="https://badge.fury.io/py/shimport.svg"></a>
    <a href="https://github.com/elo-enterprises/shimport/actions/workflows/python-test.yml"><img src="https://github.com/elo-enterprises/shimport/actions/workflows/python-test.yml/badge.svg"></a>
    </td>
  </tr>
</table>

  * [Overview](#overview)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Simple lazy modules](#simple-lazy-modules)
    * [Filtering module contents](#filtering-module-contents)
    * [Automatically importing submodules](#automatically-importing-submodules)


---------------------------------------------------------------------------------

## Overview

Import utilities for python 

---------------------------------------------------------------------------------

## Installation

See [pypi](https://pypi.org/project/shimport/) for available releases.

```
pip install shimport
```

---------------------------------------------------------------------------------

## Usage

### Simple lazy modules

```
import shimport 
pathlib = shimport.lazy('pathlib')
print(pathlib.Path('.').absolute())
```

### Filtering module contents

```
import typing
import shimport 
wrapper = shimport.wrapper("os.path")
namespace = wrapper.prune(
        exclude_private=True,
        filter_module_origin=True,
        filter_instances=typing.FunctionType,
    )

namespace.map(lambda k, v: print([k,v]))
```



### Automatically importing submodules

```
...
```

---------------------------------------------------------------------------------
