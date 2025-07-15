@echo off
title 20-20-20 护眼提醒器
echo ===================================
echo     20-20-20 护眼提醒器 启动中...
echo ===================================
echo.

cd /d "%~dp0"

echo 正在启动程序...
python start.py

if %errorlevel% neq 0 (
    echo.
    echo 程序启动失败！
    echo 错误代码: %errorlevel%
    echo.
    pause
) else (
    echo 程序已正常退出
)
