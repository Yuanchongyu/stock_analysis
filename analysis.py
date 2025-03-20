import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 下载股票数据
def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.dropna(inplace=True)
    return df

# 计算 RSI 指标
def compute_rsi(df, period=14):
    # 差值（今天 - 昨天）
    delta = df['Close'].diff()

    # np.where 结果变一维
    gain_array = np.where(delta > 0, delta, 0).ravel()
    loss_array = np.where(delta < 0, -delta, 0).ravel()

    # 转成 pd.Series，保持 index
    gain = pd.Series(gain_array, index=df.index)
    loss = pd.Series(loss_array, index=df.index)

    # 移动平均
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # RSI 公式
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df['RSI'] = rsi
    return df

# 计算 MACD 指标
def compute_macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()

    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

# 抄底信号检测
def detect_buy_signals(df):
    signals = []
    for i in range(1, len(df)):
        if df['RSI'].iloc[i] < 30:
            signals.append((df.index[i], df['Close'].iloc[i]))
    return signals
# 绘图展示
def plot_signals(df, signals, ticker):
    plt.figure(figsize=(16, 8))
    plt.plot(df['Close'], label='Close Price', color='blue')
    
    for signal in signals:
        plt.scatter(signal[0], signal[1], marker='^', color='green', s=150, label='Buy Signal')
    
    plt.title(f"{ticker} Buy Signals (RSI + MACD)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

# 主程序
if __name__ == "__main__":
    # 参数
    ticker = 'QQQ'  # 你想要分析的股票代码
    start_date = '2025-01-10'
    end_date = '2025-3-30'

    # 获取数据
    df = get_stock_data(ticker, start_date, end_date)
    # 计算指标
    df = compute_rsi(df)
    df = compute_macd(df)
    print(df)
    # 检测抄底信号
    buy_signals = detect_buy_signals(df)
    print(buy_signals)
    # 输出信号
    print(f"\n=== {ticker} 抄底信号 ===")
    # for date, price in buy_signals:
    #     print(f"{date.date()} → 抄底价: {price:.2f}")

    # 画图展示
    plot_signals(df, buy_signals, ticker)