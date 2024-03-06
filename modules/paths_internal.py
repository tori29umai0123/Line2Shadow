import sys
# 'frozen'状態に応じて適切なファイルパスを取得する関数
def get_appropriate_file_path():
    if getattr(sys, 'frozen', False):
        # ビルドされたアプリケーションの場合、sys.executableのパスを使用
        return sys.executable + "/Line2Shadow/"
    else:
        # そうでない場合は、従来通り__file__を使用
        return __file__

# 適切なファイルパスを取得
appropriate_file_path = get_appropriate_file_path()

"""this module defines internal paths used by program and is safe to import before dependencies are installed in launch.py"""

import argparse
import os
import sys
import shlex
from pathlib import Path


normalized_filepath = lambda filepath: str(Path(filepath).resolve())

commandline_args = os.environ.get('COMMANDLINE_ARGS', "")
sys.argv += shlex.split(commandline_args)

cwd = os.getcwd()
modules_path = os.path.dirname(os.path.realpath(appropriate_file_path))
script_path = os.path.dirname(modules_path)

sd_configs_path = os.path.join(script_path, "configs")
sd_default_config = os.path.join(sd_configs_path, "v1-inference.yaml")
sd_model_file = os.path.join(script_path, 'model.ckpt')
default_sd_model_file = sd_model_file

# Parse the --data-dir flag first so we can use it as a base for our other argument default values
parser_pre = argparse.ArgumentParser(add_help=False)
parser_pre.add_argument("--data-dir", type=str, default=os.path.dirname(modules_path), help="base path where all user data is stored", )
cmd_opts_pre = parser_pre.parse_known_args()[0]

data_path = cmd_opts_pre.data_dir

models_path = os.path.join(data_path, "models")
extensions_dir = os.path.join(data_path, "extensions")
extensions_builtin_dir = os.path.join(script_path, "extensions-builtin")
config_states_dir = os.path.join(script_path, "config_states")
default_output_dir = os.path.join(data_path, "output")

roboto_ttf_file = os.path.join(modules_path, 'Roboto-Regular.ttf')
