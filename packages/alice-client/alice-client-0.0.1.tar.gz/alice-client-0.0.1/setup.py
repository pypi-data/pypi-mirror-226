"""
Copyright (c) Jordan Maxwell. All rights reserved.
See LICENSE file in the project froot for full license information.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="alice-client",
    version="0.0.1",
    description="Client for the Alice AI virtual assistant server.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GNU General Public License v2.0",
    author="Jordan Maxwell",
    maintainer="Jordan Maxwell",
    url="https://github.com/AliceHomeAI/alice-server",
    packages=['alice.client', 'alice.client.models'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ])