import matplotlib.pyplot as plt

# Assume y_values is a list containing results from 6 experimental groups
# 假设y_values是包含6组实验结果的列表
y_values = [83.88, 83.25, 83.75, 82.50, 80.25, 85.25]

# Find the maximum value on the y-axis
# 找到纵坐标的最大值
max_y_value = max(y_values)
plt.rcParams['font.family'] = 'Times New Roman'    

# Create the figure and axes
# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(5, 5.5))  # Set the figure size to 8x6 inches
# Define colors in the style of academic papers
# 定义学术论文风格的颜色
colors = ['#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#ff7f0e']
# Set the width of the bars
# 设置柱子的宽度
width = 0.5
# Draw the bar chart
# 绘制柱状图
x_labels = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5", "Group 6"]
x_pos = range(len(x_labels))
ax.bar(x_pos, y_values, color=colors, width=width, align='center')

# Add text annotations of accuracy values on top of each bar
# 在每个柱子的顶部添加准确度值的文本注释
for i, v in enumerate(y_values):
    ax.text(i, v, f"{v:.2f}%", ha='center', va='bottom', fontsize=16)#, fontweight='bold')

# Set the x-axis labels
# 设置横轴标签
ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, fontsize=16)#, fontweight='bold')

# Set the y-axis label and title
# 设置纵轴标签和标题
ax.set_ylabel("Accuracy (%)", fontsize=18, fontweight='bold')
ax.set_xlabel("Experiment Group", fontsize=18, fontweight='bold')
# ax.set_title("Experimental Results", fontsize=18, fontweight='bold')
# Set the y-axis range from 80 to 90
# 设置纵轴范围为80到90
plt.ylim(80, 88)
# Adjust the position of x-axis labels to be closer to the x-axis, move down by 0.02
# 调整x轴标签的位置，使其离x轴更近，向下移动0.02
ax.xaxis.set_label_coords(0.5, -0.3)
# Set the margin of the figure
# 设置图形的边距
plt.subplots_adjust(bottom=0)  # Adjust the bottom margin
# Set the x-axis label angle to 45 degrees to prevent overlap
# 设置横轴标签显示角度为45度，防止重叠
plt.xticks(rotation=60)
# Show the legend and save the figure
# 显示图例和保存图形
# plt.legend(["Accuracy"])
plt.tight_layout()
plt.savefig(r'Output\BarChart.png', dpi=600, bbox_inches='tight')
plt.show()
