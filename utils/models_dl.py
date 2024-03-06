import os
import requests

def download_file(url, output_file):
    # URLからファイルをダウンロードしてoutput_fileに保存する関数
    response = requests.get(url)
    with open(output_file, "wb") as f:
        f.write(response.content)

def download_files(repo_id, subfolder, files, cache_dir, flat=False):
    """
    リポジトリから指定されたファイルをダウンロードする関数。
    flat=Trueの場合、サブディレクトリ構造を無視してファイルをダウンロードする。
    """
    for file in files:
        # ファイルの完全なURLを構築
        url = f"https://huggingface.co/{repo_id}/resolve/main/{subfolder}/{file}"

        # flatがTrueの場合は、ファイル名のみを使用して出力ファイルパスを決定
        output_file = os.path.join(cache_dir, os.path.basename(file)) if flat else os.path.join(cache_dir, subfolder, file)

        # 出力ディレクトリが存在しない場合は作成
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ファイルがまだ存在しない場合はダウンロード
        if not os.path.exists(output_file):
            print(f"{os.path.basename(file)} を {url} から {output_file} にダウンロードしています...")
            download_file(url, output_file)
            print(f"{os.path.basename(file)} のダウンロードが完了しました！")

def download_folder(model_dir, MODEL_ID, SUB_DIRS, FILES):
    if not os.path.exists(model_dir) or not all(os.path.exists(os.path.join(model_dir, file)) for file in FILES):
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            print(f"モデルを {model_dir} にダウンロードしています。モデルID: {MODEL_ID}")

        for sub_dir, sub_dir_files in SUB_DIRS:
            # サブディレクトリパスを正しく設定
            sub_dir_path = os.path.join(model_dir, sub_dir)
            if not os.path.exists(sub_dir_path):
                os.makedirs(sub_dir_path)
            # サブディレクトリ内のファイルをダウンロード
            for file in sub_dir_files:
                file_url = f"https://huggingface.co/{MODEL_ID}/resolve/main/{sub_dir}/{file}"
                output_file = os.path.join(sub_dir_path, file)
                if not os.path.exists(output_file):
                    print(f"{file} を {file_url} から {output_file} にダウンロードしています...")
                    download_file(file_url, output_file)
                    print(f"{file} のダウンロードが完了しました！")

        # ルートディレクトリのファイルをダウンロード
        for file in FILES:
            file_url = f"https://huggingface.co/{MODEL_ID}/resolve/main/{file}"
            output_file = os.path.join(model_dir, file)
            if not os.path.exists(output_file):
                print(f"{file} を {file_url} から {output_file} にダウンロードしています...")
                download_file(file_url, output_file)
                print(f"{file} のダウンロードが完了しました！")

        

def download_files_flat(model_dir, MODEL_ID, SUB_DIRS, FILES):
    """
    モデルディレクトリに指定されたファイルをサブディレクトリ構造を無視してダウンロードします。
    """
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"モデルを {model_dir} にダウンロードしています。モデルID: {MODEL_ID}")

    # サブディレクトリ内のファイルをフラットにダウンロード
    for sub_dir, sub_dir_files in SUB_DIRS:
        download_files(MODEL_ID, sub_dir, sub_dir_files, model_dir, flat=True)

    # ルートディレクトリのファイルもダウンロード
    for file in FILES:
        url = f"https://huggingface.co/{MODEL_ID}/resolve/main/{file}"
        output_file = os.path.join(model_dir, os.path.basename(file))
        if not os.path.exists(output_file):
            print(f"{file} を {url} から {output_file} にダウンロードしています...")
            download_file(url, output_file)
            print(f"{file} のダウンロードが完了しました！")