from setuptools import setup, find_packages

setup(
    name='nvidia_monitor',
    version='1.1.4',
    description='NVIDIA GPU monitoring package written by KwangryeolPark',
    author='pkr7098',
    author_email='pkr7098@gmail.com',
    url='https://github.com/KwangryeolPark/PyPI.nvidia-monitor.git',
    # install_requires=['tqdm'],
    packages=find_packages(exclude=[]),
    keywords=['nvidia-smi', 'gpu', 'monitor', 'nvidia', 'nvidia-monitor'],
    python_requires='>=3.7',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)