import os
import sys
from modules import launch_utils_Line2Shadow
from utils.models_dl import download_folder, download_files_flat

if getattr(sys, 'frozen', False):
    # PyInstaller でビルドされた場合
    dpath = os.path.dirname(sys.executable)
else:
    # 通常の Python スクリプトとして実行された場合
    dpath = os.path.dirname(sys.argv[0])
    


#タガーモデルをダウンロード
model_dir = os.path.join(dpath, 'models/tagger')
MODEL_ID = "SmilingWolf/wd-v1-4-moat-tagger-v2"
SUB_DIRS = [
    ("variables", ["variables.data-00000-of-00001", "variables.index"]),
]
FILES = ["keras_metadata.pb", "saved_model.pb", "selected_tags.csv"]
download_folder(model_dir, MODEL_ID, SUB_DIRS, FILES)      

#LoRAをダウンロード
model_dir = os.path.join(dpath, 'models/Lora')
MODEL_ID = "tori29umai/SDXL_shadow"
FILES = ["shadow01.safetensors"]
SUB_DIRS = []
download_folder(model_dir, MODEL_ID, SUB_DIRS, FILES)

#ControlNetをダウンロード
model_dir = os.path.join(dpath, 'models/ControlNet')
MODEL_ID = "stabilityai/control-lora"
FILES = []
SUB_DIRS = [
    ("control-LoRAs-rank256", ["control-lora-canny-rank256.safetensors"]),
]
download_files_flat(model_dir, MODEL_ID, SUB_DIRS, FILES)

#SDXLモデルをダウンロード
model_dir = os.path.join(dpath, 'models/Stable-diffusion')
MODEL_ID = "cagliostrolab/animagine-xl-3.0"
FILES = ["animagine-xl-3.0.safetensors"]
SUB_DIRS = []
download_folder(model_dir, MODEL_ID, SUB_DIRS, FILES)  

# Default arguments
default_args = ["--nowebui", "--xformers", "--skip-python-version-check", "--skip-torch-cuda-test", "--skip-torch-cuda-test", "--skip-install", "--disable-extra-extensions"]

# Check if custom arguments are provided; if not, append default arguments
if len(sys.argv) == 1:
    sys.argv.extend(default_args)
else:
    # 独自の引数がある場合、default_argsの中で未指定の引数のみを追加する
    # 引数を解析しやすくするため、setを使用
    provided_args_set = set(sys.argv)
    for arg in default_args:
        # "--"で始まるオプションのみを考慮する
        if arg.startswith("--"):
            option = arg.split("=")[0] if "=" in arg else arg
            if option not in provided_args_set:
                sys.argv.append(arg)
        else:
            # "--"で始まらないオプションは直接追加
            sys.argv.append(arg)

args = launch_utils_Line2Shadow.args

start = launch_utils_Line2Shadow.start

def main():
    start()

if __name__ == "__main__":
    main()