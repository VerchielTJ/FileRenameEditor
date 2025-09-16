@echo off
chcp 65001 >nul
title 文件重命名工具 - 映射组件启动器

:menu
cls
echo.
echo ========================================
echo    文件重命名工具 - 映射组件启动器
echo ========================================
echo.
echo 请选择要运行的程序:
echo.
echo [1] 最终版完整应用 (推荐)
echo [2] 演示程序 (功能展示)
echo [3] 基础测试程序
echo [4] 检查Python环境
echo [5] 查看使用说明
echo [0] 退出
echo.
set /p choice=请输入选择 (0-5): 

if "%choice%"=="1" goto run_final
if "%choice%"=="2" goto run_demo
if "%choice%"=="3" goto run_test
if "%choice%"=="4" goto check_python
if "%choice%"=="5" goto show_help
if "%choice%"=="0" goto exit
echo 无效选择，请重新输入
pause
goto menu

:run_final
cls
echo 正在启动最终版完整应用...
echo.
python final_mapping_app.py
if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)
goto menu

:run_demo
cls
echo 正在启动演示程序...
echo.
python mapping_demo.py
if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)
goto menu

:run_test
cls
echo 正在启动测试程序...
echo.
python test_mapping.py
if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)
goto menu

:check_python
cls
echo 检查Python环境...
echo.
python --version
if errorlevel 1 (
    echo.
    echo 错误: 未找到Python
    echo 请安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
) else (
    echo.
    echo Python环境正常
    echo.
    echo 检查必要的Python模块...
    python -c "import tkinter; print('tkinter模块: 正常')" 2>nul || echo tkinter模块: 缺失
    python -c "import re; print('re模块: 正常')" 2>nul || echo re模块: 缺失
    python -c "import json; print('json模块: 正常')" 2>nul || echo json模块: 缺失
    python -c "import os; print('os模块: 正常')" 2>nul || echo os模块: 缺失
)
echo.
pause
goto menu

:show_help
cls
echo ========================================
echo           使用说明
echo ========================================
echo.
echo 文件重命名工具 - 映射组件
echo.
echo 功能说明:
echo - 创建key-value映射规则
echo - 批量替换文件名中的特定文本
echo - 支持正则表达式
echo - 配置保存和加载
echo.
echo 使用步骤:
echo 1. 选择要运行的程序
echo 2. 在映射编辑中添加替换规则
echo 3. 选择要处理的文件夹
echo 4. 预览重命名效果
echo 5. 执行重命名操作
echo.
echo 示例映射:
echo IMG_ → 照片_
echo 2023 → 2023年
echo _ → (空格)
echo.
echo 更多详细信息请查看 README.md 文件
echo.
pause
goto menu

:exit
echo.
echo 感谢使用文件重命名工具！
echo.
pause
exit /b 0
