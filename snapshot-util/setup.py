import setuptools

setuptools.setup(
    name="snapshot",
    version="0.1",
    author="Eduard Sierov",
    author_email="ed270507@gmail.com",
    description="A tool to monitor system resources and save snapshots.",

    packages=setuptools.find_packages(),


    install_requires=[
        "psutil",
    ],

    entry_points={
        'console_scripts': [
            'snapshot=snapshot.monitor:main',
        ],
    },
)
