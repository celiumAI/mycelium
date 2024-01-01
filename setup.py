from setuptools import setup, find_packages

setup(
    name='note',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'note=mycelium.note.main:cli',
        ],
    },
    install_requires=[
    ],
    python_requires='>=3.9',
)
