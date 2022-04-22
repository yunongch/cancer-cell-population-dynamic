import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from scipy.integrate import odeint

def scan_csv(path):
    result = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".csv"):
                result.append(f)
    return result


def makeDir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

def draw(x_array, y_array, z_array):
    ax = plt.axes(projection='3d')
    ax.plot3D(x_array, y_array, z_array, 'blue')
    plt.show()
    plt.close()
    return

def drawTimeSeries(y_array):
    # Number of sample points
    N = 100
    # sample spacing
    T = 1.0 / 1000

    xf = np.linspace(0.0, 1.0 // (2.0 * T), N // 2)
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(y_array[:N // 2]))
    plt.show()
    plt.close()
    return

def model1(initials, time_points):
    u1 = initials[0]
    u3 = initials[1]
    y = (2 * a1 / (1 + k * u3) - 1) * p1 * u1
    return y

def model2(initials, time_points):
    u1 = initials[0]
    u2 = initials[1]
    u3 = initials[2]
    y = (2 * a2 / (1 + k * u3) - 1) * p2 * u2 + 2 * (1 - a1 / (1 + k * u3)) * p1 * u1
    return y

def model3(initials, time_points):
    u2 = initials[0]
    u3 = initials[1]
    y = 2 * (1 - a2 / (1 + k * u3)) * p2 * u2 - d3 * u3
    return y


print("[- Start -]")
# Parameters
a1 = 0.7
a2 = 0.5
p1 = 1
d3 = 0.1337
k = 8.75e-9


# Initial conditions A
u1_a = 0.1766e7
u2_a = 1.3082e7
u3_a = 5.9429e7
p2_a = 0.4725

# Initial conditions B
u1_b1 = 0.2717e7
u2_b1 = 2.6836e7
u3_b1 = 9.1429e7
u1_b2 = 0.1766e7
u2_b2 = 1.7443e7
u3_b2 = 5.9429e7
p2_b = 0.3544

# temp
# u1 = u1_a
# u2 = u2_a
# u3 = u3_a
# p2 = p2_a

# ODEs
# ode1 = (2 * a1 / (1 + k * u3) - 1) * p1 * u1
# ode2 = (2 * a2 / (1 + k * u3) - 1) * p2 * u2 + 2 * (1 - a1 / (1 + k * u3)) * p1 * u1
# ode3 = 2 * (1 - a2 / (1 + k * u3)) * p2 * u2 - d3 * u3

t1 = np.linspace(0.0, 1.0//100, 4)
t2 = np.linspace(0.0, 1.0//40, 10*10^7)

du1dt = odeint(model1, [u1_a, u3_a], t1)
du2dt = odeint(model2, [u1_a, u2_a, u3_a], t1)
du3dt = odeint(model3, [u2_a, u3_a], t2)


print(du1dt, "\n\n")
print(du2dt, "\n\n")
print(du3dt, "\n\n")
draw(du1dt, du2dt, du3dt)


print("[- End -]")
