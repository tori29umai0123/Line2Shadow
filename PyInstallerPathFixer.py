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
import re

# 対象のディレクトリパス
target_directory = 'C:/Line2Shadow'

# 追加する関数と変数のコード
prepend_code = """import sys
# 'frozen'状態に応じて適切なファイルパスを取得する関数
def get_appropriate_file_path():
    if getattr(sys, 'frozen', False):
        # ビルドされたアプリケーションの場合、sys.executableのパスを使用
        return sys.executable + "/Line2Shadow/"
    else:
        # そうでない場合は、従来通りappropriate_file_pathを使用
        return appropriate_file_path

# 適切なファイルパスを取得
appropriate_file_path = get_appropriate_file_path()

"""

# 検索対象から除外するファイルパスのリスト（絶対パスで指定）
exclude_files = [
    os.path.abspath("C:/Line2Shadow/PyInstallerPathFixer.py")
]

# 検索対象から除外するフォルダのリスト（絶対パスで指定）
exclude_folders = [
]

def file_needs_update(filepath):
    """ファイルが appropriate_file_path 変数を使用しているかどうかを確認"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return re.search(r'(?<!")(appropriate_file_path)(?!")', content) is not None
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError occurred in file: {filepath}")
        return False

def update_file(filepath):
    """ファイルを更新する"""
    if not any(filepath.startswith(excluded) for excluded in exclude_folders) and filepath not in exclude_files:
        with open(filepath, 'r+', encoding='utf-8') as file:
            print(filepath)
            content = file.read()
            updated_content = re.sub(r'(?<!")(appropriate_file_path)(?!")', 'appropriate_file_path', content)
            file.seek(0)
            file.write(prepend_code + updated_content)
            file.truncate()

# 特定のディレクトリ以下の.pyファイルを対象に処理
for root, dirs, files in os.walk(target_directory):
    dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_folders]
    for file in files:
        filepath = os.path.join(root, file)
        if file.endswith('.py') and file_needs_update(filepath):
            update_file(filepath)

print("処理が完了しました。")