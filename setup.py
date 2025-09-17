#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileRenameEditor - 文件重命名工具安装脚本

一个功能强大的文件重命名工具，支持前缀后缀和映射替换功能。
采用MVC架构设计，提供清晰的代码结构和良好的可维护性。
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "FileRenameEditor - 文件重命名工具"

# 读取版本信息
def get_version():
    version_path = os.path.join(os.path.dirname(__file__), "app.py")
    if os.path.exists(version_path):
        with open(version_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="FileRenameEditor",
    version=get_version(),
    author="FileRenameEditor Team",
    author_email="your-email@example.com",
    description="一个功能强大的文件重命名工具，支持前缀后缀和映射替换功能",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/FileRenameEditor",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/FileRenameEditor/issues",
        "Source": "https://github.com/yourusername/FileRenameEditor",
        "Documentation": "https://github.com/yourusername/FileRenameEditor#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
    ],
    keywords="file rename batch rename file manager utility gui tkinter",
    python_requires=">=3.7",
    install_requires=[
        # 此项目仅使用Python标准库，无需外部依赖
        # 所有必需的模块都随Python安装：
        # - tkinter: GUI框架
        # - os, pathlib, shutil: 文件操作
        # - re: 正则表达式
        # - configparser: 配置管理
        # - logging: 日志功能
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
        "optional": [
            "pillow>=8.0.0",  # 图像处理
            "send2trash>=1.8.0",  # 安全删除
        ],
    },
    entry_points={
        "console_scripts": [
            "file-rename-editor=app:main",
            "fre=app:main",  # 简短别名
        ],
        "gui_scripts": [
            "file-rename-editor-gui=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.bat", "*.ps1"],
    },
    zip_safe=False,
    platforms=["Windows", "Linux", "macOS"],
    license="MIT",
    # 项目元数据
    maintainer="FileRenameEditor Team",
    maintainer_email="your-email@example.com",
    # 项目状态
    status="Beta",
    # 支持的Python版本
    supported_versions=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"],
)
