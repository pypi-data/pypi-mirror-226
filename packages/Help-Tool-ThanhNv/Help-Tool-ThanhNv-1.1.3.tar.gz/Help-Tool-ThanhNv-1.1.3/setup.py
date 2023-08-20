import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="Help-Tool-ThanhNv",
    version="1.1.3",
    author="LinLin",
    author_email="nguyenthanh2303@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/thanhnv2303/HelpTool",
    project_urls={
        "Bug Tracker": "https://github.com/thanhnv2303/HelpTool",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='checkport',
    python_requires='>=3.7.2,<4',
    packages= setuptools.find_packages(exclude=['schemas', 'tests']),
    install_requires=[
        'requests<=2.26.0',
        'click>=8.0.4,<9',
        "sortedcontainers==2.4.0"

    ],
    entry_points={
        'console_scripts': [
            'help_tool=cli:cli',
        ],
    },
)