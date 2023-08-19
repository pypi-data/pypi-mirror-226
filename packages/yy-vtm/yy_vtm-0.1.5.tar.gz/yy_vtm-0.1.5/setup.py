# read the contents of your README file
from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    # How you named your package folder (MyLib)
    name='yy_vtm',
    packages=['yy_vtm'],             # Chose the same as "name"
    # Start with a small number and increase it with every change you make
    version='0.1.5',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',

    description='Make video thumbnail',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Jun',                                   # Type in your name
    author_email='youyinnn@gmail.com',              # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/user/reponame',

    #   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    # Keywords that define your package best
    keywords=['video', 'thumbnail', 'maker'],

    install_requires=[
        'opencv-python',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',               # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
