# 文件重命名工具 - PowerShell启动脚本
# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 设置窗口标题
$Host.UI.RawUI.WindowTitle = "文件重命名工具"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        文件重命名工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "正在启动文件重命名工具..." -ForegroundColor Yellow
try {
    python simple_main.py
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
    Read-Host "按回车键退出"
}
