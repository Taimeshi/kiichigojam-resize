from cx_Freeze import setup, Executable

build_options = {
    "packages": ["pygame", "numpy"],
    "include_files": ["resources"],  # 画像フォルダなど
}

setup(
    name="RESIZE",
    version="1.0",
    description="",
    options={"build_exe": build_options},
    executables=[Executable("main.py", base="Win32GUI", icon="resources/icon.ico")],  # コンソールなし
)
