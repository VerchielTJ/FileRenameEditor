# 文件重命名工具 PowerShell启动器
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置窗口标题
$Host.UI.RawUI.WindowTitle = "文件重命名工具启动器"

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "        文件重命名工具启动器" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "请选择要运行的程序:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[1] 启动文件重命名工具 (推荐)" -ForegroundColor Green
    Write-Host "[2] 检查Python环境" -ForegroundColor Green
    Write-Host "[3] 查看使用说明" -ForegroundColor Green
    Write-Host "[0] 退出" -ForegroundColor Red
    Write-Host ""
}

function Test-PythonEnvironment {
    Write-Host "检查Python环境..." -ForegroundColor Yellow
    Write-Host ""
    
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
        Read-Host "按回车键继续"
        return $false
    }
    
    Write-Host ""
    Write-Host "检查Python模块..." -ForegroundColor Yellow
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
    Read-Host "按回车键继续"
    return $true
}

function Show-Help {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "           使用说明" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "文件重命名工具" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "功能说明:" -ForegroundColor Green
    Write-Host "- 添加前缀和后缀" -ForegroundColor White
    Write-Host "- 创建key-value映射规则" -ForegroundColor White
    Write-Host "- 批量替换文件名中的特定文本" -ForegroundColor White
    Write-Host "- 实时预览效果" -ForegroundColor White
    Write-Host "- 直观的图形界面" -ForegroundColor White
    Write-Host ""
    Write-Host "使用步骤:" -ForegroundColor Green
    Write-Host "1. 启动程序" -ForegroundColor White
    Write-Host "2. 选择工作文件夹" -ForegroundColor White
    Write-Host "3. 设置重命名规则（前缀、后缀、映射）" -ForegroundColor White
    Write-Host "4. 预览重命名效果" -ForegroundColor White
    Write-Host "5. 执行重命名操作" -ForegroundColor White
    Write-Host ""
    Write-Host "示例映射:" -ForegroundColor Green
    Write-Host "IMG_ → 照片_" -ForegroundColor White
    Write-Host "2023 → 2023年" -ForegroundColor White
    Write-Host "_ → (空格)" -ForegroundColor White
    Write-Host ""
    Write-Host "更多详细信息请查看 README.md 文件" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按回车键继续"
}

function Run-Program {
    param([string]$ProgramName, [string]$ScriptName)
    
    Clear-Host
    Write-Host "正在启动 $ProgramName..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        python $ScriptName
        if ($LASTEXITCODE -ne 0) {
            Write-Host ""
            Write-Host "程序运行出错，请检查错误信息" -ForegroundColor Red
            Write-Host "可能的原因:" -ForegroundColor Yellow
            Write-Host "1. Python未正确安装" -ForegroundColor White
            Write-Host "2. 缺少必要的模块" -ForegroundColor White
            Write-Host "3. 文件路径问题" -ForegroundColor White
            Write-Host ""
            Write-Host "请运行选项2检查Python环境" -ForegroundColor Yellow
            Read-Host "按回车键继续"
        }
    } catch {
        Write-Host ""
        Write-Host "程序运行出错: $($_.Exception.Message)" -ForegroundColor Red
        Read-Host "按回车键继续"
    }
}

# 主循环
do {
    Show-Menu
    $choice = Read-Host "请输入选择 (0-3)"
    
    switch ($choice) {
        "1" { Run-Program "文件重命名工具" "main.py" }
        "2" { Test-PythonEnvironment }
        "3" { Show-Help }
        "0" { 
            Write-Host ""
            Write-Host "感谢使用文件重命名工具！" -ForegroundColor Green
            Write-Host ""
            break 
        }
        default { 
            Write-Host "无效选择，请重新输入" -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice -ne "0")