@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================================
echo  保密教育自动学习工具 - 一键打包exe
echo ================================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境，请先安装 Python 3
    pause
    exit /b 1
)

echo.
echo 调用 build_exe.py 进行打包（依赖安装、spec 生成、构建、UPX 压缩、清理均在其中完成）...
echo.
python build_exe.py
if errorlevel 1 (
    echo.
    echo 打包失败，请查看上方错误信息
    pause
    exit /b 1
)

if not exist "dist\保密教育自动学习工具.exe" (
    echo.
    echo 打包失败：未生成 exe 文件
    pause
    exit /b 1
)

echo.
echo ================================================
echo 打包成功！
echo 生成的 exe 文件位置: dist\保密教育自动学习工具.exe
echo ================================================
echo.
echo 是否立即运行测试？(y/n)
set /p choice=
if /i "!choice!"=="y" (
    pushd dist
    "保密教育自动学习工具.exe"
    popd
)

pause
