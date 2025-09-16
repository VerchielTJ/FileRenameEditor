@echo off
chcp 65001 >nul
title 文件重命名工具启动器

:menu
cls
echo.
echo ========================================
echo        文件重命名工具启动器
echo ========================================
echo.
echo 请选择要运行的程序:
echo.
echo [1] 启动文件重命名工具 (推荐)
echo [2] 检查Python环境
echo [3] 查看使用说明
echo [0] 退出
echo.
set /p choice=请输入选择 (0-3): 

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto check_python
if "%choice%"=="3" goto show_help
if "%choice%"=="0" goto exit
echo 无效选择，请重新输入
pause
goto menu

:run_app
cls
echo 正在启动文件重命名工具...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    echo 可能的原因:
    echo 1. Python未正确安装
    echo 2. 缺少必要的模块
    echo 3. 文件路径问题
    echo.
    echo 请运行选项2检查Python环境
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
    python -c "import os; print('os模块: 正常')" 2>nul || echo os模块: 缺失
    python -c "import pathlib; print('pathlib模块: 正常')" 2>nul || echo pathlib模块: 缺失
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
echo 文件重命名工具
echo.
echo 功能说明:
echo - 添加前缀和后缀
echo - 创建key-value映射规则
echo - 批量替换文件名中的特定文本
echo - 实时预览效果
echo - 直观的图形界面
echo.
echo 使用步骤:
echo 1. 启动程序
echo 2. 选择工作文件夹
echo 3. 设置重命名规则（前缀、后缀、映射）
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