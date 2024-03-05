import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

def exp_moving_avg(x, decay=0.9):
    shadow = x[0]
    a = [shadow]
    for v in x[1:]:
        shadow -= (1 - decay) * (shadow - v)
        a.append(shadow)
    return a

# 读取Excel文件 (Read Excel file)
file_path = r'Input\Acc Loss.xls'  # Read Excel file
df = pd.read_excel(file_path)

# 获取指定列的数据 (Get data for specified columns)
train_accuracy = df['train_acc_lst']  # Get data for specified columns
val_accuracy = df['val_acc_lst']
train_loss = df['losses_train']
val_loss = df['losses_val']

# 设置全局字体为 Times New Roman (Set global font to Times New Roman)
plt.rcParams['font.family'] = 'Times New Roman'  # Set global font to Times New Roman

# 定义周期数 (Define epochs)
epochs = range(1, len(train_accuracy) + 1)  # Define epochs

# 绘制图像 (Plot the graph)
fig, ax1 = plt.subplots()

# 绘制训练和验证准确度曲线（左侧纵轴） (Plot training and validation accuracy curves (left y-axis))
ax1.plot(epochs, exp_moving_avg(train_accuracy, 0.8), 'b', label='Train Accuracy')
ax1.plot(epochs, exp_moving_avg(val_accuracy, 0.8), 'g', label='Validation Accuracy')
ax1.set_xlabel('Epoch', fontsize=14, fontweight='bold')  # 设置横坐标轴标签 (Set x-axis label)
ax1.set_ylabel('Accuracy', fontsize=14, fontweight='bold')  # 设置纵坐标轴标签 (Set y-axis label)
ax1.tick_params(labelsize=14)  # 设置刻度标签字体大小 (Set tick label font size)

# 创建第二个纵轴，用于绘制训练和验证损失值曲线（右侧纵轴） (Create a second y-axis for plotting training and validation loss curves (right y-axis))
ax2 = ax1.twinx()

ax2.plot(epochs, exp_moving_avg(train_loss, 0.8), 'r', label='Train Loss')  #, linestyle='dashed'
ax2.plot(epochs, exp_moving_avg(val_loss, 0.8), 'orange', label='Validation Loss')  #, linestyle='dashed'
ax2.set_ylabel('Loss', fontsize=14, fontweight='bold')  # 设置纵坐标轴标签 (Set y-axis label)
ax2.tick_params(labelsize=14)  # 设置刻度标签字体大小 (Set tick label font size)

# Combine the legends of the four curves and place them in the middle right
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines += lines2
labels += labels2
ax1.legend(lines, labels, loc='center right', fontsize=12)  #, prop={'weight': 'bold'})

# 设置横坐标轴范围为最小和最大横坐标值 (Set x-axis range to the minimum and maximum x-axis values)
plt.xlim(1, len(train_accuracy))

# 设置纵坐标轴范围 (Set y-axis range)
ax1.set_ylim(0, 1)
ax2.set_ylim(0, 2)

# 设置次刻度的间隔大小 (Set the interval size of minor ticks)
ax1.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.yaxis.set_minor_locator(MultipleLocator(0.02))

# 隐藏上边的框线 (Hide top frame lines)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

# 保存图像 (Save the figure)
plt.savefig(r'Output\Acc Loss.png', dpi=600, bbox_inches='tight')

plt.show()
print('------------')
