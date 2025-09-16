# 文件重命名工具 - 运行程序 PowerShell脚本
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置窗口标题
$Host.UI.RawUI.WindowTitle = "文件重命名工具 - 运行程序"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    文件重命名工具 - 运行程序" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "正在激活虚拟环境..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ 虚拟环境已激活" -ForegroundColor Green
} else {
    Write-Host "❌ 虚拟环境不存在，请先运行 环境设置.ps1" -ForegroundColor Red
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Write-Host "正在启动文件重命名工具..." -ForegroundColor Yellow
try {
    python main.py
    if ($LASTEXITCODE -ne 0) {
        throw "程序运行出错"
    }
} catch {
    Write-Host ""
    Write-Host "程序运行出错，请检查错误信息" -ForegroundColor Red
    Write-Host "可能的原因:" -ForegroundColor Yellow
    Write-Host "1. Python环境问题" -ForegroundColor White
    Write-Host "2. 缺少必要的模块" -ForegroundColor White
    Write-Host "3. 文件路径问题" -ForegroundColor White
    Write-Host ""
    Write-Host "建议运行 环境设置.ps1 重新设置环境" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按回车键退出"
}
