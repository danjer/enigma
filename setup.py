from setuptools import setup

setup(
    name='Pynigma',
    version='1.0.0',
    py_modules=['enigma'],
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