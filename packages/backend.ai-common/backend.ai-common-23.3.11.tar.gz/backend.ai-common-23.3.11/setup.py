
# DO NOT EDIT THIS FILE -- AUTOGENERATED BY PANTS
# Target: src/ai/backend/common:dist

from setuptools import setup

setup(**{
    'author': 'Lablup Inc. and contributors',
    'classifiers': [
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    ],
    'description': 'Backend.AI commons library',
    'install_requires': (
        'PyJWT~=2.0',
        'aiodns>=3.0',
        'aiohttp_sse>=2.0',
        'aiohttp~=3.8.1',
        'aiomonitor-ng~=0.7.2',
        'aiotools~=1.6.1',
        'async_timeout~=4.0',
        'asynctest>=0.13.0',
        'asyncudp>=0.4',
        'attrs>=20.3',
        """backend.ai-plugin==23.03.11
""",
        'click>=7.1.2',
        'coloredlogs~=15.0',
        'etcetra==0.1.15',
        'ifaddr~=0.2',
        'janus~=1.0.0',
        'msgpack>=1.0.5rc1',
        'multidict>=6.0',
        'packaging>=21.3',
        'python-dateutil>=2.8',
        'python-json-logger>=2.0.1',
        'pyzmq~=24.0.1',
        'redis[hiredis]~=4.6.0',
        'tblib~=1.7',
        'temporenc~=0.1.0',
        'tenacity>=8.0',
        'tomli~=2.0.1',
        'trafaret~=2.1',
        'typeguard~=2.10',
        'types-click',
        'types-python-dateutil',
        'types-redis',
        'typing_extensions~=4.3',
        'yarl~=1.8.2',
    ),
    'license': 'LGPLv3',
    'long_description': """Backend.AI Commons
==================

[![PyPI release version](https://badge.fury.io/py/backend.ai-common.svg)](https://pypi.org/project/backend.ai-common/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/backend.ai-common.svg)
[![Build Status](https://travis-ci.com/lablup/backend.ai-common.svg?branch=master)](https://travis-ci.com/lablup/backend.ai-common)
[![Gitter](https://badges.gitter.im/lablup/backend.ai-common.svg)](https://gitter.im/lablup/backend.ai-common)

Common utilities library for Backend.AI


## Installation

```console
$ pip install backend.ai-common
```

## For development

```console
$ pip install -U pip setuptools
$ pip install -U -r requirements/dev.txt
```

### Running test suite

```console
$ python -m pytest
```

With the default halfstack setup, you may need to set the environment variable `BACKEND_ETCD_ADDR`
to specify the non-standard etcd service port (e.g., `localhost:8110`).

The tests for `common.redis` module requires availability of local TCP ports 16379, 16380, 16381,
26379, 26380, and 26381 to launch a temporary Redis sentinel cluster via `docker compose`.

In macOS, they require a local `redis-server` executable to be installed, preferably via `brew`,
because `docker compose` in macOS does not support host-mode networking and Redis *cannot* be
configured to use different self IP addresses to announce to the cluster nodes and clients.
""",
    'long_description_content_type': 'text/markdown',
    'name': 'backend.ai-common',
    'namespace_packages': (
    ),
    'package_data': {
        'ai.backend.common': (
            'VERSION',
            'enum_extension.pyi',
            'py.typed',
        ),
        'ai.backend.common.plugin': (
            'py.typed',
        ),
    },
    'packages': (
        'ai.backend.common',
        'ai.backend.common.plugin',
        'ai.backend.common.web.session',
    ),
    'project_urls': {
        'Documentation': 'https://docs.backend.ai/',
        'Source': 'https://github.com/lablup/backend.ai',
    },
    'python_requires': '>=3.11,<3.12',
    'url': 'https://github.com/lablup/backend.ai',
    'version': """23.03.11
""",
    'zip_safe': False,
})
