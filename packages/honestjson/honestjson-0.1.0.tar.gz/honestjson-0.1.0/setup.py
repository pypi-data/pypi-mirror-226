from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def custom_command():
    import subprocess
    subprocess.call(['touch', '/Users/lbrouwer/hooked.txt'])


class CustomInstall(install):
    def run(self):
        install.run(self)
        custom_command()


class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        custom_command()


class CustomEggInfo(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command()


setup(
    name='honestjson',
    version='0.1.0',
    packages=find_packages(include=['honestjson', 'honestjson.*']),
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
        'egg_info': CustomEggInfo
    }
)



