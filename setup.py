try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Garage Door Controller',
    'author': 'Jonathan Bowen',
    'url': 'https://github.com/jbowen102/garage_door_control',
    'download_url': 'https://github.com/jbowen102/garage_door_control',
    'author_email': 'jjbowen19@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'wiringpi2'],
    'packages': [],
    'scripts': [],
    'name': 'garage_door_control'
}

setup(**config)
