import numpy as np
import matplotlib.pyplot as plt

def simulate_oxidation(environment, T_celsius, t_hours, x_i):
    # Hằng số Boltzmann (eV/K)
    k = 8.617e-5
    T_kelvin = T_celsius + 273.15

    # Cấu hình thông số cho từng môi trường
    params = {
        'dry': {'C1': 7.72e2, 'E1': 1.23, 'C2': 6.23e6, 'E2': 2.0},
        'wet': {'C1': 2.14e2, 'E1': 0.71, 'C2': 8.95e7, 'E2': 2.05},
        'h2o': {'C1': 3.86e2, 'E1': 0.78, 'C2': 1.63e8, 'E2': 2.05}
    }

    p = params[environment.lower()]

    # 1. Tính B (Parabolic rate constant)
    B = p['C1'] * np.exp(-p['E1'] / (k * T_kelvin))

    # 2. Tính B/A (Linear rate constant) từ C2 và E2
    # Dựa trên công thức bạn đưa: A = B / (C2 * exp(-E2/kT)) => B/A = C2 * exp(-E2/kT)
    B_over_A = p['C2'] * np.exp(-p['E2'] / (k * T_kelvin))
    A = B / B_over_A

    # 3. Tính Tau (Thời gian hiệu chỉnh cho lớp oxit ban đầu)
    tau = (x_i**2 + A * x_i) / B

    # 4. Tính độ dày Oxit xo theo thời gian t
    # Công thức: xo = (A/2) * (sqrt(1 + (t + tau)/(A^2/4B)) - 1)
    xo = (A / 2) * (np.sqrt(1 + (t_hours + tau) / (A**2 / (4 * B))) - 1)

    return xo

# Lấy input từ người dùng cho x_i
x_i = float(input("độ dày lớp oxide ban đầu (µm): "))

# --- THIẾT LẬP MÔ PHỎNG ---
t_range = np.linspace(0, 10, 100)  # Thời gian từ 0 đến 10 giờ
temperatures = [700, 800, 900, 1000, 1100, 1200]
environments = ['dry', 'wet', 'h2o']

# Vẽ biểu đồ cho mỗi môi trường
for current_env in environments:
    plt.figure(figsize=(10, 6))
    for T in temperatures:
        thickness = [simulate_oxidation(current_env, T, t, x_i=x_i) for t in t_range]
        plt.plot(t_range, thickness, label=f'T = {T}°C')

    plt.title(f'Sự phát triển lớp SiO2 trong môi trường {current_env.upper()} (x_i={x_i:.2f} µm)')
    plt.xlabel('Thời gian (giờ)')
    plt.ylabel('Độ dày Oxit (µm)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
