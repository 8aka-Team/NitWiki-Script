import os
import shutil
import subprocess
import platform
import tempfile
from concurrent.futures import ThreadPoolExecutor

os.system("python3 -m pip install pyyaml tqdm psutil requests imageio rtoml elevate colorama nuitka ordered-set")

# 准备输出目录
if os.path.exists("dist"):
    shutil.rmtree("dist")
os.makedirs("dist", exist_ok=True)

def build(file):
    try:
        file_path = os.path.join("src", file)
        base_name = os.path.splitext(file)[0]
        print(f"🏗️ 开始构建 {file}", flush=True)

        # 创建临时构建目录
        with tempfile.TemporaryDirectory(prefix=f"build_{base_name}_") as temp_dir:
            # 构建命令参数
            args = [
                "python", "-m", "nuitka",
                "--onefile",
                file_path,
                "--assume-yes-for-downloads",
                f"--output-dir={temp_dir}",
            ]

            # 平台特定参数
            if platform.system() == 'Windows':
                args += [
                    "--windows-icon-from-ico=favicon.png",
                    "--enable-plugins=upx",
                    "--upx-binary=upx.exe"
                ]
            elif platform.system() == 'Darwin':  # 修正MacOS判断
                args.append("--macos-app-icon=favicon.png")
            elif platform.system() == 'Linux':
                args.append("--linux-icon=favicon.png")

            # 执行构建命令
            subprocess.run(args, check=True)

            # 移动生成文件到dist目录
            for item in os.listdir(temp_dir):
                src = os.path.join(temp_dir, item)
                if item.startswith(base_name) and os.path.isfile(src):
                    dest = os.path.join("dist", item)
                    shutil.move(src, dest)
                    print(f"✅ 已移动 {item} 到 dist 目录", flush=True)

        print(f"🎉 成功构建 {file}", flush=True)
    except Exception as e:
        print(f"❌ 构建 {file} 失败: {str(e)}", flush=True)

if __name__ == "__main__":
    # 获取需要构建的文件列表
    src_files = [
        f for f in os.listdir("src")
        if f != "utils.py" and os.path.isfile(os.path.join("src", f))
    ]
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(build, src_files)

    print("\n所有构建任务已完成，输出目录: dist/")