# NEOS Platform Common Code v0.9.0

## Inclusion in projects

To include this library in another neos code base, add the following to the relevant `pyproject.toml`

```toml
[[tool.poetry.source]]
name = "nortal"
url = "https://artifactory.nortal.com/artifactory/api/pypi/neos-python/simple/"
```

And configure your local poetry instance to be able to access Nortal's pypi.

```bash
$ poetry config repositories.nortal https://artifactory.nortal.com/artifactory/api/pypi/neos-python/
$ poetry config http-basic.nortal <AD-username> <password>
```

## Prerequisites

The following packages are used across python repositories. A global install of them all is *highly* recommended.

* [Poetry](https://python-poetry.org/docs/#installation)
* [Invoke](https://www.pyinvoke.org/installing.html)

### WSL

If running on Windows, you may need to install `distutils` to install the service.

```bash
$ sudo apt-get install python3.10-distutils
```

## Initial setup

```bash
$ invoke install-dev
```

## Code Quality

### Tests

```bash
invoke tests
invoke tests-coverage
```

## Linting

```bash
invoke check-style
invoke isort
```

## Releases

Release management is handled using `bump2version`. The below commands will tag
a new release. Jenkins will then publish the release to the artifact repository.

```bash
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z
```
