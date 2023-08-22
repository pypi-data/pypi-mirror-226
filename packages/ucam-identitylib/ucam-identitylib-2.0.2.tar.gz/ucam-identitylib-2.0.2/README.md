# Identity Lib

This Python package contains shared code related to Identity systems within UIS. It's primary
purpose is to encourage code-reuse and to allow for client systems to make use of the same
data structures and logic that is contained within our emergent identity APIs.

## Use

Install `ucam-identitylib` using pip:

```
pip install ucam-identitylib
```

The module can then be used as `identitylib`:

```python3
from identitylib.identifiers import Identifier

identifier = Identifier.from_string('wgd23@v1.person.identifiers.cam.ac.uk')
print(identifier)
```

## Developer quickstart

This project contains a dockerized testing environment which wraps [tox](https://tox.readthedocs.io/en/latest/).

Tests can be run using the `./test.sh` command:

```bash
# Run all PyTest tests and Flake8 checks
$ ./test.sh

# Run PyTest and Flake8 and recreate test environments
$ ./test.sh --recreate

# Run just PyTest
$ ./test.sh -e py3

# Run a single test file within PyTest
$ ./test.sh -e py3 -- tests/test_identifiers.py

# Run a single test file within PyTest with verbose logging
$ ./test.sh -e py3 -- tests/test_identifiers.py -vvv
```

### Pulling latest specs from source repositories

Local copies of the OpenAPI specs used to generate the library should be pulled in to this repo
so the specific specs used in each build are under revision control. This can be done using the
provided script:

```bash
$ ./pull-specs.sh

# If an access token required for https clones from gitlab repositories
# then this can be specified using:
$ ./pull-specs.sh --token "ACCESS_TOKEN_HERE"

# You may need to first set the $USER environment variable to match the GitLab account name.

```

### Generating the identitylib

The identitylib is generated during the docker build process. To create a local copy of the
identitylib distribution use the build script:

```bash
$ ./build-local.sh
```

This will create a new folder `/dist` in the current directory with the wheel and tar package for
identitylib.

### Interactive testing

An interactive testing environment is provided to smoke-test any changes to the identitylib against
staging or local instances of the APIs. Note that to test local instance you will need to set the
URL in the config file to `host.docker.internal:<PORT NUMBER>` on linux.

To set up the interactive testing environment, copy the `scripts/api-loader-config.yaml.example`
file to `scripts/api-loader-config.yaml` and populate with valid API key/secret pairs for any of
the APIs you wish to test.

Run the interactive test environment using the provided script:

```bash
$ ./interactive-tests.sh
```

Additional arguments can be passed to the docker build and docker run commands by setting the
variables `ITEST_BUILD_ARGS` and `ITEST_RUN_ARGS`, e.g.:

```bash
$ ITEST_BUILD_ARGS="--build-arg install_from=dist/ucam_identitylib-1.7.0-py3-none-any.whl" ./interactive-tests.sh
```

will build the interactive environment from a local wheel stored in the `dist` directory. By
default the latest version avaiable in the `test.pypi.org/simple` index is installed into the
environment.

Once the environment is active you can load up test instances and manipulate them using the python
interactive console. The `LOADER` global variable contains a helper class which reads the config
file and generates clients based off it:

```python
# Docker build output...
>>> config, client, inst = LOADER.load_card()
>>> inst.v1_cards_list()
... # Output printed to the screen
```

Use the builtin `help` command to view info on the `LOADER`, and the returned `api_inst` objects
that can be used to make requests.
