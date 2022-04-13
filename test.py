
# import pylab
import matplotlib.pyplot as plt
# from matplotlib.pyplot import figure

import numpy as np
x = np.linspace(0, 20, 1000)  # 100 evenly-spaced values from 0 to 50
y = np.sin(x)
# figure(figsize=(800, 600), dpi=80)
print('aa')
plt.plot(x, y)
plt.show()