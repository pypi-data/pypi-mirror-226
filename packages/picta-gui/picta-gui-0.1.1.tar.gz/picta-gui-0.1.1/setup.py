from setuptools import setup, find_packages

setup(
    name='picta-gui',
    version='0.1.1',
    packages=find_packages(),
    package_data={
        'picta_gui': ['data/08_17.keras'],
    },
    install_requires=[
        'opencv-python',
        'psd_tools',
        'tensorflow',
        'Pillow',
        'rawpy'
    ],
    author='Andrew Hanigan',
    author_email='andrew.hanigan@intelligent-it.com',
    description='Simple GUI for use with identifying turtle plastrons',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)