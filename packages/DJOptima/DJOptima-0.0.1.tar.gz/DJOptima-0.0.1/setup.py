from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'The DJOptima ToolKit for Django is an all-in-one utility designed to simplify and enhance the deployment process of Django projects, particularly tailored for seamless integration with the Vercel hosting platform. This toolkit empowers developers with a range of powerful features, streamlining essential tasks and boosting productivity.'


setup(
  name='DJOptima',
  version='0.0.1',
  description=DESCRIPTION,
  long_description_content_type='text/markdown',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://nagipragalathan.github.io/Personal_website/home.html',
  author='NagiPragalathan',
  author_email='nagipragalathan@gmail.com',
  license='MIT', 
  install_requires=['Django>=2.0','TerminalDesigner'],  # Replace with actual dependencies
       entry_points={
        'console_scripts': [
            'djoptima = djangokit.VercelKit:main'
        ]
    },
  classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],          
     KEYWORDS = [
    'DJOptima', 'Django', 'Toolkit', 'deployment', 'Django projects',
    'Vercel hosting', 'HTML to Django Conversion', 'custom template tags',
    'Base Model Templates', 'Vercel Hosting Support', 'Modules and Functions',
    'Base.py', 'Host.py', 'Template.py', 'Designer', 'vercelkit.py',
    'Streamlined Deployment', 'Vercel platform', 'deployment files',
    'base settings', 'configurations', 'existing HTML content',
    'foreground colors', 'background colors', 'console output',
    'coding experience', 'deployment process', 'configuration overhead'
],
  packages=find_packages(),

)