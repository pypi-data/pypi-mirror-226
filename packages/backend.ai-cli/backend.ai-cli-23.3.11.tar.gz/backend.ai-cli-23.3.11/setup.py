
# DO NOT EDIT THIS FILE -- AUTOGENERATED BY PANTS
# Target: src/ai/backend/cli:dist

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
        'License :: OSI Approved :: MIT License',
    ],
    'description': 'Backend.AI Command Line Interface Helper',
    'entry_points': {
        'console_scripts': [
            'backend.ai = ai.backend.cli.__main__:main',
        ],
    },
    'install_requires': (
        'attrs>=20.3',
        """backend.ai-plugin==23.03.11
""",
        'click>=7.1.2',
        'types-click',
    ),
    'license': 'MIT',
    'long_description': """# backend.ai-cli

Unified command-line interface for Backend.AI


## How to adopt in CLI-enabled Backend.AI packages

An example `setup.cfg` in Backend.AI Manager:
```
[options.entry_points]
backendai_cli_v10 =
    mgr = ai.backend.manager.cli.__main__:main
    mgr.start-server = ai.backend.gateway.server:main
```

Define your package entry points that returns a Click command group using a
prefix, and add additional entry points that returns a Click command using a
prefix followed by a dot and sub-command name for shortcut access, under the
`backendai_cli_v10` entry point group.

Then add `backend.ai-cli` to the `install_requires` list.

You can do the same in `setup.py` as well.
""",
    'long_description_content_type': 'text/markdown',
    'name': 'backend.ai-cli',
    'namespace_packages': (
    ),
    'package_data': {
        'ai.backend.cli': (
            'VERSION',
            'py.typed',
        ),
    },
    'packages': (
        'ai.backend.cli',
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
