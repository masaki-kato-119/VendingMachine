# VendingMachine

### 本リポジトリの目的

- GitHub Copilotを活用した自動販売機モデルの自動生成およびモデル検証の自動化を検証するためのコンテンツです。
- MBSE（モデルベースシステムズエンジニアリング）ベースの開発プロセスを前提としていますが、GitHub Copilotによる作成支援・検証を円滑に行うため、モデル記述にはPlantUMLを使用しています。
- PlantUMLはSysMLモデルを直接サポートしていないため、本プロジェクトでは一部でUMLモデルに定義されていない情報を独自に付加しています。

### 今後の展望

- 本プロジェクトで実効性が確認できた段階で、Enterprise Architectを使用したSysML版のコンテンツを作成する予定です。
- Enterprise ArchitectのAPIを利用して画像出力を行い、GitHub Copilotを活用したAIによる検証支援を目指します。
  - AIによる作成支援については、現時点でGitHub CopilotがEAのモデル生成に対応していないため、PlantUMLを生成し、手動でEAに入力する運用を想定しています。