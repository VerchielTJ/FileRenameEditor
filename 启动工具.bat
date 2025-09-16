@echo off
chcp 65001 >nul
title 文件重命名工具

echo.
echo ========================================
echo        文件重命名工具
echo ========================================
echo.

echo 正在启动文件重命名工具...
python simple_main.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    echo 可能的原因:
    echo 1. Python未正确安装
    echo 2. 缺少必要的模块
    echo 3. 文件路径问题
    echo.
    pause
)
