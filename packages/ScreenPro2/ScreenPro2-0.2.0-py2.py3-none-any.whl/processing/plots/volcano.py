"""volcano plot function
"""
import numpy as np
import matplotlib.pyplot as plt
from utils import checkOptions, cleanAxes, plotGrid, dark2


def volcanoPlot(data, phenotype=None, replicate=None, transcripts=False, showPseudo=True,
                effectSizeLabel=None, pvalueLabel=None, hitThreshold=7,
                labelHits=False, showGeneSets={}, labelGeneSets=True,
                figureScale=1
                ):
    """

    Parameters
    ----------
    data :

    phenotype :
         (Default value = None)
    replicate :
         (Default value = None)
    transcripts :
         (Default value = False)
    showPseudo :
         (Default value = True)
    effectSizeLabel :
         (Default value = None)
    pvalueLabel :
         (Default value = None)
    hitThreshold :
         (Default value = 7)
    labelHits :
         (Default value = False)
    showGeneSets :
         (Default value = {})
    labelGeneSets :
         (Default value = True)

    Returns
    -------

    """

    if not checkOptions(data, 'genes', (phenotype, replicate)):
        return

    if transcripts:
        table = data['transcript scores'][(phenotype, replicate)].copy()
        isPseudo = table.apply(lambda row: row.name[0][:6] == 'pseudo', axis=1)
    else:
        table = data['gene scores'][(phenotype, replicate)].copy()
        isPseudo = table.apply(lambda row: row.name[:6] == 'pseudo', axis=1)

    if effectSizeLabel == None:
        effectSizeLabel = getEffectSizeLabel(table)

        if effectSizeLabel == None:
            return

    if pvalueLabel == None:
        pvalueLabel = getPvalueLabel(table)

        if pvalueLabel == None:
            return

    discScore = lambda z, p: p * np.abs(z)

    pseudogeneScores = table[isPseudo]
    pseudoStd = np.std(pseudogeneScores[effectSizeLabel])
    table.loc[:, 'thresh'] = discScore(table[effectSizeLabel] / pseudoStd,
                                       -1 * np.log10(table[pvalueLabel])) >= hitThreshold

    yGenes = -1 * np.log10(table[pvalueLabel])
    xGenes = table[effectSizeLabel]

    fig, axis = plt.subplots(1, 1, figsize=(4 * figureScale, 3.5 * figureScale))
    cleanAxes(axis)

    axis.scatter(
        table.loc[isPseudo.ne(True)].loc[table['thresh'], effectSizeLabel],
        -1 * np.log10(table.loc[isPseudo.ne(True)].loc[table['thresh'], pvalueLabel].values),
        s=4,
        c='#7570b3',
        label='Gene hit',
        rasterized=True
    )

    axis.scatter(
        table.loc[isPseudo.ne(True)].loc[table['thresh'].ne(True), effectSizeLabel],
        -1 * np.log10(table.loc[isPseudo.ne(True)].loc[table['thresh'].ne(True), pvalueLabel].values),
        s=4,
        c='#999999',
        label='Gene non-hit',
        rasterized=True
    )

    if labelHits:
        for gene, row in table.loc[isPseudo.ne(True)].loc[table['thresh']].iterrows():
            if transcripts:
                gene = ', '.join(gene)

            axis.text(row[effectSizeLabel], -1 * np.log10(row[pvalueLabel]), gene, fontsize=6,
                      horizontalalignment='left' if row[effectSizeLabel] > 0 else 'right', verticalalignment='center')

    if showPseudo:
        axis.scatter(table.loc[isPseudo.ne(False)].loc[table['thresh'], effectSizeLabel],
                     -1 * np.log10(table.loc[isPseudo.ne(False)].loc[table['thresh'], pvalueLabel].values),
                     s=4,
                     c='#d95f02',
                     label='Negative control gene hit',
                     rasterized=True)

        axis.scatter(table.loc[isPseudo.ne(False)].loc[table['thresh'].ne(True), effectSizeLabel],
                     -1 * np.log10(table.loc[isPseudo.ne(False)].loc[table['thresh'].ne(True), pvalueLabel].values),
                     s=4,
                     c='#dadaeb',
                     label='Negative control gene',
                     rasterized=True)

    if showGeneSets and len(showGeneSets) != 0:
        if not isinstance(showGeneSets, dict) or not (
                isinstance(showGeneSets[showGeneSets.keys()[0]], set) or
                isinstance(showGeneSets[showGeneSets.keys()[0]], list)):
            print('Gene sets must be a dictionary of {set_name: [gene list/set]} pairs')

        else:
            for i, gs in enumerate(showGeneSets):
                sgsTargetingSet = data['library']['gene'].apply(lambda gene: gene in showGeneSets[gs])
                axis.scatter(table.loc[showGeneSets[gs], effectSizeLabel],
                             -1 * np.log10(table.loc[showGeneSets[gs], pvalueLabel]),
                             s=6, c=dark2[i], label=gs)

                if labelGeneSets:
                    for gene, row in table.loc[showGeneSets[gs]].iterrows():
                        if transcripts:
                            gene = ', '.join(gene)

                        axis.text(row[effectSizeLabel], -1 * np.log10(row[pvalueLabel]), gene, fontsize=6,
                                  horizontalalignment='left' if row[effectSizeLabel] > 0 else 'right',
                                  verticalalignment='center')

    plotGrid(axis, vert_origin=True, horiz_origin=False, unity=False)

    ymax = np.ceil(max(yGenes)) * 1.02
    xmin = min(xGenes) * 1.05
    xmax = max(xGenes) * 1.05

    axis.plot(np.linspace(xmin, xmax, 1000),
              np.abs(hitThreshold / np.linspace(xmin / pseudoStd, xmax / pseudoStd, 1000)), 'k--', lw=.5)

    axis.set_xlim((xmin, xmax))
    axis.set_ylim((0, ymax))

    axis.set_xlabel(
        '{3} {0} {1} ({2})'.format(phenotype, replicate, effectSizeLabel, 'gene' if not transcripts else 'transcript'),
        fontsize=8)
    axis.set_ylabel('-log10 {0}'.format(pvalueLabel, fontsize=8))

    plt.legend(loc='best', fontsize=6, handletextpad=0.005)
    plt.tight_layout()
    # return displayFigure(fig, 'volcano_plot')
    return fig


def getEffectSizeLabel(table):
    """

    Parameters
    ----------
    table :


    Returns
    -------

    """
    effectColLabels = [colname for colname, col in table.iteritems() if colname[:7] == 'average']

    if len(effectColLabels) == 0:
        print('No gene effect size data columns found')
        return None

    elif len(effectColLabels) > 1:
        print('Multiple effect size data columns found, please specifiy one: ' + ', '.join(effectColLabels))
        return None

    else:
        return effectColLabels[0]


def getPvalueLabel(table):
    """

    Parameters
    ----------
    table :


    Returns
    -------

    """
    pvalColLabels = [colname for colname, col in table.iteritems() if colname == 'Mann-Whitney p-value']

    if len(pvalColLabels) == 0:
        print('No p-value data columns found')
        return None

    elif len(pvalColLabels) > 1:
        effectColLabels = [colname for colname, col in table.iteritems() if colname[:7] == 'average']
        print('Multiple p-value data columns found, please specifiy one: ' + ', '.join(effectColLabels))
        return None

    else:
        return pvalColLabels[0]
