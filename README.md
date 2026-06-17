# 📈 股票技術分析應用程式

一個基於 Streamlit 的互動式股票技術分析工具，支援實時數據、多種技術指標和數據可視化。

## 功能特色

✅ **即時股票數據** - 使用 yfinance 獲取最新數據  
✅ **多種技術指標** - SMA、EMA、RSI、MACD、布林帶  
✅ **互動式界面** - 可自定義時間範圍和指標參數  
✅ **數據可視化** - 美觀的圖表展示  
✅ **數據下載** - 可下載分析結果為 CSV  
✅ **支持全球股票** - 台股、美股等均可分析  

## 快速開始

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 運行應用
```bash
streamlit run stock_analysis_app.py
```

然後在瀏覽器中訪問 `http://localhost:8501`

## 支持的股票代號範例

- `AAPL` - Apple
- `MSFT` - Microsoft
- `GOOGL` - Google
- `TSLA` - Tesla
- `0050.TW` - 台灣 50
- `2330.TW` - 台積電
- `2454.TW` - 聯發科

## 技術指標說明

### SMA (Simple Moving Average) - 簡單移動平均
計算過去 N 天的平均價格，用於識別趨勢方向。

### EMA (Exponential Moving Average) - 指數移動平均
給予最近的價格更多權重的移動平均，反應更靈敏。

### RSI (Relative Strength Index) - 相對強弱指數
- 值 > 70：超買信號
- 值 < 30：超賣信號

### MACD (Moving Average Convergence Divergence)
用於識別價格趨勢變化和動量。

### 布林帶 (Bollinger Bands)
用於識別價格的支撐和阻力位置。

## 在 Streamlit Cloud 上部署

1. 將代碼推送到 GitHub
2. 訪問 https://streamlit.io/cloud
3. 用 GitHub 帳號登入
4. 點擊 "New app"
5. 選擇此 repository 和 `stock_analysis_app.py` 文件
6. 點擊 "Deploy"

## 許可證

MIT