import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform


def corr_clust(data, dendrogram=False, threshold=0.8):
    '''Correlation Heatmaps with Hierarchical Clustering
    '''
    # https://www.kaggle.com/sgalella/correlation-heatmaps-with-hierarchical-clustering
    dissimilarity = 1 - abs(data.corr())
    Z = linkage(squareform(dissimilarity), 'complete')

    if dendrogram:
        return Z

    else:
        # the cluster
        labels = fcluster(Z, threshold, criterion='distance')

        # Keep the indices to sort labels
        labels_order = np.argsort(labels)

        # Build a new dataframe with the sorted columns
        for idx, i in enumerate(data.columns[labels_order]):
            if idx == 0:
                clustered = pd.DataFrame(data[i])
            else:
                df_to_append = pd.DataFrame(data[i])
                clustered = pd.concat([clustered, df_to_append], axis=1)

        correlations = clustered.corr()

        return correlations


def plot_corr(data, ax, vmin=None, vmax=None):
    # Compute the correlation matrix
    corr = corr_clust(data)
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        round(corr, 2), mask=mask, cmap=cmap, vmin=vmin, vmax=vmax, center=0,
        square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax
    )


#     def plot_corr(df,title,vmin=None,vmax=None,sub=111):
#     fig = plt.figure()
#     ax = fig.add_subplot(sub)

#     alpha = df.columns.values
#     cax = ax.matshow(df.corr()) #, interpolation='nearest')
#     fig.colorbar(cax)
#     cax.set_clim(vmin,vmax)

#     xaxis = np.arange(len(alpha))
#     ax.set_xticks(xaxis)
#     ax.set_yticks(xaxis)
#     ax.set_xticklabels(alpha, rotation=45)
#     ax.set_yticklabels(alpha, rotation=45)
#     ax.set_title(title, fontsize=15)


#     plt.show()
