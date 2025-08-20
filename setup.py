from setuptools import setup

package_name = 'motor_serial_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmad',
    maintainer_email='ahmad@example.com',
    description='Simple ROS2 package to test motor serial communication with Arduino.',
    license='BSD',
    entry_points={
        'console_scripts': [
            'motor_driver = motor_serial_test.motor_driver:main',
            'motor_gui = motor_serial_test.motor_gui:main',
        ],
    },
)
