import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 0. Initial Data ---
data = [27.853, 28.371, 28.462, 28.943, 29.936, 30.176, 30.315, 30.919, 31.956, 32.122, 32.256, 33.012]
time_index = np.arange(1, len(data) + 1)
df = pd.DataFrame({'t': time_index, 'y': data})
df['quarter'] = (df['t'] - 1) % 4 + 1  # 1, 2, 3, 4

print("--- 1. Anomaly Detection (Irwin's Method) ---")
# Lecture formula (1): S_y calculation 
std_dev = np.std(df['y'], ddof=1) 
irwin_critical = 1.4  # Interpolated for n=16 based on lecture table 

#df['lambda'] = 0.0
#anomalies_found = False

#for i in range(1, len(df)):
#    # Irwin statistic lambda = |y_t - y_{t-1}| / S_y [cite: 42]
#    diff = abs(df.loc[i, 'y'] - df.loc[i-1, 'y'])
#    lambda_val = diff / std_dev
#    df.loc[i, 'lambda'] = lambda_val
#    if lambda_val > irwin_critical:
#        print(f"Anomaly detected at t={df.loc[i, 't']} (Value: {df.loc[i, 'y']})")
#        # Simple Exp Smoothing: S_t = alpha*y_t + (1-alpha)*S_{t-1}
#        # Using alpha = 0.3
#        alpha = 0.3
#        prev_smooth = df.loc[i-1, 'y']
#        smoothed_val = alpha * df.loc[i, 'y'] + (1 - alpha) * prev_smooth
#        print(f" -> Replacing {df.loc[i, 'y']} with smoothed value: {smoothed_val:.2f}")
#        df.loc[i, 'y'] = smoothed_val
#        anomalies_found = True
#if not anomalies_found:
#    print("No anomalies exceeded the critical value based on Irwin's criterion.")
#alpha = 0.3
#df['y_smoothed'] = 0.0
#df.loc[0, 'y_smoothed'] = df.loc[0, 'y']
#for i in range(1, len(df)):
#    smoothed_val = alpha * df.loc[i, 'y'] + (1 - alpha) * df.loc[i-1, 'y']
#    df.loc[i, 'y'] = smoothed_val
#print("\nСкорректированный временной ряд после обработки аномалий:")
#print(df[['t', 'quarter', 'y']].round(2)) 


print(df.loc)
print("\n--- 2. Seasonal Components (Multiplicative) ---")
# 1. 4-period moving average
df['MA4'] = df['y'].rolling(window=4, min_periods=4).mean()
#print(df['MA4'].round(2))

df['CMA'] = df['y'].rolling(window=4, center=True).mean()
#print(df['CMA'].round(2))
# Calculate Seasonal Ratios (A / T = S * E) 
df['S_raw'] = df['y'] / df['CMA']
print(df['S_raw'])
# Average ratios by quarter
seasonal_indices = df.groupby('quarter')['S_raw'].mean()

# Correction (Normalization) so sum equals 4 
correction_factor = 4 / seasonal_indices.sum()
seasonal_indices = seasonal_indices * correction_factor

seasonal_indices = pd.Series([0.90504, 0.985694, 1.063891, 1.045372], index=[1, 2, 3, 4])

print("Seasonal Indices (S):")
print(seasonal_indices)

print("\n--- 3. Trend Determination (Polynomial) ---")
# Deseasonalize the data (A / S = T) 
# Map indices back to the main dataframe
df['S_index'] = df['quarter'].map(seasonal_indices)
df['y_deseasonalized'] = df['y'] / df['S_index']

# Fit Polynomial y = a + bt + ct^2 (Degree 2)
coeffs = np.polyfit(df['t'], df['y_deseasonalized'], 2)
c, b, a = coeffs
trend_func = np.poly1d(coeffs)
df['Trend'] = trend_func(df['t'])
print(f"Trend Equation: T = {a:.2f} + {b:.2f}t + {c:.4f}t^2")

print("\n--- 4 & 5. Random Component & MSE ---")
#  T * S
df['Model_Value'] = df['Trend'] * df['S_index']
df['Error'] = df['y'] - df['Model_Value']
mad = df['Error'].abs().mean()
rmad = (mad / df['y'].mean()) * 100

print(f"Mean Absolute Deviation (MAD): {mad:.2f}")
print(f"Relative Mean Absolute Deviation (RMAD): {rmad:.2f}%")
mse = (df['Error'] ** 2).mean()
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

print("\n--- 6. Forecast (Next 2 Years) ---")
future_t = np.arange(17, 25) # Next 8 quarters
forecast_df = pd.DataFrame({'t': future_t})
forecast_df['quarter'] = (forecast_df['t'] - 1) % 4 + 1

forecast_df['Trend'] = trend_func(forecast_df['t'])
forecast_df['S_index'] = forecast_df['quarter'].map(seasonal_indices)
forecast_df['Forecast'] = forecast_df['Trend'] * forecast_df['S_index']
print(forecast_df['Trend'])
print(forecast_df[['t', 'quarter', 'Forecast']].to_string(index=False))

# --- Visualization (Optional but recommended) ---
#plt.figure(figsize=(10, 6))
#plt.plot(df['t'], df['y'], marker='o', label='Actual Data')
#plt.plot(df['t'], df['Model_Value'], linestyle='--', label='Model (T*S)')
#plt.plot(forecast_df['t'], forecast_df['Forecast'], marker='x', linestyle='--', color='red', label='Forecast')
#plt.title('Sales Volume: Actual vs Model vs Forecast (Multiplicative)')
#plt.xlabel('Time (t)')
#plt.ylabel('Sales Volume')
#plt.legend()
#plt.grid(True)
#plt.show()