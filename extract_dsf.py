# 认为h20 mass mixing ratio是混合比，利用马格努斯饱和水汽压公式计算饱和水汽压，从而计算得到RH（%）相对湿度
# 臭氧混合比TIGR中是（g/g），tape5里要用到的是（g/kg），所以乘1000
# 大气压
pressure = [2.6e-3, 8.9e-3, 2.4e-2, 0.5E-01, 0.8999997E-01, 0.17E+00, 0.3E+00, 0.55E+00, \
    0.1E+01, 0.15E+01, 0.223E+01, 0.333E+01, 0.498E+01, \
        0.743E+01, 0.1111E+02, 0.1660001E+02, 0.2478999E+02, 0.3703999E+02, \
            0.4573E+02, 0.5646001E+02, 0.6971001E+02, 0.8607001E+02, 0.10627E+03, \
                0.1312E+03, 0.16199E+03, 0.2E+03, 0.22265E+03, 0.24787E+03, \
                    0.27595E+03, 0.3072E+03, 0.34199E+03, 0.38073E+03, 0.4238501E+03, \
                        0.4718601E+03, 0.525E+03, 0.5848E+03, 0.65104E+03, 0.72478E+03, \
                            0.8E+03, 0.8486899E+03, 0.9003301E+03, 0.9551201E+03, 0.1013E+04]
height = [88.072, 80.954, 75.230, 70.893, 66.897, 62.406, 58.241, 53.506, \
    48.730, 45.469, 42.404, 39.351, 36.377, \
        33.206, 30.659, 27.933, 25.242, 22.636, \
            21.303, 20.004, 18.731, 17.494, 16.257, \
                15.035, 13.756, 12.400, 11.701, 10.976, \
                    10.244, 9.489, 8.721, 7.946, 7.143, \
                        6.321, 5.492, 4.637, 3.769, 2.885, \
                            2.053, 1.542, 1.035, 0.517, 0.002]


# 提取中纬度夏季廓线，从873到1260，altitude(km)，pressure(mb)，temperature(K)，water vapor(%)，ozone(g/kg)
for i in range(873, 1261):
    T = []
    H2O = []
    O3 = []
    start = (i - 1) * 26
    with open('atm4atigr2000_v1.2_43lev.dsf', 'r') as f:
        for line in f.readlines()[start + 1: start + 9]:
            curline = line.strip().split()
            floatline = list(map(float, curline))
            T.append(floatline)
    with open('atm4atigr2000_v1.2_43lev.dsf', 'r') as f:
        for line in f.readlines()[start + 10: start + 18]:
            curline = line.strip().split()
            floatline = list(map(float, curline))
            H2O.append(floatline)
    with open('atm4atigr2000_v1.2_43lev.dsf', 'r') as f:
        for line in f.readlines()[start + 18: start + 26]:
            curline = line.strip().split()
            floatline = list(map(float, curline))
            O3.append(floatline)
    T = sum(T, [])
    H2O = sum(H2O, [])
    O3 = sum(O3, [])

    for j in range(len(O3)):
        O3[j] = O3[j] * 1000
    RH = []
    for j in range(len(H2O)):
        E = 6.1078 * pow(10, 7.5 * (T[j] - 273.15) / (237.3 + (T[j] - 273.15)))
        e = H2O[j] * pressure[j] / (0.622 + H2O[j])
        rh = e / E
        RH.append(rh * 100)
    
    pressure_rev = list(reversed(pressure))
    height_rev = list(reversed(height))
    T.reverse()
    RH.reverse()
    O3.reverse()
    with open('./game/test_mid_sum_0/' + str(i) + '.tp5', 'w') as f:
        '''
        for j in range(len(T)):
            f.write(str(format(height_rev[j], '.3f')) + "  " + str(format(pressure_rev[j], '.3f')) + "  " \
                + str(format(T[j], '.3f')) + "  " + str(format(RH[j], '.3f')) + "  " + str(format(O3[j], '.3f')) + "\n")
        '''
        f.write("TMF 7    3    1   -1    0    0    2    2    2    2    0    1    0   0.001    0.0   !card1" + "\n" \
                + "FFF  8 0.0   365.000                    01 F T T       0.000      0.00     0.000     0.000     0.000         0   !card1a" + "\n" \
                    + "D:\modtran5.2\MODTRAN\Sentinel3_SLSTR_S8.flt" + "\n" \
                        + "    1    0    0    0    0    0    23.000     0.000     0.000     0.000     0.500   !card2" + "\n" \
                            + "   43    0    0                           0.0    0     1.000    28.964  !card2c" + "\n" \
                                )
        
        # 顺序依次是高程 压强 气温 水汽含量 二氧化碳（0）臭氧 +AAH C222  2表示其他都用中纬度夏季
        for j in range(len(T)):
            f.write("   " + str(format(height_rev[j], '.3f')).rjust(7) + " " + str(format(pressure_rev[j], '.3e')).lower() + " " \
                + str(format(T[j], '.3e')).lower() + " " + str(format(RH[j], '.3e')).lower() + " " + str(format(0.000, '.3e')).lower() + " " + str(format(O3[j], '.3e')).lower() + "AAH C333" + "\n")

        f.write("   100.000     0.000   180.000     0.000     0.000     0.000    0          0.000 !card3" + "\n" \
            + "   737.000  1000.000       1.0       2.0TM              F  1             !card4" + "\n" \
                + "    0 !card5")
        
        
