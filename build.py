#!/usr/bin/env python3
import os
import platform
import subprocess
from pathlib import Path

system = platform.system()
version_info_filename = "version_info.txt"

# 动态导入平台相关模块
if system == "Windows":
    from PyInstaller.utils.win32.versioninfo import (
        FixedFileInfo,
        StringFileInfo,
        StringTable,
        StringStruct,
        VarFileInfo,
        VarStruct,
        VSVersionInfo,
    )

from sc_templates import PROJECT_NAME, __version__


def get_platform_specific_args():
    """返回平台特定的打包参数"""
    args = {
        "Windows": {
            "executable_suffix": ".exe",
            "icon": "app.ico",
            "extra_args": [f"--version-file={version_info_filename}"]
        },
        "Darwin": {
            "executable_suffix": ".app",
            "icon": "app.icns",
            "extra_args": [
                f"--osx-bundle-identifier=com.scott.{PROJECT_NAME.replace('-', '_')}",
                # "--osx-entitlements-file=entitlements.plist",
            ]
        },
        "Linux": {
            "executable_suffix": "",
            "icon": "app.ico",
            "extra_args": []
        }
    }
    return args.get(system, args["Windows"])  # 默认返回Windows配置


def create_windows_version_info():
    """创建Windows版本信息文件"""
    version_parts = __version__.split(".")
    while len(version_parts) < 4:
        version_parts.append("0")
    file_version = prod_version = tuple(int(num) for num in version_parts[:4])

    version_info = VSVersionInfo(
        ffi=FixedFileInfo(
            filevers=file_version,
            prodvers=prod_version,
            mask=0x3F,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0),
        ),
        kids=[
            StringFileInfo(
                [
                    StringTable(
                        "040904B0",
                        [
                            StringStruct("CompanyName", "Scott"),
                            StringStruct("FileDescription", PROJECT_NAME),
                            StringStruct("FileVersion", ".".join(map(str, file_version))),
                            StringStruct("InternalName", PROJECT_NAME),
                            StringStruct("LegalCopyright", "Copyright © 2025"),
                            StringStruct("OriginalFilename", f"{PROJECT_NAME}.exe"),
                            StringStruct("ProductName", PROJECT_NAME),
                            StringStruct("ProductVersion", ".".join(map(str, prod_version))),
                        ],
                    )
                ]
            ),
            VarFileInfo([VarStruct("Translation", [1033, 1200])]),
        ]
    )

    with open(version_info_filename, "w", encoding='utf-8') as f:
        f.write(str(version_info))


def build_app():
    """执行跨平台打包"""
    platform_args = get_platform_specific_args()

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--name={PROJECT_NAME}",
        # f"--icon={platform_args['icon']}",
        *platform_args["extra_args"],
        # "--add-data=assets:assets",  # 跨平台路径分隔符PyInstaller会自动处理
        "--noconfirm",
        "--clean",
        f"{PROJECT_NAME}"
    ]

    print(f"执行打包命令: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    try:
        # Windows平台需要生成版本信息文件
        if system == "Windows":
            if os.path.exists(version_info_filename):
                os.remove(version_info_filename)
            create_windows_version_info()

        build_app()

        # 输出打包结果位置
        dist_path = Path("dist") / f"{PROJECT_NAME}{get_platform_specific_args()['executable_suffix']}"
        print(f"\n打包成功！生成文件: {dist_path.absolute()}")

    finally:
        # 清理Windows版本信息文件
        if system == "Windows" and os.path.exists(version_info_filename):
            os.remove(version_info_filename)


if __name__ == "__main__":
    main()
