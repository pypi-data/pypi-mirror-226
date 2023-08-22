from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='service_Rabbit_thread',
    version='0.0.1',
    license='MIT License',
    author='Eliézer Schwartz',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='eliezer.mail090@gmail.com',
    keywords='rabbit',
    description=u'Wrapper não oficial do Rabbit',
    packages=['rabbit_library'],
    install_requires=['pika'],)