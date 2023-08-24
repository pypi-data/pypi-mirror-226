"""read counts-level plotting functions
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from utils import checkOptions, cleanAxes, almost_black, dark2, yellow_blue


def countsHistogram(data, condition=None, replicate=None, figureScale=1):
    if not checkOptions(data, 'counts', (condition, replicate)):
        return

    fig, axis = plt.subplots(figsize=(3.5 * figureScale, 2.5 * figureScale))
    cleanAxes(axis)

    axis.semilogy()

    logCounts = np.log2(data['counts'].loc[:, (condition, replicate)].fillna(0) + 1)

    axis.hist(logCounts,
              bins=int(len(data['counts']) ** .3),
              histtype='step', color=almost_black, lw=1)

    ymax = axis.get_ylim()[1]
    axis.plot([np.median(logCounts)] * 2, (0.8, ymax), color='#BFBFBF', lw=.5, alpha=.5)
    axis.text(np.median(logCounts) * .98, ymax * .90,
              'median reads = {0:.0f}'.format(np.median(data['counts'].loc[:, (condition, replicate)].fillna(0))),
              horizontalalignment='right', verticalalignment='top', fontsize=6)

    axis.set_ylim((0.9, ymax))

    axis.set_xlabel('{0} {1} sgRNA read counts (log2)'.format(condition, replicate))
    axis.set_ylabel('Number of sgRNAs')

    plt.tight_layout()
    # return displayFigure(fig, 'counts_hist')
    return fig


def countsScatter(data, condition_x=None, replicate_x=None,
                  condition_y=None, replicate_y=None,
                  showAll=True, showNegatives=True, showGenes=[],
                  colorByPhenotype_condition=None, colorByPhenotype_replicate=None,
                  figureScale=1):
    if not checkOptions(data, 'counts', (condition_x, replicate_x)):
        return
    if not checkOptions(data, 'counts', (condition_y, replicate_y)):
        return
    if colorByPhenotype_condition != None and colorByPhenotype_replicate != None \
            and not checkOptions(data, 'phenotypes', (colorByPhenotype_condition, colorByPhenotype_replicate)):
        return

    fig, axis = plt.subplots(figsize=(3 * figureScale, 3 * figureScale))
    cleanAxes(axis)

    if showAll:
        if colorByPhenotype_condition == None or colorByPhenotype_replicate == None:
            axis.scatter(np.log2(data['counts'].loc[:, (condition_x, replicate_x)] + 1),
                         np.log2(data['counts'].loc[:, (condition_y, replicate_y)] + 1),
                         s=1.5, c=almost_black, label='all sgRNAs',
                         rasterized=True)
        else:
            result = axis.scatter(np.log2(data['counts'].loc[:, (condition_x, replicate_x)] + 1),
                                  np.log2(data['counts'].loc[:, (condition_y, replicate_y)] + 1),
                                  s=1.5,
                                  c=data['phenotypes'].loc[:, (colorByPhenotype_condition, colorByPhenotype_replicate)],
                                  cmap=yellow_blue, label='all sgRNAs',
                                  rasterized=True)

            plt.colorbar(result)

    if showNegatives:
        axis.scatter(
            np.log2(data['counts'].loc[data['library']['gene'] == 'negative_control', (condition_x, replicate_x)] + 1),
            np.log2(data['counts'].loc[data['library']['gene'] == 'negative_control', (condition_y, replicate_y)] + 1),
            s=1.5, c='#BFBFBF', label='non-targeting sgRNAs',
            rasterized=True)

    if showGenes and len(showGenes) != 0:
        if isinstance(showGenes, str):
            showGenes = [showGenes]

        geneSet = set(data['library']['gene'])
        for i, gene in enumerate(showGenes):
            if gene not in geneSet:
                print('{0} not in dataset'.format(gene))
            else:
                axis.scatter(
                    np.log2(data['counts'].loc[data['library']['gene'] == gene, (condition_x, replicate_x)] + 1),
                    np.log2(data['counts'].loc[data['library']['gene'] == gene, (condition_y, replicate_y)] + 1),
                    s=3, c=dark2[i], label=gene)

    plt.legend(loc='best', fontsize=6, handletextpad=0.005)

    axis.set_xlim((-0.2, max(axis.get_xlim()[1], axis.get_ylim()[1])))
    axis.set_ylim((-0.2, max(axis.get_xlim()[1], axis.get_ylim()[1])))

    axis.set_xlabel('{0} {1} sgRNA read counts (log2)'.format(condition_x, replicate_x), fontsize=8)
    axis.set_ylabel('{0} {1} sgRNA read counts (log2)'.format(condition_y, replicate_y), fontsize=8)

    plt.tight_layout()
    # return displayFigure(fig, 'counts_scatter')
    return fig


def premergedCountsScatterMatrix(data, condition=None, replicate=None):
    if not checkOptions(data, 'counts', (condition, replicate)):
        return

    if 'premerged counts' not in data:
        print('Data must be loaded with premergedCounts = True')
        return

    dataTable = data['premerged counts'].loc[:, (condition, replicate)]
    dataColumns = dataTable.columns
    if len(dataColumns) == 1:
        print('Only one counts file for {0}, {1}; no scatter matrix will be generated'.format(condition, replicate))
        return

    fig, axes = plt.subplots(
        len(dataColumns), len(dataColumns),
        figsize=(len(dataColumns) * 2.5, len(dataColumns) * 2.5)
    )

    for i, (name1, col1) in enumerate(dataTable.iteritems()):
        name1 = '{0:.30}'.format(os.path.split(name1)[-1])
        for j, (name2, col2) in enumerate(dataTable.iteritems()):
            name2 = '{0:.30}'.format(os.path.split(name2)[-1])
            if i < j:
                cleanAxes(axes[i, j], top=False, bottom=False, left=False, right=False)
                axes[i, j].xaxis.set_tick_params(top=False, bottom=False, labelbottom=False)
                axes[i, j].yaxis.set_tick_params(left=False, right=False, labelleft=False)

            elif i == j:
                axes[i, j].hist(np.log2(col2.dropna() + 1), bins=int(len(col2) ** .3), histtype='step',
                                color=almost_black, lw=1)

                axes[i, j].set_xlabel(name2, fontsize=6)
                axes[i, j].set_ylabel('# sgRNAs', fontsize=6)

                axes[i, j].xaxis.set_tick_params(labelsize=6)
                axes[i, j].yaxis.set_tick_params(labelsize=6)
            else:
                axes[i, j].scatter(np.log2(col2.dropna() + 1), np.log2(col1.dropna() + 1), s=2, c=almost_black,
                                   rasterized=True)

                axes[i, j].set_xlabel(name2, fontsize=6)
                axes[i, j].set_ylabel(name1, fontsize=6)

                axes[i, j].xaxis.set_tick_params(labelsize=6)
                axes[i, j].yaxis.set_tick_params(labelsize=6)

    plt.tight_layout(pad=.05)
    # return displayFigure(fig, 'premerged_counts_scatter')
    return fig
