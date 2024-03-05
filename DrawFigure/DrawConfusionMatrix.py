import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score
import itertools

#***************Plot Multiple Confusion Matrices****************
# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming confusion_matrices is a list containing 4 confusion matrices
# 假设confusion_matrices是一个包含4个混淆矩阵的列表
confusion_matrices = [
    np.array([[143, 4, 7, 0, 6],  # Confusion Matrix 1 混淆矩阵1
              [7, 112, 29, 4, 8],
              [2, 7, 144, 0, 7],
              [0, 4, 3, 135, 18],
              [18, 7, 4, 7, 124]]), 
    
    np.array([[150, 2, 6, 0, 2],  # Confusion Matrix 2 混淆矩阵2
              [11, 98, 37, 7, 7],
              [0, 2, 151, 0, 7],
              [0, 3, 1, 132, 24],
              [1, 2, 1, 5, 151]]),

    np.array([[152, 3, 4, 0, 1],  # Confusion Matrix 3 混淆矩阵3
              [13, 118, 19, 5, 5],
              [12, 11, 133, 0, 4],
              [0, 6, 1, 132, 21],
              [2, 2, 1, 3, 152]]),   
     
    np.array([[151, 3, 4, 0, 2],  # Confusion Matrix 4 混淆矩阵4
              [3, 96, 49, 7, 5],
              [2, 5, 149, 0, 4],
              [0, 8, 1, 143, 8],
              [2, 9, 0, 12, 137]]), 
]

# Set the figure size
# 设置图形大小
plt.figure(figsize=(12, 10))

# Set the font
# 设置字体
plt.rcParams['font.family'] = 'Times New Roman'    

# Loop through the list of confusion matrices and plot heatmaps one by one
# 遍历混淆矩阵列表，逐个绘制热力图
for i, matrix in enumerate(confusion_matrices):
    plt.subplot(2, 2, i+1)  # Create a 2x2 subplot, currently plotting the ith+1 subplot
    sns.heatmap(matrix, annot=True, fmt='d', annot_kws={"fontsize": 16},cmap='Blues', cbar=True)  
    # if i == len(confusion_matrices) - 1:
    #     plt.subplot(2, 2, i+1)  # Create a 2x2 subplot, currently plotting the ith+1 subplot
    #     sns.heatmap(matrix, annot=True, fmt='d', annot_kws={"fontsize": 14},cmap='Blues', cbar=True)  # Display color bar for the last subplot
    # else:
    #     plt.subplot(2, 2, i+1)  # Create a 2x2 subplot, currently plotting the ith+1 subplot
    #     sns.heatmap(matrix, annot=True, fmt='d', annot_kws={"fontsize": 14},cmap='Blues', cbar=False)  # Hide color bar for other subplots

    # Set the axis labels for the subplot
    # 设置子图的坐标轴标签
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')

    # Set the title for the subplot
    # 设置子图的标题
    if i==0:
        plt.title(f'RF', fontsize=14, fontweight='bold')
    elif i==1:
        plt.title(f'GoogLeNet', fontsize=14, fontweight='bold')
    elif i==2:
        plt.title(f'GCNN', fontsize=14, fontweight='bold')
    elif i==3:
        plt.title(f'Proposed method', fontsize=14, fontweight='bold')   
plt.tight_layout()
plt.savefig(r'Output\Confusion matrices.png',dpi=600, bbox_inches='tight')
plt.show()


# ##*************Plot Multiple Confusion Matrices with Bar Chart*********************************
# # Import necessary libraries
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Assuming confusion_matrices is a list containing 5 confusion matrices
# # 假设confusion_matrices是一个包含5个混淆矩阵的列表
# confusion_matrices = [
#     np.array([[143, 4, 7, 0, 6],  # Confusion Matrix 1 混淆矩阵1
#               [7, 112, 29, 4, 8],
#               [2, 7, 144, 0, 7],
#               [0, 4, 3, 135, 18],
#               [18, 7, 4, 7, 124]]), 
    
#     np.array([[150, 2, 6, 0, 2],  # Confusion Matrix 2 混淆矩阵2
#               [11, 98, 37, 7, 7],
#               [0, 2, 151, 0, 7],
#               [0, 3, 1, 132, 24],
#               [1, 2, 1, 5, 151]]),

#     np.array([[152, 3, 4, 0, 1],  # Confusion Matrix 3 混淆矩阵3
#               [13, 118, 19, 5, 5],
#               [12, 11, 133, 0, 4],
#               [0, 6, 1, 132, 21],
#               [2, 2, 1, 3, 152]]),   
     
