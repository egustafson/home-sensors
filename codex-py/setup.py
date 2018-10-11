## setuptools  (https:/pythonhosted.org/setuptools/setuptools.html)

from setuptools import setup, find_packages

setup(
    name = "codex",
    version = "0.1",
    packages = ["codex"],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
    ],

    entry_points = {
        'console_scripts': [
            'codexd = codex.daemon:main',
            'codex  = codex.cli:cli',
        ],
    },
)
