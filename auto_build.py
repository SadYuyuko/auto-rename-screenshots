import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "rename_screenshots.py")
EXE_NAME = "自动重命名.exe"
SPEC_FILE = os.path.join(SCRIPT_DIR, os.path.splitext(EXE_NAME)[0] + ".spec")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")


def cleanup():
    for path in (SPEC_FILE, BUILD_DIR, os.path.join(SCRIPT_DIR, "__pycache__")):
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        elif os.path.isfile(path):
            os.remove(path)


def main():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("未安装 PyInstaller，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--noconfirm",
        "--distpath", SCRIPT_DIR,
        "--workpath", BUILD_DIR,
        "--specpath", SCRIPT_DIR,
        "--name", os.path.splitext(EXE_NAME)[0],
        MAIN_SCRIPT,
    ]

    print("正在打包，请稍候...")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("正在清理临时文件...")
        cleanup()
        print(f"打包成功: {os.path.join(SCRIPT_DIR, EXE_NAME)}")
    else:
        print("打包失败，请检查错误信息。")
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
