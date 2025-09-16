@echo off
chcp 65001 >nul
title 文件重命名工具 - 安装检查

echo.
echo ========================================
echo    文件重命名工具 - 安装检查
echo ========================================
echo.

REM 检查Python是否安装
echo [1/4] 检查Python环境...
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
) else (
    for /f "tokens=*" %%i in ('python --version') do echo ✅ %%i
)

REM 检查Python模块
echo.
echo [2/4] 检查Python模块...
python -c "import tkinter" 2>nul && echo ✅ tkinter模块正常 || echo ❌ tkinter模块缺失
python -c "import re" 2>nul && echo ✅ re模块正常 || echo ❌ re模块缺失
python -c "import json" 2>nul && echo ✅ json模块正常 || echo ❌ json模块缺失
python -c "import os" 2>nul && echo ✅ os模块正常 || echo ❌ os模块缺失

REM 检查项目文件
echo.
echo [3/4] 检查项目文件...
if exist "final_mapping_app.py" (
    echo ✅ final_mapping_app.py
) else (
    echo ❌ final_mapping_app.py 缺失
)

if exist "mapping_widget.py" (
    echo ✅ mapping_widget.py
) else (
    echo ❌ mapping_widget.py 缺失
)

if exist "enhanced_mapping_widget.py" (
    echo ✅ enhanced_mapping_widget.py
) else (
    echo ❌ enhanced_mapping_widget.py 缺失
)

if exist "mapping_persistence.py" (
    echo ✅ mapping_persistence.py
) else (
    echo ❌ mapping_persistence.py 缺失
)

if exist "mapping_demo.py" (
    echo ✅ mapping_demo.py
) else (
    echo ❌ mapping_demo.py 缺失
)

if exist "test_mapping.py" (
    echo ✅ test_mapping.py
) else (
    echo ❌ test_mapping.py 缺失
)

REM 测试程序运行
echo.
echo [4/4] 测试程序运行...
echo 正在测试基础模块导入...
python -c "from mapping_widget import MappingListWidget; print('✅ 基础映射组件导入成功')" 2>nul || echo ❌ 基础映射组件导入失败
python -c "from enhanced_mapping_widget import EnhancedMappingListWidget; print('✅ 增强映射组件导入成功')" 2>nul || echo ❌ 增强映射组件导入失败
python -c "from mapping_persistence import MappingPersistence; print('✅ 持久化模块导入成功')" 2>nul || echo ❌ 持久化模块导入失败

echo.
echo ========================================
echo           检查完成
echo ========================================
echo.

REM 创建配置目录
if not exist "mapping_configs" (
    mkdir "mapping_configs"
    echo ✅ 已创建配置目录: mapping_configs
)

echo 安装检查完成！
echo.
echo 您现在可以运行以下程序:
echo - 双击 "启动映射工具.bat" 启动主程序
echo - 双击 "run_mapping_tool.bat" 直接运行最终版
echo - 双击 "run_demo.bat" 运行演示程序
echo.
echo 如果遇到问题，请检查:
echo 1. Python是否正确安装
echo 2. 所有.py文件是否完整
echo 3. 是否有足够的文件权限
echo.
pause
