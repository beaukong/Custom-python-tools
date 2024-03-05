import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

legendLst = ['1', '2', '3', '4', '5']
n_classes = 5

# 读取不同模型的高维特征向量和标签 (Read high-dimensional feature vectors and labels of different models)
def load_features_and_labels(features_path, labels_path):
    features = np.loadtxt(features_path, delimiter=' ')
    labels = np.loadtxt(labels_path, delimiter=' ')
    return features, labels

filePath = r'Input\tSNE\Diffpool_HighDimVec.txt'
txt_ = np.loadtxt(filePath, delimiter=' ')
high_dim_features_diffpool = txt_[:, 2:]
labels_diffpool = txt_[:, 1:2]
high_dim_features_RF, ytest_RF = load_features_and_labels(
    r'Input\tSNE\RF_HighDimVec.txt',
    r'Input\tSNE\RF_Y.txt'
)

high_dim_features_GCNN, ytest_GCNN = load_features_and_labels(
    r'Input\tSNE\GCNN_HighDimVec.txt',
    r'Input\tSNE\GCNN_Y.txt'
)

high_dim_features_GoogLeNet, ytest_GoogLeNet = load_features_and_labels(
    r'Input\tSNE\GoogLeNet_HighDimVec.txt',
    r'Input\tSNE\GoogLeNet_Y.txt'
)

# 绘制单个子图 (Plot a single subplot)
def plot_single_tsne_subplot(features, labels, title, ax):
    tsne = TSNE(n_components=2, random_state=42)
    low_dim_features = tsne.fit_transform(features)
    class_indices = [np.where(labels == i)[0] for i in range(n_classes)]
    colors = plt.cm.rainbow(np.linspace(0, 1, len(class_indices)))

    for i, indices in enumerate(class_indices):
        ax.scatter(low_dim_features[indices, 0], low_dim_features[indices, 1], label=legendLst[i], color=colors[i])

    ax.set_title(title, fontsize=22, fontweight='bold')  # 设置子图标题字体大小 (Set the subplot title font size)
    ax.legend(fontsize=20, handletextpad=0, framealpha=0.9)  # 设置图例字体大小 (Set legend font size)
    ax.set_xlabel('t-SNE Dimension 1', fontsize=22, fontweight='bold')  # 设置横坐标轴标签字体大小 (Set x-axis label font size)
    ax.set_ylabel('t-SNE Dimension 2', fontsize=22, fontweight='bold')  # 设置纵坐标轴标签字体大小 (Set y-axis label font size)
    ax.tick_params(axis='both', which='both', labelsize=20)  # 设置刻度标签字体大小 (Set tick label font size)

# 绘制大图和子图 (Plot the main and subplots)
# 设置字体 (Set font)
plt.rcParams['font.family'] = 'Times New Roman'  
fig, axes = plt.subplots(2, 2, figsize=(15, 15))
plt.subplots_adjust(wspace=0.3, hspace=0.5)

plot_single_tsne_subplot(high_dim_features_diffpool, labels_diffpool, '(a) Proposed method', axes[0, 0])
plot_single_tsne_subplot(high_dim_features_RF, ytest_RF, '(b) RF', axes[0, 1])
plot_single_tsne_subplot(high_dim_features_GoogLeNet, ytest_GoogLeNet, '(c) GoogLeNet', axes[1, 0])
plot_single_tsne_subplot(high_dim_features_GCNN, ytest_GCNN, '(d) GCNN', axes[1, 1])

# 设置图例是否可见 (Set whether the legend is visible).
# for ax in axes.ravel():
#     ax.legend().set_visible(False)

plt.tight_layout()
plt.savefig(r'Output\tSNE_Subplots.png', dpi=600, bbox_inches='tight')
plt.show()
