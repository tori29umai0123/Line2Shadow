import sys
import os

# 'frozen'状態に応じて適切なファイルパスを取得する関数
def get_appropriate_file_path():
    if getattr(sys, 'frozen', False):
        # ビルドされたアプリケーションの場合、os.path.dirname(sys.executable)のパスを使用
        return os.path.dirname(sys.executable) + "/ldm_patched/modules"
    else:
        # そうでない場合は、従来通り__file__を使用
        return os.path.dirname(__file__) 

# 適切なファイルパスを取得
appropriate_file_path = get_appropriate_file_path()

# Taken from https://github.com/comfyanonymous/ComfyUI
# This file is only for reference, and not used in the backend or runtime.


from ldm_patched.modules import sd1_clip
import torch
import os

class SD2ClipHModel(sd1_clip.SDClipModel):
    def __init__(self, arch="ViT-H-14", device="cpu", max_length=77, freeze=True, layer="penultimate", layer_idx=None, dtype=None):
        if layer == "penultimate":
            layer="hidden"
            layer_idx=-2

        textmodel_json_config = os.path.join(appropriate_file_path, "sd2_clip_config.json")
        super().__init__(device=device, freeze=freeze, layer=layer, layer_idx=layer_idx, textmodel_json_config=textmodel_json_config, dtype=dtype, special_tokens={"start": 49406, "end": 49407, "pad": 0})

class SD2ClipHTokenizer(sd1_clip.SDTokenizer):
    def __init__(self, tokenizer_path=None, embedding_directory=None):
        super().__init__(tokenizer_path, pad_with_end=False, embedding_directory=embedding_directory, embedding_size=1024)

class SD2Tokenizer(sd1_clip.SD1Tokenizer):
    def __init__(self, embedding_directory=None):
        super().__init__(embedding_directory=embedding_directory, clip_name="h", tokenizer=SD2ClipHTokenizer)

class SD2ClipModel(sd1_clip.SD1ClipModel):
    def __init__(self, device="cpu", dtype=None, **kwargs):
        super().__init__(device=device, dtype=dtype, clip_name="h", clip_model=SD2ClipHModel, **kwargs)