from setuptools import setup

setup(
    name='downloader-anime-automatic',
    version='1.0.0',
    packages=['src', 'src.GUI', 'src.downloader', 'selenium', 'tkinter'],
    install_requires=['selenium'],
    url='',
    license='',
    author='Karlos Warney',
    author_email='karloswarney@gmail.com',
    description='Esse aplicativo serve para automatizar downloads do site AniTube'
)
