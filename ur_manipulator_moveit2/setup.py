from setuptools import setup
import os
from glob import glob

package_name = 'ur_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hpmcsg1wl7',
    maintainer_email='hansangu093@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ur5_test_node = ur_control.ur5_test_node:main',
            'ur5_control_node = ur_control.ur5_control_node:main',
            'ur5_moveit_control = ur_control.ur5_moveit_control:main'
        ],
    },
)
