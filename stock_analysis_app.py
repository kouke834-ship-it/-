import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import ta
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="股票技術分析", layout="wide")

# Title
st.title("📈 股票技術分析應用程式")
st.markdown("---")

# Sidebar - 使用者輸入
st.sidebar.header("設定參數")

# 股票代號輸入
stock_symbol = st.sidebar.text_input("輸入股票代號", value="AAPL", placeholder="例如: AAPL, MSFT, 0050.TW").upper()

# 日期範圍選擇
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.sidebar.date_input(
        "開始日期",
        value=datetime.now() - timedelta(days=365),
        max_value=datetime.now()
    )
with col2:
    end_date = st.sidebar.date_input(
        "結束日期",
        value=datetime.now(),
        max_value=datetime.now()
    )

# 技術指標選擇
st.sidebar.header("技術指標")
show_sma = st.sidebar.checkbox("簡單移動平均 (SMA)", value=True)
show_ema = st.sidebar.checkbox("指數移動平均 (EMA)", value=True)
show_rsi = st.sidebar.checkbox("相對強弱指數 (RSI)", value=True)
show_macd = st.sidebar.checkbox("MACD", value=True)
show_bb = st.sidebar.checkbox("布林帶 (Bollinger Bands)", value=True)

# 移動平均線參數
if show_sma or show_ema:
    st.sidebar.header("移動平均線參數")
    sma_period = st.sidebar.slider("SMA 週期", 5, 200, 20)
    ema_period = st.sidebar.slider("EMA 週期", 5, 200, 12)

# 獲取股票數據
@st.cache_data
def fetch_stock_data(symbol, start, end):
    try:
        data = yf.download(symbol, start=start, end=end, progress=False)
        return data
    except:
        st.error(f"無法獲取 {symbol} 的數據。請檢查股票代號是否正確。")
        return None

# 計算技術指標
def calculate_indicators(df):
    # SMA
    if show_sma:
        df['SMA'] = ta.trend.sma_indicator(df['Close'], window=sma_period)
    
    # EMA
    if show_ema:
        df['EMA'] = ta.trend.ema_indicator(df['Close'], window=ema_period)
    
    # RSI
    if show_rsi:
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    # MACD
    if show_macd:
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['Signal'] = macd.macd_signal()
        df['Histogram'] = macd.macd_diff()
    
    # Bollinger Bands
    if show_bb:
        bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
        df['BB_High'] = bb.bollinger_hband()
        df['BB_Mid'] = bb.bollinger_mavg()
        df['BB_Low'] = bb.bollinger_lband()
    
    return df

# 主程式邏輯
if stock_symbol:
    # 獲取數據
    df = fetch_stock_data(stock_symbol, start_date, end_date)
    
    if df is not None and len(df) > 0:
        # 計算指標
        df = calculate_indicators(df)
        
        # 顯示基本信息
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("最新收盤價", f"${df['Close'].iloc[-1]:.2f}")
        with col2:
            change = df['Close'].iloc[-1] - df['Close'].iloc[0]
            change_pct = (change / df['Close'].iloc[0]) * 100
            st.metric("變化", f"${change:.2f}", f"{change_pct:.2f}%")
        with col3:
            st.metric("最高價", f"${df['High'].max():.2f}")
        with col4:
            st.metric("最低價", f"${df['Low'].min():.2f}")
        
        st.markdown("---")
        
        # 繪製價格和技術指標圖表
        st.subheader("價格走勢與技術指標")
        
        # 創建圖表
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # 繪製收盤價
        ax.plot(df.index, df['Close'], label='收盤價', color='black', linewidth=2)
        
        # 繪製 SMA
        if show_sma and 'SMA' in df.columns:
            ax.plot(df.index, df['SMA'], label=f'SMA {sma_period}', alpha=0.7)
        
        # 繪製 EMA
        if show_ema and 'EMA' in df.columns:
            ax.plot(df.index, df['EMA'], label=f'EMA {ema_period}', alpha=0.7)
        
        # 繪製布林帶
        if show_bb and 'BB_High' in df.columns:
            ax.fill_between(df.index, df['BB_High'], df['BB_Low'], alpha=0.1, color='gray')
            ax.plot(df.index, df['BB_High'], label='布林帶上軌', alpha=0.5, linestyle='--')
            ax.plot(df.index, df['BB_Low'], label='布林帶下軌', alpha=0.5, linestyle='--')
        
        ax.set_xlabel('日期')
        ax.set_ylabel('價格 ($)')
        ax.set_title(f'{stock_symbol} - 價格走勢')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        
        # RSI 圖表
        if show_rsi and 'RSI' in df.columns:
            st.subheader("相對強弱指數 (RSI)")
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.plot(df.index, df['RSI'], label='RSI (14)', color='purple')
            ax.axhline(y=70, color='r', linestyle='--', label='超買 (70)')
            ax.axhline(y=30, color='g', linestyle='--', label='超賣 (30)')
            ax.fill_between(df.index, 70, 100, alpha=0.1, color='red')
            ax.fill_between(df.index, 0, 30, alpha=0.1, color='green')
            ax.set_ylabel('RSI')
            ax.set_title('相對強弱指數')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        # MACD 圖表
        if show_macd and 'MACD' in df.columns:
            st.subheader("MACD")
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.plot(df.index, df['MACD'], label='MACD', color='blue')
            ax.plot(df.index, df['Signal'], label='Signal', color='red')
            ax.bar(df.index, df['Histogram'], label='Histogram', alpha=0.3)
            ax.set_ylabel('MACD 值')
            ax.set_title('MACD 指標')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        # 顯示數據表格
        st.subheader("最近數據")
        st.dataframe(df.tail(10).sort_index(ascending=False))
        
        # 下載數據
        st.subheader("下載數據")
        csv = df.to_csv()
        st.download_button(
            label="下載 CSV 文件",
            data=csv,
            file_name=f"{stock_symbol}_stock_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("無法獲取股票數據，請檢查股票代號或日期範圍。")
else:
    st.info("👈 請在左側邊欄輸入股票代號開始使用")