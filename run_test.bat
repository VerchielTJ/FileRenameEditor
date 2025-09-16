@echo off
chcp 65001 >nul
title 映射组件测试程序

echo.
echo ========================================
echo    映射组件测试程序
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在启动测试程序...
echo.

REM 运行测试程序
python test_mapping.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)

echo.
echo 程序已退出
pause
