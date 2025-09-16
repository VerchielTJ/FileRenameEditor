@echo off
chcp 65001 >nul
title 文件重命名工具 - 环境设置

echo.
echo ========================================
echo    文件重命名工具 - 环境设置
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo.
    echo 请执行以下步骤:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python 3.7或更高版本
    echo 3. 安装时勾选 "Add Python to PATH"
    echo 4. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境正常
python --version

echo.
echo 正在检查必要的Python模块...
python -c "import tkinter; print('✅ tkinter模块: 正常')" 2>nul || echo ❌ tkinter模块: 缺失
python -c "import os; print('✅ os模块: 正常')" 2>nul || echo ❌ os模块: 缺失
python -c "import pathlib; print('✅ pathlib模块: 正常')" 2>nul || echo ❌ pathlib模块: 缺失

echo.
echo 正在创建虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo ✅ 虚拟环境创建成功
) else (
    echo ✅ 虚拟环境已存在
)

echo.
echo 正在激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo 正在安装项目依赖...
pip install --upgrade pip
pip install -e .

echo.
echo ========================================
echo           环境设置完成
echo ========================================
echo.
echo 使用方法:
echo 1. 激活虚拟环境: venv\Scripts\activate.bat
echo 2. 运行程序: python main.py
echo 3. 或者直接运行: 启动映射工具.bat
echo.
echo 虚拟环境已激活，现在可以运行程序了！
echo.
pause
