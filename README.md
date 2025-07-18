# エモーション画像ジェネレータ (Emotion Image Generator)

このアプリは、ユーザーがアップロードした画像から感情を分析し、その感情を表現した新しい画像を生成するStreamlitウェブアプリケーションです。Azure OpenAIのGPT-4oとDALL-E 3を活用しています。

![Demo](static/background_forAzureAIDemo.png)

## 🌟 機能概要

- **複数画像分析**: 最大20枚の画像をアップロードして一括感情分析
- **AI感情抽出**: GPT-4oによる画像からの感情抽出（10個の形容詞）
- **創作画像生成**: 抽出された感情に基づいたDALL-E 3による画像生成
- **美しいUI**: カスタム背景とモダンなデザインの日本語インターフェース
- **ステートフル体験**: セッション状態管理による段階的なワークフロー

## 📋 必要条件

- Python 3.10以上
- Azure OpenAIのアカウントとAPIキー
- GPT-4oとDALL-E 3へのアクセス権限

## 🚀 セットアップ

### ローカル環境での実行

1. **リポジトリをクローン**
   ```bash
   git clone <repository-url>
   cd demo_app
   ```

2. **依存関係をインストール**
   ```bash
   pip install -r main/requirements.txt
   ```

3. **Azure OpenAI資格情報の設定**
   
   `main/emo_img_streamlit.py`の以下の部分を更新:
   ```python
   endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"  # あなたのAzure OpenAIエンドポイント
   api_key = "YOUR_AZURE_OPENAI_API_KEY"   # あなたのAzure OpenAI APIキー
   ```

4. **アプリを実行**
   ```bash
   streamlit run main/emo_img_streamlit.py
   ```

### 🐳 Dockerを使った実行

1. **Dockerイメージをビルド**
   ```bash
   docker build -t emotion-image-generator .
   ```

2. **コンテナを実行**
   ```bash
   docker run -p 80:80 emotion-image-generator
   ```

### ☁️ Azure Web Appsへのデプロイ

このプロジェクトはAzure Web Appsへの自動デプロイ設定が含まれています：

- `.deployment` - ビルド設定
- `.streamlit/config.toml` - ポート80でのサーバー設定
- `.vscode/settings.json` - デプロイ時の除外ファイル設定

## 📖 使い方

### ステップバイステップガイド

1. **画像アップロード**
   - アプリを開くと「エモーション画像ジェネレータ」のインターフェースが表示
   - 「画像ファイルを選んでください」から最大20枚の画像をアップロード

2. **感情分析**
   - 「あなたの心の声を分析」ボタンをクリック
   - GPT-4oが画像を分析し、10個の感情形容詞を抽出

3. **画像生成**
   - 「あなたの心の声を表す画像を生成」ボタンをクリック
   - DALL-E 3が感情に基づいた新しい画像を生成

4. **結果確認**
   - 生成された画像と使用されたプロンプトが表示
   - お祝いのバルーンアニメーション

5. **再実行**
   - 「もう一度試す」または「リセット」で新しい分析を開始

## 📁 プロジェクト構成

```
demo_app/
├── .deployment              # Azure Web Appsデプロイ設定
├── .streamlit/
│   └── config.toml         # Streamlitサーバー設定（ポート80）
├── .vscode/
│   └── settings.json       # VS Code設定（デプロイ除外ファイル）
├── Dockerfile              # Dockerコンテナ設定
├── images/
│   └── generated_image.png # 生成画像の保存先（動的作成）
├── main/
│   ├── emo_img_streamlit.py # メインアプリケーションコード
│   └── requirements.txt    # Python依存パッケージ
├── static/
│   ├── background_forAzureAIDemo.png # デモ用背景画像
│   └── background_original.png       # アプリ背景画像
└── README.md               # このファイル
```

## 🔧 技術スタック

### フロントエンド
- **[Streamlit](https://streamlit.io/)** - ウェブUIフレームワーク
- **カスタムCSS** - 背景画像とモダンなUI

### AI サービス
- **[Azure OpenAI](https://azure.microsoft.com/ja-jp/products/ai-services/openai-service)**
  - **GPT-4o** (`gpt-4o-2`) - 画像分析と感情抽出
  - **DALL-E 3** (`dalle3`) - 画像生成

### その他のライブラリ
- **[Pillow](https://pillow.readthedocs.io/)** - 画像処理
- **[requests](https://requests.readthedocs.io/)** - HTTP通信
- **base64** - 画像エンコーディング
- **json** - データ処理

### デプロイメント
- **[Docker](https://www.docker.com/)** - コンテナ化
- **Azure Web Apps** - クラウドホスティング

## 🔑 主要な関数

### Core Functions

#### `encode_image(image_path)`
画像ファイルをBase64エンコードする関数
```python
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
```

#### `response_gpt4o_with_images(model, client, system_prompt, json_list)`
GPT-4oを使用して画像から感情を分析する関数
- 複数画像を一括処理
- 10個の感情形容詞を抽出

#### `responce_gpt4o_with_text(model, client, system_prompt, emotions)`
感情データからDALL-E用のプロンプトを生成する関数
- 日本語でのプロンプト生成
- 都市の単一オブジェクト表現

#### `call_dalle(client, prompt_by_gpt)`
DALL-E 3を使用して画像を生成し、ローカルに保存する関数
- 画像URL取得とダウンロード
- `images/`フォルダへの自動保存

## ⚙️ 設定詳細

### Azure OpenAI設定
```python
api_version="2024-02-01"
temperature=1.0  # 創造性重視
model="gpt-4o-2"  # 画像分析・テキスト生成
image_model="dalle3"  # 画像生成
```

### システムプロンプト
- **感情抽出用**: アップロードされた全画像から10個の形容詞を抽出
- **画像生成用**: 感情に関連した都市の単一オブジェクトを日本語で表現

### Streamlit設定
- **ポート**: 80（本番環境対応）
- **UI**: 日本語インターフェース
- **背景**: `static/background_original.png`

## 🎨 カスタマイズ

### 背景画像の変更
`static/`フォルダに新しい画像を配置し、`main/emo_img_streamlit.py`の`image`変数を更新:
```python
image = r'static/your_new_background.png'
```

### プロンプトの調整
システムプロンプトを変更して、異なる分析スタイルや生成スタイルに対応可能:
```python
system_prompt_for_get_emotions = "カスタムプロンプト..."
system_prompt_for_generate_image = "カスタムプロンプト..."
```

## 🔒 セキュリティ注意事項

- **API キー**: 本番環境では環境変数を使用してAPIキーを管理
- **ファイルアップロード**: 画像ファイルのみ許可（拡張子チェック実装済み）
- **セッション管理**: Streamlitのセッション状態で安全に管理

## 🚨 トラブルシューティング

### よくある問題

1. **API エラー**
   - Azure OpenAIの資格情報を確認
   - モデルへのアクセス権限を確認

2. **画像が表示されない**
   - `static/background_original.png`の存在を確認
   - ファイルパスの区切り文字（Windows: `\`, Linux/Mac: `/`）

3. **Docker ビルドエラー**
   - Dockerfileの権限設定を確認
   - 必要なファイルが含まれているか確認

### ログの確認
Streamlitアプリのログは標準出力に表示されます：
```bash
streamlit run main/emo_img_streamlit.py --logger.level debug
```

## 📄 ライセンス

このプロジェクトは研究・教育目的で作成されています。

## 🤝 コントリビューション

プルリクエストやイシューの報告を歓迎します。

---

**開発者**: KOBE_LAB  
**プロジェクト**: Demo Application  
**最終更新**: 2025年7月
