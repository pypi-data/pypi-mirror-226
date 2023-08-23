from setuptools import setup, find_packages

setup(
    name='youtube-selenium-cookie',
    version='0.2',
    packages=find_packages(),
    install_requires=["selenium", "webdriver_manager"],  # Add your dependencies here
    author='Abdulazeez Olabode',
    author_email="dataslid@gmail.com",
    description='A Youtube 3rd Party Library that uses selenium and webdriver_manager',
    url='https://github.com/azeez010/youtube-selenium-cookie',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
