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
    
#SDXLモデルをダウンロード
model_dir = os.path.join(dpath, 'models/Stable-diffusion')
MODEL_ID = "cagliostrolab/animagine-xl-3.0"
FILES = ["animagine-xl-3.0.safetensors"]
SUB_DIRS = []
download_folder(model_dir, MODEL_ID, SUB_DIRS, FILES)      

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


# Default arguments
default_args = ["--nowebui", "--xformers"]

# Append default arguments if sys.argv is empty
if len(sys.argv) == 1:
    sys.argv.extend(default_args)


args = launch_utils_Line2Shadow.args

start = launch_utils_Line2Shadow.start

def main():
    # Assuming 'args' can be directly modified. If not, this approach may need adjustment.
    # Set default values for nowebui and xformers if not explicitly provided
    if not hasattr(args, 'nowebui'):
        setattr(args, 'nowebui', True)  # Assuming boolean flag for simplicity; adjust as needed

    if not hasattr(args, 'xformers'):
        setattr(args, 'xformers', True)  # Same assumption as above

    start()

if __name__ == "__main__":
    main()
