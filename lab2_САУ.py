
import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import colorama as color
import math
import sympy

def choice1():
    global w1p
    Newchoice = True
    while Newchoice:
        w1a = 'Жесткая обратная связь'
        w1b = 'Гибная обратная связь'
        w1c = 'Апериодическая жесткая обратная связь'
        w1d = 'Апериодичекая гибная обратная связь'
        Newchoice = False
        Userinput = input('Пожалуйста выберете обратную связь\n'
                          'a - '+w1a+'\n'
                          'b - '+w1b+'\n'
                          'c - '+w1c+'\n'
                          'd - '+w1d+'\n')
        Userinput = str(Userinput)
        if Userinput == 'a':
            w1 = w1a
            w1ainput = input('Пожалуйста введите Кос:\n')
            w1p = float(w1ainput)
        elif Userinput == 'b':
            w1 = w1b
            w1binput1 = input('Пожалуйста введите Кос:\n')
            w1p = matlab.tf([float(w1binput1), 0], [1])
        elif Userinput == 'c':
            w1 = w1c
            w1cinput1 = input('Пожалуйста введите Кос:\n')
            w1cinput2 = input('Пожалуйста введите Toc:\n')
            w1p = matlab.tf([float(w1cinput1)], [float(w1cinput2), 1])
        elif Userinput == 'd':
            w1 = w1d
            w1dinput1 = input('Пожалуйста введите Кос:\n')
            w1dinput2 = input('Пожалуйста введите Toc:\n')
            w1p =matlab.tf([float(w1dinput1), 0], [float(w1dinput2), 1])
        else:
            print('Пожалуйста введите правильную букву')
            Newchoice =True

    return w1p
print(choice1())

def choice2():
    global w2p
    Newchoice2 = True
    while Newchoice2:
        print('Это генератор')
        w2input = input('Пожалуйста введите Tг:\n')
        w2p = matlab.tf([1], [float(w2input), 1])
        Newchoice2 = False
    return w2p

print(choice2())

def choice3():
    global w3p
    w3a = 'Для гидравлической турбины'
    w3b = 'Для паровой турбина'
    Newchoice3 = True
    while Newchoice3:
        Userinput3 = input('Пожалуйста выберете турбину\n'
                          '1 - '+w3a+'\n'
                          '2 - '+w3b+'\n')
        Userinput3 = str(Userinput3)
        Newchoice3 = False
        if Userinput3 == '1':
            w3 = w3a
            w3ainput1 = input('Пожалуйста введите Tгт:\n')
            w3ainput2 = input('Пожалуйста введите Tг:\n')
            w3p = matlab.tf([0.01*float(w3ainput1), 1], [0.05*float(w3ainput2), 1])
        elif Userinput3 == '2':
            w3 = w3b
            w3binput1 = input('Пожалуйста введите Кnm:\n')
            w3binput2 = input('Пожалуйста введите Tnm:\n')
            w3p = matlab.tf([float(w3binput1)], [float(w3binput2), 1])
        else:
            print('Пожалуйста введите правильный номер')
            Newchoice3 =True

    return w3p
print(choice3())

def choice4():
    global w4p
    Newchoice4 = True
    while Newchoice4:
        print('Это исполнительное устройство:')
        w4input1 = input('Пожалуйста введите Tу:\n')
        w4input2 = input('Пожалуйста введите kу:\n')
        w4p = matlab.tf([float(w4input2)], [float(w4input1), 1])
        Newchoice4 = False
    return w4p
print(choice4())

# wpclose = matlab.tf([63], [96, 64, 14, 19.9])
wpclose_1 = w4p*w2p*w3p
wpclose_2 = 1+w1p*w2p*w3p*w4p
wpclose = matlab.tf(wpclose_1.num, wpclose_2.num)
wpopen = w1p*w2p*w3p*w4p
def transforfunction():
    # wpclose = (w4p*w2p*w3p)/(1+w1p*w2p*w3p*w4p)
    print('Передаточная функция замкнутой:', wpclose)
    fenfu = wpclose.den
    closeroots = numpy.roots(fenfu[0][0])
    print(closeroots)

    timeline = []
    for i in range(0, 5000):
        timeline.append(i/100)
    [y, x] = matlab.step(wpclose, timeline)
    pyplot.plot(x, y)
    # pyplot.xticks(timeline)
    pyplot.xlabel('t[s]')
    pyplot.ylabel('h(t)')
    pyplot.title('Переходная финкция')
    pyplot.show()
transforfunction()

