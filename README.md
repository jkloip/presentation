# 🍌 Nano Banana Pro - 超萌 AI 簡報生成器

**Nano Banana Pro** 是一個充滿活力的簡報生成工具，讓製作投影片變得像吃香蕉一樣快樂！透過整合 Google Gemini 3 (Imagen 3) 的強大生成能力，搭配精心設計的「香蕉主題」UI，讓你輕鬆將創意轉化為精美的簡報。

## ✨ 特色功能 (Features)

* **🍌 超萌互動介面**：客製化的 CSS 樣式，擁有活潑的漸層背景、彈跳標題與可愛的按鈕設計。
* **🤖 Google Gemini 3 整合**：利用最新的 Imagen 3 模型生成高畫質投影片背景。
* **🎨 多種視覺風格**：內建台北捷運、文青咖啡館、清水模、科技漸層等多種風格 Prompt。
* **📊 完整匯出功能**：
    * 支援匯出為可編輯的 **PowerPoint (.pptx)** 檔案。
    * 生成 **HTML 網頁預覽**。
    * 支援 **JSON** 格式備份專案數據。
* **💰 成本透明化**：即時計算 Token 與圖片生成費用（基於 API 定價），並提供統計儀表板。
* **🎉 正能量滿滿**：內建隨機鼓勵訊息與慶祝動畫，讓開發過程不再枯燥。

## 🛠️ 技術堆疊 (Tech Stack)

* **Frontend**: [Streamlit](https://streamlit.io/) (包含大量自定義 CSS)
* **AI Model**: Google Gemini 3 (via `google-genai` SDK)
* **Export**: `python-pptx`
* **Environment**: `python-dotenv`

## 🚀 快速開始 (Quick Start)

### 1. 安裝依賴
確保你已經安裝了 Python 3.8+，然後執行：

```bash
pip install streamlit google-genai python-dotenv python-pptx