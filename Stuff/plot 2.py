import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

fig, axs =plt.subplots(2,2)
axs[0,0].set_title("Heat Map")
sns.heatmap(np.transpose(heat_map), ax=axs[0,0], cbar=False, cmap='icefire', center=0).invert_yaxis()

axs[0,1].set_title("Position Map")
sns.scatterplot(x=self.position_state[:, 0], y=self.position_state[:, 1], data=self.position_state, ax=axs[0,1],hue=self.position_state[:, 2], legend=False, palette='coolwarm')

axs[1,0].set_title("line graph")
axs[1,0].plot()
