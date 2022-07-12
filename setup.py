from setuptools import setup

setup(
    name='trusts_platform_client',
    version='0.1',
    description='A collection of tools to exchange data with TRUSTS.',
    url='http://github.com/storborg/funniest',
    author='Stefan Gindl',
    author_email='stefan.gindl@researchstudio.at',
    license='MIT',
    packages=['trusts_platform_client'],
    install_requires=[
        'ckanapi==4.7',
        'requests==2.27.1',
    ],
    zip_safe=False,
)
