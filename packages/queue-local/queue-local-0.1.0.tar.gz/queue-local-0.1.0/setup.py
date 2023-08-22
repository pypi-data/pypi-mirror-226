import setuptools

setuptools.setup(
    name='queue-local',  # https://pypi.org/project/queue-local
    version='0.1.0',
    author="Circles",
    author_email="info@circles.life",
    url="https://github.com/circles-zone/queue-local-python-package",
    packages=setuptools.find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ]
)
