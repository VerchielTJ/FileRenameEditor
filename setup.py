#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileRenameEditor 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="FileRenameEditor",
    version="1.0.0",
    author="FileRenameEditor Team",
    author_email="",
    description="一个功能强大的文件重命名工具，支持前缀后缀和映射替换功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: System :: Filesystems",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 基础依赖（通常随Python安装）
        # tkinter - GUI界面
        # os, pathlib, shutil - 文件操作
        # re - 正则表达式
        # configparser - 配置管理
        # logging - 日志记录
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-rename-editor=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