# wpopen =matlab.tf([80, 420, 190], [0.8, 4.2, 1, 0])

def nyquist():
    # wpopen = w1p*w2p*w3p*w4p
    print('Передаточная функция размкнутой:', wpopen)
    [re, im, w] = matlab.nyquist(wpopen)
    y = numpy.sqrt(1-re**2)
    pyplot.plot(re, y)
    pyplot.plot(re, -y)
    pyplot.plot(re, im, 'red')
    pyplot.xlabel('w')
    pyplot.ylabel('jw')
    pyplot.title('Годограф Найквиста')
    pyplot.show()
    w, mag, phase = matlab.bode(wpopen)
    # pyplot.figure(figsize=(10, 6))
    # ax1 = pyplot.subplot(1, 2, 1)
    # pyplot.semilogx(w, mag)
    # ax2 = pyplot.subplot(1, 2, 2)
    # pyplot.semilogx(w, phase)
    pyplot.show()
nyquist()

def margin():
    userinput1 = input(color.Fore.BLUE + 'Введете координата пересечения годографа Найквиста с осью Im:')
    userinput2 = input(color.Fore.BLUE + 'Введете продольную координату пересечения годографа Найквиста с кругом:')
    userinput3 = input(color.Fore.BLUE + 'Введете поперечную координату пересечения годографа Найквиста с кругом:')
    gm = 20*numpy.log(-1/float(userinput1))
    phase = numpy.arctan(float(userinput3)/float(userinput2))
    print('Запас устойчивости по ампультуде:', gm)
    print('Запас устойчивости по фазе:', numpy.rad2deg(phase))
margin()

def mixaibofu():
    xishu = list(wpclose.den[0][0])
    long = len(xishu)
    for i in range(0, long):
        xishu[i] = numpy.power(1j, long-1-i)*xishu[i]
        # print(xishu[i])
    m = xishu
    m = tuple(m)
    Re = list()
    Im = list()
    for w in range(0, 100):
        n = 0
        for i in range(0, long):
            xishu[i] = w**(long-1-i)*m[i]
            # print(xishu[i])
        for i in range(0, long):
            n = xishu[i] + n
        Re.append(n.real)
        Im.append(n.imag)
    pyplot.plot(Re, Im)
    pyplot.grid(True)
    pyplot.plot(Re, Im, 'red')
    pyplot.xlabel('Re')
    pyplot.ylabel('Im')
    pyplot.title('Годограф Михайпова')
    pyplot.show()
mixaibofu()

def linjiezhi():
    # wpclose = matlab.tf([63], [9216, 12290, 6784, 3798, 1534, 292.6, 19.9])
    xishu = list(wpclose.den[0][0])
    long = int(len(wpclose.den[0][0]))
    xishu_mw = xishu[long-1]
    if long % 2 == 0:
        b = int(long/2)
    if long % 2 == 1:
        b = int((long+1)/2)
    # print(m)
    # print(long)
    for Koc in range(460, 480):
        m = [[0] * (b + 1)] * long
        k = b
        xishu[long-1] = xishu_mw*(Koc/1000)
        xishu1 = tuple(xishu)
        p = []
        q = []
        if long % 2 == 0:
            for y in range(0, b):
                p.append(xishu1[2 * y])
                q.append(xishu1[2 * y + 1])
            for y in range(b, b + 1):
                p.append(0)
                q.append(0)
        if long % 2 == 1:
            for y in range(0, b):
                p.append(xishu1[2 * y])
            for y in range(0, b-1):
                q.append(xishu1[2 * y + 1])
            for y in range(b, b + 1):
                p.append(0)
            for y in range(b-1, b+1):
                q.append(0)
        m[0] = p
        m[1] = q
        # print(m)
        for x in range(2, long):
            h = []
            k = k-1
            if k >= 0:
                r = float((m[x - 2][0]) / (m[x - 1][0]))
                for y in range(0, k+1):
                    h.append(m[x - 2][y + 1] - r * m[x - 1][y + 1])
                m[x] = h
                if abs(m[x][0]-0) <= 0.001:
                    print(color.Fore.YELLOW, m, 19.9 * Koc/63000-1/63)
                    print(color.Fore.GREEN, 'Предельное значение Koc:', 19.9 * Koc/63000-1/63)  # 这里的0.3是初始的Koc，不同条件下需要改
        print(color.Fore.BLUE, m, 19.9 * Koc/63000-1/63)
                    # print('Предельное значение Koc:', 0.3 * Koc / 1000)  # 这里的0.3是初始的Koc，不同条件下需要改
linjiezhi()










