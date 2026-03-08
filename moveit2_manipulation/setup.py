from setuptools import setup
from glob import glob
import os

package_name = 'my_manipulation_robot'

# URDF 파일들을 재귀적으로 찾기
def get_urdf_files():
    urdf_files = []
    for root, dirs, files in os.walk('urdf'):
        for file in files:
            if file.endswith(('.urdf', '.xacro')):
                rel_path = os.path.relpath(os.path.join(root, file), 'urdf')
                target_dir = os.path.join('share', package_name, 'urdf', os.path.dirname(rel_path))
                if target_dir not in [item[0] for item in urdf_files]:
                    urdf_files.append((target_dir, []))
                for item in urdf_files:
                    if item[0] == target_dir:
                        item[1].append(os.path.join(root, file))
                        break
    return urdf_files

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*'))),
        (os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*'))),
    ] + get_urdf_files(),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='soonawg',
    maintainer_email='hansangu093@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sin_node = my_manipulation_robot.sin_node:main',
            'joint2_extractor = my_manipulation_robot.joint2_extractor:main',
            'joint2_plotter = my_manipulation_robot.joint2_plotter:main',
            'sin_sam = my_manipulation_robot.sin_sam:main',
            'sin_sa = my_manipulation_robot.sin_sa:main',
            'sin_five = my_manipulation_robot.sin_five:main',
            'sin_all = my_manipulation_robot.sin_all:main',
            'joint_move = my_manipulation_robot.joint_move:main',
        ],
    },
)
