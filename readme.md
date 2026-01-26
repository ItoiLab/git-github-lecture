# Git & Github の便利な使い方


## 目次

1. [はじめに](#はじめに)
2. [Level 1: 既存コードの利用](#level-1-既存コードの利用)
3. [Level 2: バックアップツールとしての活用](#level-2-バックアップツールとしての活用)
4. [Level 3: ブランチを使用した開発](#level-3-ブランチを使用した開発)
5. [付録](#付録)

---

## はじめに

### レベル構成

- **Level 1**: 既存のコードを使うだけ（読み取り専用）
- **Level 2**: 自分のコードをバックアップ・管理する (ここがメインです。意外とほかのドライブ系ソフトだとできない。)
- **Level 3**: チームで協力して開発する(別に要らないと思う)

---

## Level 1: 既存コードの利用

**目標**: GitHubにあるコードを自分のPCにダウンロードして使えるようになる

### 1.1 Gitのインストール

#### Windows
```bash
# Git for Windowsをダウンロード
# https://git-scm.com/download/win
```

#### macOS
```bash
brew install git
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

#### インストール確認
```bash
git --version
```

### 1.2 基本設定（初回のみ）

```bash
# 名前とメールアドレスを設定
git config --global user.name "あなたの名前"
git config --global user.email "your.email@example.com"
```

### 1.3 既存のリポジトリをクローン

```bash
# GitHubのリポジトリURLをコピーして実行
git clone https://github.com/username/repository-name.git

# フォルダ名を指定してクローン
git clone https://github.com/username/repository-name.git my-project
```

### 1.4 クローンしたコードを使う

```bash
# プロジェクトディレクトリに移動
cd simulation-project

# コードを実行（例）
python main.py
```

### 1.5 最新版に更新する

```bash
# リポジトリ内で実行
git pull
```

### 1.6 【オプション】.gitを削除して単なるフォルダとして使う

「バージョン管理が不要で、単にコードをコピーして使いたい」場合は、`.git`フォルダを削除できます。
クローンしたフォルダがvscode上でキモイ色になって嫌な人は消しちゃっていいと思います。

#### 削除方法

```bash
# クローン後、.gitフォルダを削除
cd simulation-project
rm -rf .git

# Windowsの場合（PowerShell）
Remove-Item -Recurse -Force .git
```

**注意**: `.git`を削除すると以下ができなくなります
- `git pull`での更新
- バージョン履歴の確認
- 変更の追跡

---

## Level 2: バックアップツールとしての活用

**目標**: 自分のコードをGitHubにバックアップし、必要に応じて過去のバージョンに戻せるようになる。
←githubの便利なところです。でかすぎるファイルを扱うのはストレスなので無視して部分的なバックアップがおすすめです。

例えば設定ファイルと初期ファイルだけgithub上に残しておけば万が一データを紛失しても復元できるし、csvの結果だけは選択的にバックアップを取っておく、とかも可能です。

PCごと変更するときも便利です。

### 2.1 GitHubアカウントの作成

1. https://github.com にアクセス
2. Sign upからアカウント作成
3. メールアドレスを認証

### 2.2 新しいリポジトリの作成

#### GitHubでリポジトリを作成

1. GitHubにログイン
2. 右上の「+」→「New repository」
3. リポジトリ名を入力（例: `my-simulation`）
4. Public または Private を選択
5. 「Create repository」をクリック

#### ローカルのプロジェクトとリンク

```bash
# 既存のプロジェクトフォルダに移動
cd ~/my-simulation

# Gitリポジトリとして初期化
git init

# GitHubリポジトリをリモートとして追加
git remote add origin https://github.com/yourusername/my-simulation.git
```

### 2.3 基本ワークフロー: Add → Commit → Push

#### ステップ1: 変更をステージング

```bash
# 全ての変更をステージング
git add .

# 特定のファイルだけステージング
git add simulation.py config.yaml
```

#### ステップ2: 変更をコミット

```bash
# コミットメッセージと共に記録
git commit -m "初回コミット: シミュレーションコードを追加"
```

#### ステップ3: GitHubにプッシュ

```bash
# 初回プッシュ
git push -u origin main

# 2回目以降
git push
```

### 2.4 選択的バックアップ

容量が大きすぎるファイルはgithubにアップロードできません。`.gitignore`で除外するファイルを指定できます。

#### .gitignoreの作成

**研究用プロジェクトの典型的な.gitignore**:

```gitignore
# コンパイル済みファイル
*.o
*.so
*.a
*.pyc
__pycache__/

# 実行ファイル
*.out
*.exe
a.out

# 計算結果データ（大きすぎるため）
*.dat
*.h5
*.hdf5
*.prof
*.profbin
*.vtu
*.vtk

# 一時ファイル
*.tmp
*.log
```

### 2.5 過去のバージョンに戻す

```bash
# まだコミットしていない変更を破棄
git checkout -- filename.py

# 最新のコミットを取り消す（変更は残る）
git reset --soft HEAD^

# 最新のコミットを取り消す（変更も破棄）
git reset --hard HEAD^

# コミット履歴を確認
git log --oneline
```

---

## Level 3: ブランチを使用した開発

**目標**: ブランチを使った効率的な開発ができるようになる。←研究室では不要かもしれません。趣味的にチャレンジするのもいいと思います。

### 3.1 ブランチとは

ブランチは「平行世界」のようなもので、メインの開発ラインに影響を与えずに新機能を開発できます。

```
main     : o---o---o---o
                \
feature  :       o---o (新機能開発中)
```

### 3.2 ブランチの基本操作

```bash
# ブランチを作成して切り替え
git checkout -b feature/new-solver

# ブランチ一覧の確認
git branch

# ブランチの切り替え
git checkout main

# ブランチの削除
git branch -d feature/old-feature
```

### 3.3 ブランチを使った開発フロー

```bash
# 1. mainから新しいブランチを作成
git checkout main
git pull
git checkout -b feature/new-algorithm

# 2. 開発作業
# ... コードを編集 ...
git add .
git commit -m "新しいアルゴリズムを実装"
git push -u origin feature/new-algorithm

# 3. mainに戻ってマージ
git checkout main
git merge feature/new-algorithm

# 4. リモートにプッシュ
git push
```

### 3.4 コンフリクト（競合）の解決

異なるブランチで同じ箇所を編集すると、コンフリクトが発生します。

#### 解決手順

1. コンフリクトしているファイルを開く

```cpp
<<<<<<< HEAD
double dt = 0.001;  // mainブランチの変更
=======
double dt = 0.0001; // featureブランチの変更
>>>>>>> feature/update-solver
```

2. どちらを採用するか編集

```cpp
double dt = 0.0001;  // より精度の高い値を採用
```

3. マーカーを削除して保存

4. 解決したファイルをステージング

```bash
git add solver.cpp
git commit -m "コンフリクトを解決"
```

### 3.5 便利なGitコマンド

#### スタッシュ（一時退避）

```bash
# 現在の変更を一時退避
git stash

# 退避した変更を復元
git stash pop
```

---

## 付録

### A. SSH鍵の設定

パスワード入力を省略するためにSSH鍵を設定します。

```bash
# SSH鍵を生成
ssh-keygen -t ed25519 -C "your.email@example.com"

# 公開鍵をコピー（Mac）
pbcopy < ~/.ssh/id_ed25519.pub

# Linux
cat ~/.ssh/id_ed25519.pub

# GitHubに登録
# 1. GitHub > Settings > SSH and GPG keys
# 2. New SSH key
# 3. コピーした公開鍵を貼り付け
```

### B. よく使うGitコマンド一覧

```bash
# 基本操作
git clone <URL>             # クローン
git status                  # 状態確認
git add .                   # 全てステージング
git commit -m "message"     # コミット
git push                    # プッシュ
git pull                    # プル

# ブランチ
git branch                  # ブランチ一覧
git checkout -b <name>      # ブランチ作成・切替
git merge <branch>          # マージ

# 履歴確認
git log --oneline           # 簡潔な履歴
git diff                    # 差分確認

# 取り消し
git reset --soft HEAD^      # コミット取消（変更は保持）
git checkout -- <file>      # ファイルの変更を破棄
git stash                   # 変更を一時退避
```



## まとめ

### Level 1のゴール
- `git clone`でコードをダウンロードできる
- `git pull`で更新できる
- 必要に応じて`.git`を削除して使える

### Level 2のゴール
- `git add`, `git commit`, `git push`でバックアップできる
- `.gitignore`で不要なファイルを除外できる
- 過去のバージョンに戻せる

### Level 3のゴール
- ブランチを使って並行開発できる
- コンフリクトを解決できる


---