#     np.array([[151, 3, 4, 0, 2],  # Confusion Matrix 4 混淆矩阵4
#               [3, 96, 49, 7, 5],
#               [2, 5, 149, 0, 4],
#               [0, 8, 1, 143, 8],
#               [2, 9, 0, 12, 137]]), 
       
#     np.array([[139, 4, 14, 0, 3],  # Confusion Matrix 5 混淆矩阵5
#               [10, 117, 24, 3, 6],
#               [1, 3, 150, 0, 6],
#               [0, 1, 2, 140, 17],
#               [12, 2, 0, 6, 140]]),    
# ]

# # Assuming y_values is a list containing accuracy values for 6 experiment groups
# # 假设y_values是包含6组实验结果的准确度值列表
# y_values = [85.88, 85.25, 85.75, 82.25, 84.50, 87.25]
# # Set the figure size
# # 设置图形大小
# plt.figure(figsize=(16, 10))

# # Set the font
# # 设置字体
# plt.rcParams['font.family'] = 'Times New Roman'    

# # Plot the bar chart
# # 绘制柱状图
# plt.subplot(2, 3, 1)  # Create a 2x3 subplot and plot the first subplot
# x_labels = ["1", "2", "3", "4", "5","6"]
# x_pos = range(len(x_labels))
# # Set colors, where dark blue indicates high accuracy, and light green indicates low accuracy
# # 设置颜色，深蓝色表示高准确度，浅绿色表示低准确度
# colors = ['#b0e2aa', '#b0e2aa', '#b0e2aa', '#b0e2aa', '#b0e2aa', '#2ca25f']
# width = 0.4
# # Plot the bar chart
# # 绘制柱状图
# plt.bar(x_pos, y_values, color=colors, width=width)
# for i, v in enumerate(y_values):
#     # Add text annotations for accuracy values on top of each bar
#     # 在每个柱子的顶部添加准确度值的文本注释
#     plt.text(i, v, f"{v:.2f}%", ha='center', va='bottom', fontsize=16)
# plt.xticks(x_pos, x_labels, fontsize=18, rotation=45, fontweight='bold')
# plt.ylabel("Accuracy (%)", fontsize=20, fontweight='bold')
# plt.xlabel("(a) Experiment Group", fontsize=20, fontweight='bold', labelpad=-10)
# plt.ylim(80, 88)
# plt.yticks(fontsize=16, fontweight='bold')

# # Plot the confusion matrices
# # 绘制混淆矩阵
# x_labels = ["Predicted Label", "Predicted Label", "Predicted Label", "Predicted Label", "Predicted Label"]
# # Loop through and plot multiple confusion matrices
# # 循环绘制多个混淆矩阵
# for i, matrix in enumerate(confusion_matrices):
#     plt.subplot(2, 3, i+2)  # Create a 2x3 subplot and plot the i+2th subplot
#     classes = [0, 1, 2, 3, 4]
#     cbar_kws = {"fontsize": 16}  if i == len(confusion_matrices) - 1 else {}  # Set the color bar annotation font size
#     # Use the Greens color map and plot the confusion matrix heatmap
#     # 使用Greens颜色映射，绘制混淆矩阵热力图
#     sns.heatmap(matrix, annot=True, fmt='d', cmap='Greens', cbar=i == len(confusion_matrices) - 1,
#                 linewidths=2, annot_kws={"fontsize": 16}, xticklabels=classes, yticklabels=classes, edgecolor='black')
#     # Get the current Axes object
#     ax = plt.gca()
#     # Set the internal cell borders to white
#     # 绘制内部单元格的边框为白色
#     for _, spine in ax.spines.items():
#         spine.set_visible(True)  # Show the borders around the plot
#         spine.set_edgecolor('black')  # Set the border color to black
#     plt.xlabel('Predicted Label', fontsize=20, fontweight='bold')
#     plt.ylabel('Real Label', fontsize=20, fontweight='bold')
#     plt.xlabel(x_labels[i], fontsize=20, fontweight='bold')
#     plt.xticks(fontsize=16, fontweight='bold')  # Set the x-axis category label font size
#     plt.yticks(fontsize=16, fontweight='bold')  # Set the y-axis category label font size    

# # Adjust the horizontal and vertical spacing between subgraphs
# # 调整子图之间的水平和垂直间距
# plt.tight_layout()
# # Save the figure and display
# # 保存图形并显示
# plt.savefig(r'Output\Confusion matrices and Bar Chart.png', dpi=600, bbox_inches='tight')
# plt.show()
