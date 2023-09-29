from setuptools import setup

setup(
    name='enigma',
    version='1.0.0',
    packages=['enigma'],
    install_requires=[
        'PyQt5',
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'enigma-emulator = enigma._cli:start_gui',
        ],
    },
)

