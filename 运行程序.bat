@echo off
chcp 65001 >nul
title 文件重命名工具 - 运行程序

echo.
echo ========================================
echo    文件重命名工具 - 运行程序
echo ========================================
echo.

echo 正在激活虚拟环境...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ 虚拟环境已激活
) else (
    echo ❌ 虚拟环境不存在，请先运行 环境设置.bat
    echo.
    pause
    exit /b 1
)

echo.
echo 正在启动文件重命名工具...
python main.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    echo 可能的原因:
    echo 1. Python环境问题
    echo 2. 缺少必要的模块
    echo 3. 文件路径问题
    echo.
    echo 建议运行 环境设置.bat 重新设置环境
    echo.
    pause
)
