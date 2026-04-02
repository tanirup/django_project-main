# Djangoプロジェクトの実行方法メモ

## 1. プロジェクトフォルダへ移動

```bash
cd ~/Downloads/django_project-main
```

## 2. 仮想環境を作る（最初の1回だけ）

```bash
python3 -m venv venv
```

## 3. 仮想環境を有効化する

```bash
source venv/bin/activate
```

有効化できると、ターミナルの左に `(venv)` が出る。

## 4. 必要なライブラリを入れる

```bash
python -m pip install django pymysql
python -m pip install --upgrade "mysqlclient>=2.2.1"
```

`mysqlclient` でエラーが出たら、先にこれを入れる。

```bash
brew install mysql pkg-config
```

そのあともう一度。

```bash
python -m pip install --no-cache-dir "mysqlclient>=2.2.1"
```

## 5. Djangoを起動する

```bash
python manage.py runserver
```

ブラウザで開く:

```bash
http://127.0.0.1:8000/
```

---

# 毎回の起動手順

```bash
cd ~/Downloads/django_project-main
source venv/bin/activate
python manage.py runserver
```

終わるとき:

```bash
deactivate
```

---

# よくあるエラー

## `No such file or directory: manage.py`

今いる場所に `manage.py` がない。

確認:

```bash
find . -name manage.py
```

## `ModuleNotFoundError: No module named 'pymysql'`

`pymysql` が入っていない。

対処:

```bash
source venv/bin/activate
python -m pip install pymysql
```

## `mysqlclient 2.2.1 or newer is required; you have 1.4.6`

`mysqlclient` が古い。

対処:

```bash
source venv/bin/activate
python -m pip uninstall -y mysqlclient
python -m pip install --no-cache-dir "mysqlclient>=2.2.1"
python -m pip show mysqlclient
```

## `externally-managed-environment`

Homebrew の Python に直接入れようとしている。

対処:

* 仮想環境 `venv` を使う
* `source venv/bin/activate` してから `pip install` する

---

# 確認コマンド

```bash
which python
which pip
python -V
pip -V
```

`venv` が有効なら、`.../django_project-main/venv/bin/...` が出る。

---

# 最短版

```bash
cd ~/Downloads/django_project-main
source venv/bin/activate
python manage.py runserver
```

