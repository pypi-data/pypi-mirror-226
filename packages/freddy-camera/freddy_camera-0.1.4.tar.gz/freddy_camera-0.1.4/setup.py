# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freddy_camera']

package_data = \
{'': ['*'], 'freddy_camera': ['freddy_frames/*']}

install_requires = \
['Pillow>=10.0.0,<11.0.0', 'pyvirtualcam==0.9.1', 'sounddevice>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'freddy-camera',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'megahomyak',
    'author_email': 'g.megahomyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
