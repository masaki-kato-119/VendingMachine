import subprocess
import os
from pathlib import Path

def list_wsd_files(directory):
    """
    指定ディレクトリ内の .wsd ファイル一覧を取得（Pathlib版）

    @param directory: 対象ディレクトリのパス
    @return: .wsd ファイルのリスト（Pathオブジェクト）
    """
    return list(Path(directory).glob("*.wsd"))

def generate_plantuml_image(wsd_file_path, plantuml_jar_path='c:/plantuml.jar', output_format='png'):
    """
    PlantUMLファイル（.wsd）から画像を生成する関数。

    @param wsd_file_path: 入力となる .wsd ファイルのパス
    @param plantuml_jar_path: plantuml.jar のファイルパス（デフォルトはカレントディレクトリ）
    @param output_format: 出力形式（例: 'png', 'svg' など）
    """
    if not os.path.exists(wsd_file_path):
        raise FileNotFoundError(f"{wsd_file_path} が見つかりません")

    if not os.path.exists(plantuml_jar_path):
        raise FileNotFoundError(f"{plantuml_jar_path} が見つかりません")

    # 出力ファイルのパスを決定
    output_file = str(wsd_file_path.with_suffix(f'.{output_format}'))

    # 既存のpngが新しい場合はスキップ
    if os.path.exists(output_file):
        wsd_mtime = os.path.getmtime(wsd_file_path)
        png_mtime = os.path.getmtime(output_file)
        if png_mtime >= wsd_mtime:
            print(f"スキップ: {output_file} は最新です")
            return
        
    # コマンドを構築
    command = [
        'java', '-jar', plantuml_jar_path,
        f'-t{output_format}',  # 出力形式指定
        wsd_file_path
    ]

    # コマンドを実行
    try:
        subprocess.run(command, check=True)
        print(f"生成成功: {wsd_file_path} → {output_format}形式の画像")
    except subprocess.CalledProcessError as e:
        print("PlantUMLの実行中にエラーが発生しました:", e)

if __name__ == '__main__':
    paths = [
        'ユースケース図',
        'ステートマシン図',
        'システム構成図',
        'シーケンス図_機能',
        'コンテキスト図',
        'アクティビティ図_機能',
        'アクティビティ図_ユースケース',
        '要求図',
        'シミュレーション_機能',
        'プロセス',
        'リスク評価',
    ]

    current_dir = os.getcwd()
    for path in paths:
        file_list = list_wsd_files(os.path.join(current_dir, path))
        #file_list = list_wsd_files(path)
        print(file_list)
        for file in file_list:
            print(f"{file}を変換します")
            generate_plantuml_image(file)
            print(f"{file}を変換しました")
            print()
