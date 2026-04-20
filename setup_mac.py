from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icon.icns',
    'packages': ['pygame', 'numpy'],
    'includes': ['pygame']
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
)
