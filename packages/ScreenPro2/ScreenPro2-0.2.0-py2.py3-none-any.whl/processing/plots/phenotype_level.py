"""phenotype-level plotting functions
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from utils import checkOptions, cleanAxes, plotGrid, almost_black, dark2


def phenotypeHistogram(data, phenotype=None, replicate=None, figureScale=1):
    if not checkOptions(data, 'phenotypes', (phenotype, replicate)):
        return

    fig, axis = plt.subplots(figsize=(3.5 * figureScale, 2.5 * figureScale))
    cleanAxes(axis)

    axis.semilogy()

    axis.hist([data['phenotypes'].loc[:, (phenotype, replicate)].dropna(),
               data['phenotypes'].loc[data['library']['gene'] == 'negative_control', (phenotype, replicate)].dropna()],
              bins=int(len(data['phenotypes']) ** .3),
              histtype='step', color=[almost_black, '#BFBFBF'], label=['all sgRNAs', 'non-targeting sgRNAs'], lw=1)

    plt.legend(fontsize=6, loc='upper left')

    axis.set_ylim((0.9, axis.get_ylim()[1]))

    axis.set_xlabel('{0} {1} sgRNA phenotypes'.format(phenotype, replicate))
    axis.set_ylabel('Number of sgRNAs')

    plt.tight_layout()
    # return displayFigure(fig, 'phenotype_hist')
    return fig


def phenotypeScatter(data, phenotype_x=None, replicate_x=None,
                     phenotype_y=None, replicate_y=None,
                     showAll=True, showNegatives=True,
                     showGenes=[], showGeneSets={}, figureScale=1):
    if not checkOptions(data, 'phenotypes', (phenotype_x, replicate_x)):
        return
    if not checkOptions(data, 'phenotypes', (phenotype_y, replicate_y)):
        return

    fig, axis = plt.subplots(figsize=(3 * figureScale, 3 * figureScale))
    cleanAxes(axis)

    if showAll:
        axis.scatter(data['phenotypes'].loc[:, (phenotype_x, replicate_x)],
                     data['phenotypes'].loc[:, (phenotype_y, replicate_y)],
                     s=1.5, c=almost_black, label='all sgRNAs',
                     rasterized=True)

    if showNegatives:
        axis.scatter(data['phenotypes'].loc[data['library']['gene'] == 'negative_control', (phenotype_x, replicate_x)],
                     data['phenotypes'].loc[data['library']['gene'] == 'negative_control', (phenotype_y, replicate_y)],
                     s=1.5, c='#BFBFBF', label='non-targeting sgRNAs',
                     rasterized=True)

    i = 0
    if showGenes and len(showGenes) != 0:
        if isinstance(showGenes, str):
            showGenes = [showGenes]

        geneSet = set(data['library']['gene'])
        for i, gene in enumerate(showGenes):
            if gene not in geneSet:
                print('{0} not in dataset'.format(gene))
            else:
                axis.scatter(data['phenotypes'].loc[data['library']['gene'] == gene, (phenotype_x, replicate_x)],
                             data['phenotypes'].loc[data['library']['gene'] == gene, (phenotype_y, replicate_y)],
                             s=3, c=dark2[i], label=gene,
                             rasterized=True)

    if showGeneSets and len(showGeneSets) != 0:
        if not isinstance(showGeneSets, dict) or not \
                (isinstance(showGeneSets[showGeneSets.keys()[0]], set) or isinstance(
                    showGeneSets[showGeneSets.keys()[0]], list)):
            print('Gene sets must be a dictionary of {set_name: [gene list/set]} pairs')

        else:
            for j, gs in enumerate(showGeneSets):
                sgsTargetingSet = data['library']['gene'].apply(lambda gene: gene in showGeneSets[gs])
                axis.scatter(data['phenotypes'].loc[sgsTargetingSet, (phenotype_x, replicate_x)],
                             data['phenotypes'].loc[sgsTargetingSet, (phenotype_y, replicate_y)],
                             s=3, c=dark2[i + j], label=gs,
                             rasterized=True)

    plotGrid(axis)

    plt.legend(loc='best', fontsize=6, handletextpad=0.005)

    axis.set_xlabel('sgRNA {0} {1}'.format(phenotype_x, replicate_x), fontsize=8)
    axis.set_ylabel('sgRNA {0} {1}'.format(phenotype_y, replicate_y), fontsize=8)

    plt.tight_layout()
    # return displayFigure(fig, 'phenotype_scatter')
    return fig


def sgRNAsPassingFilterHist(data, phenotype, replicate, transcripts=False, figureScale=1):
    if not checkOptions(data, 'phenotypes', (phenotype, replicate)):
        return

    fig, axis = plt.subplots(figsize=(3.5 * figureScale, 2.5 * figureScale))
    cleanAxes(axis)

    axis.semilogy()

    if transcripts:
        sgRNAsPerGene = data['phenotypes'].loc[
            data['library']['gene'] != 'negative_control', (phenotype, replicate)].groupby(
            [data['library']['gene'], data['library']['transcripts']]).count()
    else:
        sgRNAsPerGene = data['phenotypes'].loc[
            data['library']['gene'] != 'negative_control', (phenotype, replicate)].groupby(
            data['library']['gene']).count()

    axis.hist(sgRNAsPerGene,
              bins=np.arange(min(sgRNAsPerGene), max(sgRNAsPerGene) + 1, 1),
              histtype='step', color=almost_black, lw=1)

    axis.set_ylim((0.9, axis.get_ylim()[1]))

    axis.set_xlabel(
        '{0} {1} sgRNAs passing filter per {2}'.format(phenotype, replicate, 'transcript' if transcripts else 'gene'))
    axis.set_ylabel('Number of sgRNAs')

    plt.tight_layout()
    # return displayFigure(fig, 'sgRNAs_passing_filter_hist')
    return fig
