# strategies.py
def ma_signal_with_params(df, short_period, long_period, threshold_ratio=0.0002):
    """Generate BUY/SELL signal based on EMA crossover."""
    df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()

    short_prev, short_curr = df['ema_short'].iloc[-2], df['ema_short'].iloc[-1]
    long_prev, long_curr = df['ema_long'].iloc[-2], df['ema_long'].iloc[-1]
    latest_close = df['close'].iloc[-1]
    threshold = latest_close * threshold_ratio
    diff = short_curr - long_curr

    # Debug prints
    print(f"[DEBUG] Short EMA: {short_prev:.6f} -> {short_curr:.6f}, "
          f"Long EMA: {long_prev:.6f} -> {long_curr:.6f}, "
          f"Diff: {diff:.6f}, Threshold: {threshold:.6f}")

    if short_prev < long_prev and short_curr > long_curr and abs(diff) > threshold:
        return "BUY"
    elif short_prev > long_prev and short_curr < long_curr and abs(diff) > threshold:
        return "SELL"
    return None
