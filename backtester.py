# backtester.py
import pandas as pd
from strategies import ma_signal_with_params

def backtest_ema(df, short_range, long_range, threshold=0.0001):
    """Backtest EMA crossovers to find best short/long periods."""
    best_combo = None
    best_profit = float('-inf')

    for short_period in short_range:
        for long_period in long_range:
            if short_period >= long_period:
                continue
            profit = simulate_trades(df.copy(), short_period, long_period)
            if profit > best_profit:
                best_profit = profit
                best_combo = (short_period, long_period)

    return best_combo, best_profit

def simulate_trades(df, short_period, long_period):
    df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()

    position = None
    profit = 0
    trade_amount = 1
    payout_ratio = 0.8

    for i in range(1, len(df)):
        if df['ema_short'].iloc[i-1] < df['ema_long'].iloc[i-1] and df['ema_short'].iloc[i] > df['ema_long'].iloc[i]:
            if position != 'BUY':
                position = 'BUY'
                profit += trade_amount * payout_ratio
        elif df['ema_short'].iloc[i-1] > df['ema_long'].iloc[i-1] and df['ema_short'].iloc[i] < df['ema_long'].iloc[i]:
            if position != 'SELL':
                position = 'SELL'
                profit += trade_amount * payout_ratio
    return profit
