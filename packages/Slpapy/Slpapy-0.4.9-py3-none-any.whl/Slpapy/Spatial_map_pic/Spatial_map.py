from typing import Optional
import anndata as ad
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import seaborn as sns

from .scatterplots import embedding, Spatial_class


def Spatial_map(adata, cls):
    cls = str(cls)
    embedding(adata, basis='X_spacial', color=f'{cls}', frameon=False, save=f'_spacial_{cls}.png')


def Spatial_class_location(
        adata: ad.AnnData,
        cls: str,  # TIC和XY文件路径
        *,
        n: str = None,  # 不同的类别
) -> Optional[ad.AnnData]:
    cls = str(cls)
    if n is None:
        for i in adata.obs[cls].values.categories.values:
            Spatial_class(adata, cls, i)

    else:
        Spatial_class(adata, cls, n)


def significant_feature_pic(
        adata: ad.AnnData,
        names: str = None,
        n_genes: int = 5,
):
    result = adata.uns['rank_genes_groups']

    if names == None:
        # 结束本函数
        return print("Please input the name of the cluster")
    if names not in result['names'].dtype.names:
        return print("Please input the right name of the cluster")

    result = adata.uns['rank_genes_groups']
    res = pd.DataFrame({key: result[key][names] for key in
                        ['names', 'pvals', 'logfoldchanges', 'pvals_adj', 'scores']})
    # 查找res中scores最大的前n_genes个基因的名字形成列表
    res = res.sort_values(by='scores', ascending=False)
    res = res.iloc[:n_genes, :]
    # 在adata.var['m/z']中查找res中的基因名字对应的m/z值
    res['m/z'] = [adata.var.loc[i, 'm/z'] for i in res['names']]
    for i in res.index:
        embedding(adata, basis='X_spacial', color=f"{res.loc[i, 'names']}",title=None,
                  frameon=False, save=f"{res.loc[i, 'm/z']}_{res.loc[i, 'names']}.png")
    return


def Correlation_map(
        adata: ad.AnnData,
        *,
        threshold: int = 0,
        segmentation_threshold: int = 0.8,  # 不同的类别
) -> Optional[ad.AnnData]:
    corr_matrix = np.corrcoef(adata.X.T)
    threshold = threshold
    corr_matrix[corr_matrix < threshold] = 0
    C = pd.DataFrame(corr_matrix, columns=adata.var_names, index=adata.var_names)
    plt.figure(figsize=(10, 10), )
    cluster_map = sns.clustermap(C, cmap="viridis", xticklabels=0, yticklabels=0, )
    plt.title("Coexpression heat map")
    plt.savefig(".\\figures\clustermap_highres.png", dpi=700)
    plt.close()

    plt.figure(figsize=(25, 5), )
    dendrogram_row_linkage = cluster_map.dendrogram_row.linkage

    color_threshold = max(dendrogram_row_linkage[:, 2]) * segmentation_threshold
    dendrogram = sch.dendrogram(dendrogram_row_linkage, labels=C.index,
                                color_threshold=color_threshold)  # 0.62
    plt.title('Dendrogram Tree')
    plt.xticks(fontsize=2, )  # 根据需要调整字体大小和旋转角度rotation=45轴
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.tight_layout()
    plt.savefig(".\\figures\clustermap_Data Heatmap1.png", dpi=700)
    plt.close()
    classification_result = sch.fcluster(dendrogram_row_linkage,
                                         color_threshold, criterion='distance')
    adata.var['class'] = classification_result
    return adata
