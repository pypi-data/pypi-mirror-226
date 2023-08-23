from pathlib import Path
import os
from setuptools import find_packages, setup

current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = "0.0.0"

setup(
    name='openchai',
    version=version,
    description='Open Chai',
    author='Chai Research Corp.',
    author_email='hello@chai-research.com',
    license='MIT',
    packages=['chai_guanaco'],
    package_dir={"": "src"},
    package_data={"chai_guanaco": ["resources/*"]},
    url='https://www.open-chai.com',
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': ['chai-guanaco=chai_guanaco.login_cli:cli'],
    },
)
