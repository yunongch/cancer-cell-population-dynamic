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

def draw(x_array, y_array, z_array, filename):
    ax = plt.axes(projection='3d')
    ax.plot3D(x_array, y_array, z_array, 'blue')
    plt.xlabel("u1")
    plt.ylabel("u2")
    # plt.zlabel("u3")
    plt.savefig(filename)
    plt.show()
    plt.close()
    return

def draw2Pic(x1, y1, z1, x2, y2, z2, filename):
    ax = plt.axes(projection='3d')
    ax.plot3D(x1, y1, z1, 'blue')
    ax.plot3D(x2, y2, z2, 'green')
    plt.xlabel("u1")
    plt.ylabel("u2")
    # plt.zlabel("u3")
    plt.savefig(filename)
    plt.show()
    plt.close()
    return

def drawTimeSeries(t, y_array, filename):

    fig, ax = plt.subplots()
    # ax.plot(xf, 2.0 / N * np.abs(y_array[:N // 2]))
    ax.plot(t, y_array)
    plt.savefig(filename)
    plt.close()
    return

def draw2TimeSeries(t, y_array_1, y_array_2, filename):

    fig, ax = plt.subplots()
    # ax.plot(xf, 2.0 / N * np.abs(y_array[:N // 2]))
    ax.plot(t, y_array_1, color="red")
    ax.plot(t, y_array_2, color="green")
    plt.savefig(filename)
    plt.close()
    return

def model(z,t,threshold):
    u1 = z[0]
    u2 = z[1]
    u3 = z[2]
    x = z[3]
    y = z[4]
    du1dt1 = (2 * a1 / (1 + k * u3) - 1) * p1 * u1
    du2dt1 = (2 * a2 / (1 + k * u3) - 1) * p2 * u2 + 2 * (1 - a1 / (1 + k * u3)) * p1 * u1
    du3dt2 = 2 * (1 - a2 / (1 + k * u3)) * p2 * u2 - d3 * u3 * (x + y)
    dxdt = Lambda * x - gamma1 * u3 * x
    dydt = Lambda * y - gamma2 * u3 * y
    dzdt = [du1dt1,du2dt1,du3dt2, dxdt, dydt]  
    if abs(du1dt1) < threshold and abs(du2dt1) < threshold and abs(du3dt2) < threshold:
        print("u1:", u1, "u2:", u2, "u3:", u3)
    return dzdt


def buildSolveArray(z):
    solve_u1 = []
    solve_u2 = []
    solve_u3 = []
    solve_x = []
    solve_y = []
    for solve in z:
        if len(solve) != 5:
            print("[ERROR]solve:", solve, " > or < 5 elements. Skipped.")
            continue
        solve_u1.append(solve[0])
        solve_u2.append(solve[1])
        solve_u3.append(solve[2])
        solve_x.append(solve[3])
        solve_y.append(solve[4])
    return solve_u1, solve_u2, solve_u3, solve_x, solve_y


print("[- Start -]")
makeDir("3dpp")
# Parameters
threshold_a = 30
threshold_b = 290000
a1 = 0.7
a2 = 0.5
p1 = 1
d3 = 0.1337
k = 8.75e-9
Lambda = 0.1
gamma1 = 0.01
gamma2 = 0.1

# Initial conditions A
p2 = 0.4725
z0 = [0.1766e7,1.3082e7,5.9429e7,0,0]

t1 = np.linspace(0.0, 300*10^7, 2000)
t2 = np.linspace(0.0, 300*10^7, 2000)

print("a <", threshold_a, ":")
z, infodict = odeint(model, z0, t1, args = (threshold_a,), full_output = True)
solve_u1, solve_u2, solve_u3, solve_x, solve_y = buildSolveArray(z)
draw(solve_u1, solve_u2, solve_u3, "1.png")
# draw time series
drawTimeSeries(t1, solve_u1, "ts_1_u1.png");
drawTimeSeries(t1, solve_u2, "ts_1_u2.png");
drawTimeSeries(t1, solve_u3, "ts_1_u3.png");
drawTimeSeries(t1, solve_x, "ts_1_x.png");
drawTimeSeries(t1, solve_y, "ts_1_y.png");
print("z1:")
for ele in z:
    print(ele)

# file_u1 = open("u1.txt", "w", encoding="UTF-8")
# for u1 in sorted(solve_u1):
#     file_u1.write(str(u1))
#     file_u1.write("\n")
# file_u1.close()

print("\n\n\n\nb <", threshold_b, ":")
# Initial conditions B
p2 = 0.3544
z0 = [0.2717e7, 2.6836e7, 9.1429e7,0,0]
z, infodict = odeint(model, z0, t1, args = (threshold_b,), full_output = True)
solve_u1_1, solve_u2_1, solve_u3_1, solve_x_1, solve_y_1 = buildSolveArray(z)
print("z2:")
for ele in z:
    print(ele)
# draw time series
drawTimeSeries(t1, solve_u1_1, "ts_2_u1.png");
drawTimeSeries(t1, solve_u2_1, "ts_2_u2.png");
drawTimeSeries(t1, solve_u3_1, "ts_2_u3.png");
drawTimeSeries(t1, solve_x_1, "ts_2_x.png");
drawTimeSeries(t1, solve_y_1, "ts_2_y.png");


# Initial conditions B2
z0 = [0.1766e7, 1.7443e7, 5.9429e7,0,0]
z, infodict = odeint(model, z0, t2, args = (threshold_b,), full_output = True)
solve_u1_2, solve_u2_2, solve_u3_2, solve_x_2, solve_y_2 = buildSolveArray(z)
draw2Pic(solve_u1_1, solve_u2_1, solve_u3_1, solve_u1_2, solve_u2_2, solve_u3_2, "2.png")
# draw 2 time series
drawTimeSeries(t1, solve_u1_2, "ts_3_u1.png");
drawTimeSeries(t1, solve_u2_2, "ts_3_u2.png");
drawTimeSeries(t1, solve_u3_2, "ts_3_u3.png");
drawTimeSeries(t1, solve_x_2, "ts_3_x.png");
drawTimeSeries(t1, solve_y_2, "ts_3_y.png");
print("z3:")
for ele in z:
    print(ele)

print("[- End -]")
