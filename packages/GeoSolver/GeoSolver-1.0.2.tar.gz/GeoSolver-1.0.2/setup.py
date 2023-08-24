from setuptools import setup

with open('doc.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='GeoSolver',
    version='1.0.2',
    packages=[''],
    url='https://github.com/KareEnges/GeoSolver',
    license='MIT',
    author='EngelsVon/FengHaoen',
    author_email='engelsvon3@gmail.com',
    description='A library to solve 3D-geometry',
    install_requires=[
        'sympy'
    ],
    readme="doc.md",
    classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
