from setuptools import setup

setup(
    name='cfnipv6subnetgenerator',
    version='1.0.1',
    description='CloudFormation Custom Resource for IPv6 Subnet Generator',
    author='Manuel Pata',
    author_email='pata@alface.de',
    license='BSD',
    keywords='aws cloudformation ipv6',
    py_modules=[
        'cfnresponse',
        'ipv6subnets'],
    install_requires=["py2-ipaddress"]
)
