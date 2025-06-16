## AI駆動型MBSEプロセス実証: 自動販売機モデル

### 概要
このリポジトリは、MBSE（モデルベースシステムズエンジニアリング）の開発プロセスにAIによる検証支援を組み込むアプローチを、具体的な「自動販売機」モデルを通じて実証するプロジェクトです。

設計成果物をテキストベースのPlantUMLで記述し、GitHub Copilot (OpenAI API) を活用してモデルの整合性・網羅性を自動検証するフレームワークを提示します。これにより、設計品質の向上と開発プロセスの効率化を目指します。

#### このリポジトリが示すもの
- AIを活用したMBSEプロセスの一例: 上流工程の設計・検証フェーズでAIの支援を受ける具体的な開発フロー。
- PlantUMLによるモデルのテキスト化: AIによる解析を可能にするための「モデルのコード化」の実践。
- プロンプトによる設計検証: 要求カバレッジ、図間整合性、リスク対応カバレッジなどをAIに検証させるための具体的なプロンプト例。
- ローカルLLMへの展開構想: セキュリティを確保しつつ企業利用を可能にするための、ローカルLLM活用への道筋。

#### 技術スタック
モデリング: PlantUML
AI: OpenAI API (GPT-4.1), GitHub Copilot
検証ツール: Python, Streamlit
その他: Java (PlantUMLの実行に必要)

#### セットアップと使い方
1. 前提条件
- Python 3.9以上
- Java (PlantUMLの実行に必要)
- OpenAI APIキー
  
2. セットアップ
```
# 1. リポジトリをクローン
git clone https://github.com/your-username/VendingMachine.git
cd VendingMachine

# 2. 必要なライブラリをインストール
pip install -r requirements.txt

# 3. OpenAI APIキーを設定
export OPENAI_API_KEY='your_api_key_here'
```

3. モデル画像の生成
ディレクトリ内のすべてのPlantUMLファイルをPNG画像に変換します。
```
python create_imager.py
```
4. AIによる設計検証
Streamlitで構築された検証ツールを起動します。

```
streamlit run ai_doc_checker_app.py
```
ブラウザでツールが立ち上がったら、ドロップダウンから検証したい項目を選択し、実行ボタンを押してください。

### 今後の展望：Enterprise Architect (EA) + SysMLへの展開

本プロジェクトで確立したコンセプトを、より本格的なMBSE環境へ展開することを目指します。

#### 課題：PlantUMLベースのアプローチの限界
PlantUMLはテキストベースでAIとの親和性が高い一方で、以下の課題があります。

- 表現力の限界: 正式なSysMLをサポートしておらず、複雑なモデルを表現しきれない可能性があります。
- 学習コスト: 業界標準のEAやCameo等に比べ、利用経験のあるエンジニアが少なく、チーム展開には学習コストが伴います。

#### 次のステップ：EAとXMIを活用したAI支援
これらの課題を解決するため、Enterprise Architectを中核とした以下のプロセスを構想しています。

- SysMLによるモデリング: EA上でSysMLを用いて、より表現力豊かで厳密なモデリングを行います。
- XMIによるモデルのエクスポート: EAのAPIを利用してモデル情報をテキスト（XMI形式）で出力します。
- AIによるテキストベースの検証: PythonスクリプトでXMIから必要なメタデータを抽出し、整形した上でGitHub Copilot (AI) に連携。これにより、PlantUMLと同様のテキストベースの検証支援を実現します。