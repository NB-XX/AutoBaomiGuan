#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建最小体积 exe 的脚本。
唯一打包入口：生成 spec -> 调 PyInstaller -> UPX 压缩 -> 报告体积 -> 清理。
"""

import os
import sys
import subprocess
import shutil

EXE_NAME = '保密教育自动学习工具'
SPEC_FILE = 'build.spec'
EXE_PATH = os.path.join('dist', f'{EXE_NAME}.exe')

# 精简排除清单：只排除确定用不到的库。
# 注意：不能排除 http / email / xml / ssl —— requests/urllib3 依赖它们；
# 也不能排除 distutils —— PyInstaller 自带 hook-distutils.py 会与之冲突导致构建失败。
EXCLUDES = [
    'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 'PIL',
    'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx',
    'tornado', 'flask', 'django', 'sqlalchemy',
    'pytest', 'unittest', 'doctest', 'pydoc',
    'setuptools', 'pkg_resources', 'lib2to3',
    'IPython', 'jedi', 'parso', 'pygments',
    'multiprocessing', 'concurrent', 'asyncio',
    'pdb', 'profile', 'pstats', 'trace', 'turtle', 'curses',
]

# 对齐 PyInstaller 6.x 的 spec 模板：optimize 在 Analysis，EXE 位置参数
# 为 pyz / a.scripts / a.binaries / a.datas / [] / name=...，不要 block_cipher。
SPEC_CONTENT = f'''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={EXCLUDES!r},
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name={EXE_NAME!r},
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''


def install_deps():
    """安装运行依赖与 PyInstaller"""
    print("正在安装/更新依赖（含 PyInstaller）...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print("依赖安装完成!")
        return True
    except subprocess.CalledProcessError:
        print("依赖安装失败，请检查 pip/网络")
        return False


def write_spec():
    with open(SPEC_FILE, 'w', encoding='utf-8') as f:
        f.write(SPEC_CONTENT)
    print(f"已生成精简 spec: {SPEC_FILE}")


def build_exe():
    print("开始构建 exe ...")
    cmd = [sys.executable, '-m', 'PyInstaller', '--clean', '--noconfirm', SPEC_FILE]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False
    return True


def upx_compress():
    """若系统存在 UPX，则进一步压缩 exe"""
    if not os.path.exists(EXE_PATH):
        print("未找到 exe，跳过 UPX 压缩")
        return
    try:
        subprocess.check_call(['upx', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("UPX 不可用，跳过压缩（如需进一步压缩请安装 UPX: https://upx.github.io/）")
        return

    print("正在使用 UPX 压缩 exe ...")
    original = os.path.getsize(EXE_PATH)
    try:
        subprocess.check_call(['upx', '--best', '--lzma', EXE_PATH])
    except subprocess.CalledProcessError as e:
        print(f"UPX 压缩出错，已跳过: {e}")
        return
    compressed = os.path.getsize(EXE_PATH)
    print(f"UPX 压缩完成: {original / 1048576:.2f} MB -> {compressed / 1048576:.2f} MB "
          f"({(1 - compressed / original) * 100:.1f}%)")


def report_size():
    if os.path.exists(EXE_PATH):
        size = os.path.getsize(EXE_PATH)
        print(f"生成的 exe 大小: {size / 1048576:.2f} MB")
        print(f"exe 位置: {os.path.abspath(EXE_PATH)}")
    else:
        print("警告: 未找到生成的 exe 文件")


def clean():
    print("清理临时文件 ...")
    for d in ('build', '__pycache__'):
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"已删除目录: {d}")
    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
        print(f"已删除文件: {SPEC_FILE}")


def main():
    print("=" * 50)
    print("保密教育自动学习工具 - exe 打包脚本")
    print("=" * 50)

    print("\n1. 安装依赖 ...")
    if not install_deps():
        return

    print("\n2. 生成精简 spec ...")
    write_spec()

    print("\n3. 构建 exe ...")
    if not build_exe():
        return

    print("\n4. UPX 压缩 ...")
    upx_compress()

    print("\n5. 体积报告 ...")
    report_size()

    print("\n6. 清理临时文件 ...")
    clean()

    print("\n" + "=" * 50)
    print("打包完成！生成的 exe 在 dist 目录中")
    print("=" * 50)


if __name__ == '__main__':
    main()
