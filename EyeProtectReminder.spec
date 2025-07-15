# -*- mode: python ; coding: utf-8 -*-

import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 配置分析选项
a = Analysis(
    ['main.py'],  # 主入口文件
    pathex=[current_dir],  # 搜索路径
    binaries=[],
    datas=[
        ('icon.png', '.'),  # 将图标文件包含到根目录
        ('icon_16x16.png', '.'),
        ('icon_32x32.png', '.'),
        ('icon_64x64.png', '.'),
        ('icon_128x128.png', '.'),
    ],
    hiddenimports=[
        'pystray._win32',  # pystray Windows 模块
        'PIL._tkinter_finder',  # PIL tkinter 查找器
        'tkinter',
        'tkinter.ttk',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'pystray',
        'threading',
        'time',
        'config',
        'reminder_window',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # 排除不需要的大型库
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'tornado',
        'zmq',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# 配置PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 配置EXE - 单文件模式
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='护眼提醒器',  # 可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩（如果可用）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.png',  # 设置程序图标
    version_file=None,
)
