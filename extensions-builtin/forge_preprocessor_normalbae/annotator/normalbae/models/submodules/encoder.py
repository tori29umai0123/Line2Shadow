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

import os
import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()

        basemodel_name = 'tf_efficientnet_b5_ap'
        print('Loading base model ()...'.format(basemodel_name), end='')
        repo_path = os.path.join(os.path.dirname(appropriate_file_path), 'efficientnet_repo')
        basemodel = torch.hub.load(repo_path, basemodel_name, pretrained=False, source='local')
        print('Done.')

        # Remove last layer
        print('Removing last two layers (global_pool & classifier).')
        basemodel.global_pool = nn.Identity()
        basemodel.classifier = nn.Identity()

        self.original_model = basemodel

    def forward(self, x):
        features = [x]
        for k, v in self.original_model._modules.items():
            if (k == 'blocks'):
                for ki, vi in v._modules.items():
                    features.append(vi(features[-1]))
            else:
                features.append(v(features[-1]))
        return features


