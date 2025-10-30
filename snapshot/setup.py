import setuptools

setuptools.setup(
    name="snapshot",
    version="1.0.0",
    author="Eduard Sierov",
    author_email="ed270507@gmail.com",
    description="A tool to monitor system resources and save snapshots.",

    packages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],

    python_requires='>=3.6',
    install_requires=[
        'psutil>=5.8.0',
    ],
    entry_points={
        'console_scripts': [
            'snapshot=snapshot.monitor:main',

        ],
    },
)
