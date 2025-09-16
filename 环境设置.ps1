# 文件重命名工具 - 环境设置 PowerShell脚本
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置窗口标题
$Host.UI.RawUI.WindowTitle = "文件重命名工具 - 环境设置"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    文件重命名工具 - 环境设置" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "正在检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python未找到"
    }
} catch {
    Write-Host "❌ Python未安装或未添加到PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "请执行以下步骤:" -ForegroundColor Yellow
    Write-Host "1. 访问 https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. 下载并安装Python 3.7或更高版本" -ForegroundColor White
    Write-Host "3. 安装时勾选 'Add Python to PATH'" -ForegroundColor White
    Write-Host "4. 重新运行此脚本" -ForegroundColor White
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Write-Host "正在检查必要的Python模块..." -ForegroundColor Yellow
$modules = @("tkinter", "os", "pathlib")
foreach ($module in $modules) {
    try {
        python -c "import $module" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $module 模块正常" -ForegroundColor Green
        } else {
            Write-Host "❌ $module 模块缺失" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ $module 模块缺失" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "正在创建虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ 虚拟环境创建成功" -ForegroundColor Green
} else {
    Write-Host "✅ 虚拟环境已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "正在激活虚拟环境..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "正在安装项目依赖..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -e .

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           环境设置完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Green
Write-Host "1. 激活虚拟环境: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. 运行程序: python main.py" -ForegroundColor White
Write-Host "3. 或者直接运行: 启动映射工具.bat" -ForegroundColor White
Write-Host ""
Write-Host "虚拟环境已激活，现在可以运行程序了！" -ForegroundColor Green
Write-Host ""
Read-Host "按回车键继续"
