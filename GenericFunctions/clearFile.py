
x = open('D:\\Projects\\Python\\ResellScraperv2\\txt\\reebok_PID_not_available.txt', 'r').readlines()
print(len(x))
y = dict.fromkeys(x)
x = list(y)
print(len(x))
x_w = open('D:\\Projects\\Python\\ResellScraperv2\\txt\\reebok_PID_not_available.txt', 'w')
x_w.writelines(x)
x_w.close()