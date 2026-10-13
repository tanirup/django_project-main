# Djangoプロジェクト セットアップ手順

## 1. プロジェクトの準備

```bash
git clone <リポジトリURL>
cd <プロジェクト名>
```

## 2. 仮想環境の作成・有効化

```bash
python3 -m venv venv
source venv/bin/activate
```

※ 仮想環境の作成は初回のみ。

## 3. 必要なライブラリのインストール

```bash
python -m pip install django pymysql "mysqlclient>=2.2.1"
```

インストールでエラーが出た場合（Mac）：

```bash
brew install mysql pkg-config
python -m pip install --upgrade mysqlclient
```

## 4. MySQLの設定

`django_project/settings.py` の `DATABASES` を確認する。

```python
import os

# DATABASES内
'PASSWORD': os.environ['DB_PASSWORD'],
```

環境変数を設定する。

```bash
export DB_PASSWORD='自分のMySQLパスワード'
```

※ パスワードをGitHubにPushしないこと。

## 5. Djangoの起動

`manage.py` があるフォルダで実行する。

```bash
python manage.py runserver
```

アクセス先：http://127.0.0.1:8000/

---

## 毎回の起動手順

```bash
cd ~/Downloads/django_project-main
source venv/bin/activate
export DB_PASSWORD='自分のMySQLパスワード'
python manage.py runserver
```

終了：`Ctrl + C`

仮想環境の終了：

```bash
deactivate
```

---

## よくあるエラー

| エラー | 対処方法 |
|---|---|
| `manage.py` が見つからない | `find . -name manage.py` |
| `No module named django` | `pip install django` |
| `No module named pymysql` | `pip install pymysql` |
| `No module named MySQLdb` | `pip install mysqlclient` |
| `mysqlclient` が古い | `pip install --upgrade mysqlclient` |
| `externally-managed-environment` | 仮想環境を有効化する |
| `Access denied for user` | MySQLのユーザー名・パスワードを確認 |

## 注意事項

- `venv/` は `.gitignore` に追加する。
- MySQLのパスワードをGitHubに公開しない。
- MySQLサーバーを起動しておく。
- MySQLのデータベースとユーザーは各自で準備する。
