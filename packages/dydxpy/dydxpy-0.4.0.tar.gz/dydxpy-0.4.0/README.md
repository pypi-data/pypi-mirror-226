## dYdX Python SDK

### Dependencies

**Ubuntu**
```bash
sudo apt install python3.X-dev autoconf automake build-essential libffi-dev libtool pkg-config
```
**Fedora**
```bash
sudo dnf install python3-devel autoconf automake gcc gcc-c++ libffi-devel libtool make pkgconfig
```

**macOS**

```bash
brew install autoconf automake libtool
```

### Quick Start
Installation
```bash
pip install dydxpy
```

### Usage
Requires Python 3.7+

[Examples](https://github.com/dydxprotocol/dydxpy/tree/master/examples)
```bash
$ pipenv shell
$ pipenv install

```
Upgrade `pip` to the latest version, if you see these warnings:
  ```
  WARNING: Value for scheme.platlib does not match. Please report this to <https://github.com/pypa/pip/issues/10151>
  WARNING: Additional context:   user = True   home = None   root = None   prefix = None
  ```

### Development
1. Initialize submodule. For more help with submodules, see this [doc](https://www.notion.so/dydx/Git-Submodules-9a158282ac2145c9a3dde66dffa60f8f).
  ```
  git submodule update --init
  ```

2. Install tooling
  Make sure to install buf from brew instead of pip
  ```
  pip install grpcio-tools
  brew install buf
  ```

2. Update version
  Modify version under project and tool.poetry in pyproject.toml

3. Generate proto binding & build
  ```
  make gen
  poetry build
  ```

4. Test Local Install
  ```
  # from local build
  pip uninstall dydxpy
  pip install dydxpy --no-index --find-links /path/to/dydxpy/proto
  ```

5. Test deployment
  ```
  twine upload -r testpypi dist/* 
  ```

6. Test installation
  ```
  pip install -i https://test.pypi.org/simple/ dydxpy==<version>
  ```

7. Deply (After 1.0)

8. Install pkg (After 1.0)
  ```
  # from pypi
  pip uninstall dydxpy
  pip install dydxpy
  ```

## License

Copyright © 2023 dYdX Trading Inc. (https://dydx.exchange/)

Originally released dYdX Trading Inc. under: <br />
Proprietary License <br />
