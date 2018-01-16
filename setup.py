from setuptools import setup
from rofi_tmux.version import __version__
desc = 'Quickly manages tmux sessions, windows and tmuxinator projects on Rofi'

setup(
    name='rofi-tmux',
    version=__version__,
    description=desc,
    author='Vinicius Arcanjo',
    author_email='viniciusarcanjov8@gmail.com',
    keywords='rofi tmux tmuxinator i3 manage switch',
    url='http://github.com/viniciusarcanjo/rofi-tmux',
    packages=['rofi_tmux', 'bin'],
    license='MIT',
    install_requires=['python-rofi', 'libtmux', 'i3ipc', 'click'],
    entry_points='''
        [console_scripts]
        rofi-tmux=bin.main:main
    ''',
    zip_safe=False,
)
