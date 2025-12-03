# GitHub 部署指南

## 🚀 步驟 1: 初始化 Git 儲存庫

在專案目錄執行：

```bash
# 初始化 Git
git init

# 添加所有檔案
git add .

# 第一次 commit
git commit -m "Initial commit: Weather crawler with Streamlit UI"

# 連結到您的 GitHub 儲存庫
git remote add origin https://github.com/pcchou102/cwa_weather.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## ☁️ 步驟 2: 部署到 Streamlit Cloud

1. 前往 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用 GitHub 帳號登入
3. 點擊 "New app"
4. 選擇您的儲存庫：`pcchou102/cwa_weather`
5. 設定：
   - **Main file path:** `weather_app.py`
   - **App URL:** `cwa-weather` (或您喜歡的名稱)
6. 點擊 "Deploy!"

## 🔑 步驟 3: 設定環境變數（選用）

如果需要設定自訂 API 金鑰：

1. 在 Streamlit Cloud 應用設定中
2. 進入 "Secrets" 頁面
3. 添加：
```toml
CWA_API_KEY = "your-api-key-here"
```

## 📝 更新程式碼

之後更新程式碼時：

```bash
# 查看變更
git status

# 添加變更的檔案
git add .

# Commit
git commit -m "描述您的變更"

# 推送到 GitHub
git push
```

Streamlit Cloud 會自動偵測變更並重新部署！

## 🌐 您的應用網址

部署完成後，您的應用將可在以下網址存取：
- https://cwa-weather.streamlit.app
- 或您設定的自訂網址

## ❓ 疑難排解

**問題：推送到 GitHub 時要求登入**
```bash
# 使用 Personal Access Token
# 前往 GitHub Settings > Developer settings > Personal access tokens
# 建立新的 token，使用它作為密碼
```

**問題：Streamlit 部署失敗**
- 檢查 `requirements.txt` 是否正確
- 確認 `weather_app.py` 在根目錄
- 查看 Streamlit Cloud 的錯誤日誌
