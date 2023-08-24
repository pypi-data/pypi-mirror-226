from setuptools import setup

from versions import get_latest_version

# reading long description from file
with open('description.md') as file:
    long_description = file.read()
    
project_urls = {
    'Documentation': 'http://docs.cardinalkinetic.com/api/inodrive-python/latest/index.html'
}

# specify requirements of your package here
REQUIREMENTS = ['websocket-client', 'ifaddr', 'msgpack']

# some more details
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
]

latest_version = get_latest_version()

# calling the setup function
setup(name='CK-InoDrive-API',
      version=latest_version['number'],
      description='InoDrive API library',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://cardinalkinetic.com',
      project_urls=project_urls,
      author='Cardinal Kinetic',
      author_email='support@cardinalkinetic.com',
      license='https://www.cardinalkinetic.com/about-us/terms-of-service',
      packages=['CkInoDriveAPI'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='InoWorx InoDrive InoSync MotionControl ServoControl'
      )
