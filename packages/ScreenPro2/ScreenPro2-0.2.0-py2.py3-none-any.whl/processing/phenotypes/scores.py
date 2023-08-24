"""
filter by read counts, generate phenotype scores, average replicates
"""

from scipy import stats

from processing.load import *


def averageBestN(group, numToAverage):
    return group.apply(lambda column: np.mean(sorted(column.dropna(), key=abs, reverse=True)[:numToAverage]) if len(
        column.dropna()) > 0 else np.nan)


def getBestTranscript(group):
    """set the index to be transcripts and then get the index with the lowest p-value for each cell
    """
    return group.set_index('transcripts').drop(('gene', ''), axis=1).idxmin()


def scoreGeneByBestTranscript(geneTable):
    """score genes by best m-w p-value
    given a gene table indexed by both gene and transcript, score genes by the best m-w p-value per phenotype/replicate
    """
    geneTableTransGroups = geneTable.reorder_levels([2, 0, 1], axis=1)['Mann-Whitney p-value'].reset_index().groupby(
        'gene')

    bestTranscriptFrame = geneTableTransGroups.apply(getBestTranscript)

    tupList = []
    bestTransList = []
    for tup, group in geneTable.groupby(level=list(range(2)), axis=1):
        tupList.append(tup)
        curFrame = geneTable.loc[zip(bestTranscriptFrame.index, bestTranscriptFrame[tup]), tup]
        bestTransList.append(curFrame.reset_index().set_index('gene'))

    return pd.concat(bestTransList, axis=1, keys=tupList, sort=True)


def calcLog2e(row, countsRatio, growthValue, wtLog2E):
    return (np.log2(countsRatio * row[1] / row[0]) - wtLog2E) / growthValue


def applyMW(group, negativeTable):
    out = group.apply(lambda column: stats.mannwhitneyu(
        column.dropna().values, negativeTable[column.name].dropna().values,
        alternative='two-sided')[1] if len(column.dropna()) > 0 else np.nan)

    return out


def filterCountsPerExperiment(min_reads, exptsTable, libraryTable):
    """filter out reads if /all/ reads for an expt across replicates/conditions < min_reads
    """
    experimentGroups = []

    exptTuples = exptsTable.columns

    exptSet = set([tup[0] for tup in exptTuples])
    for expt in exptSet:
        exptDf = exptsTable[[tup for tup in exptTuples if tup[0] == expt]]
        exptDfUnderMin = (exptDf < min_reads).all(axis=1)
        exptDfFiltered = exptDf.align(exptDfUnderMin[exptDfUnderMin == False], axis=0, join='right')[0]
        experimentGroups.append(exptDfFiltered)

        print(expt, len(exptDfUnderMin[exptDfUnderMin == True]))

    resultTable = pd.concat(experimentGroups, axis=1, sort=True).align(libraryTable, axis=0)[0]

    return resultTable


def filterLowCounts(countsColumns, filterType, filterThreshold):
    """more flexible read filtering
    keep row if either both/all columns are above threshold, or if either/any column is
    in other words, mask if any column is below threshold or only if all columns are below
    """
    if filterType == 'both' or filterType == 'all':
        failFilterColumn = countsColumns.apply(lambda row: min(row) < filterThreshold, axis=1)
    elif filterType == 'either' or filterType == 'any':
        failFilterColumn = countsColumns.apply(lambda row: max(row) < filterThreshold, axis=1)
    else:
        raise ValueError('filter type not recognized or not implemented')

    resultTable = countsColumns.copy()
    resultTable.loc[failFilterColumn, :] = np.nan

    return resultTable


def computePhenotypeScore(counts1, counts2, libraryTable, growthValue, pseudocountBehavior, pseudocountValue,
                          normToNegs=True):
    """compute phenotype scores for any given comparison of two conditions
    """
    combinedCounts = pd.concat([counts1, counts2], axis=1, sort=True)

    # pseudocount
    if pseudocountBehavior == 'default' or pseudocountBehavior == 'zeros only':
        defaultBehavior = lambda row: row if min(row) != 0 else row + pseudocountValue
        combinedCountsPseudo = combinedCounts.apply(defaultBehavior, axis=1)
    elif pseudocountBehavior == 'all values':
        combinedCountsPseudo = combinedCounts.apply(lambda row: row + pseudocountValue, axis=1)
    elif pseudocountBehavior == 'filter out':
        combinedCountsPseudo = combinedCounts.copy()
        zeroRows = combinedCounts.apply(lambda row: min(row) <= 0, axis=1)
        combinedCountsPseudo.loc[zeroRows, :] = np.nan
    else:
        raise ValueError('Pseudocount behavior not recognized or not implemented')

    totalCounts = combinedCountsPseudo.sum()
    countsRatio = float(totalCounts[0]) / totalCounts[1]

    # compute neg control log2 enrichment
    if normToNegs == True:
        negCounts = \
        combinedCountsPseudo.align(libraryTable[libraryTable['gene'] == 'negative_control'], axis=0, join='inner')[0]
        # print negCounts
    else:
        negCounts = combinedCountsPseudo
    neglog2e = negCounts.apply(calcLog2e, countsRatio=countsRatio, growthValue=1, wtLog2E=0, axis=1).median()
    # print neglog2e

    # compute phenotype scores
    scores = combinedCountsPseudo.apply(calcLog2e, countsRatio=countsRatio, growthValue=growthValue, wtLog2E=neglog2e,
                                        axis=1)

    return scores


def averagePhenotypeScores(scoreTable):
    """average replicate phenotype scores
    """
    exptTuples = scoreTable.columns
    exptsToReplicates = dict()
    for tup in exptTuples:
        if (tup[0], tup[1]) not in exptsToReplicates:
            exptsToReplicates[(tup[0], tup[1])] = set()
        exptsToReplicates[(tup[0], tup[1])].add(tup[2])

    averagedColumns = []
    labels = []
    for expt in exptsToReplicates:
        exptDf = scoreTable[[(expt[0], expt[1], rep_id) for rep_id in exptsToReplicates[expt]]]
        averagedColumns.append(exptDf.mean(axis=1))
        labels.append((expt[0], expt[1], 'ave_' + '_'.join(exptsToReplicates[expt])))

    resultTable = pd.concat(averagedColumns, axis=1, keys=labels, sort=True).align(scoreTable, axis=0)[0]
    resultTable.columns = pd.MultiIndex.from_tuples(labels)

    return resultTable


def applyGeneScore(groupedPhenotypeTable, negativeTable, analysis, analysisParamList):
    """apply gene scoring functions to pre-grouped tables of phenotypes
    """
    if analysis == 'calculate_ave':
        numToAverage = analysisParamList[0]
        if numToAverage <= 0:
            means = groupedPhenotypeTable.aggregate(np.mean)
            counts = groupedPhenotypeTable.count()
            result = pd.concat([means, counts], axis=1,
                               keys=['average of all phenotypes', 'average of all phenotypes_sgRNAcount'], sort=True)
        else:
            means = groupedPhenotypeTable.apply(lambda x: averageBestN(x, numToAverage))
            counts = groupedPhenotypeTable.count()
            result = pd.concat([means, counts], axis=1,
                               keys=['average phenotype of strongest %d' % numToAverage, 'sgRNA count_avg'], sort=True)
    elif analysis == 'calculate_mw':
        pvals = groupedPhenotypeTable.apply(lambda x: applyMW(x, negativeTable))
        counts = groupedPhenotypeTable.count()
        result = pd.concat([pvals, counts], axis=1, keys=['Mann-Whitney p-value', 'sgRNA count_MW'], sort=True)
    elif analysis == 'calculate_nth':
        nth = analysisParamList[0]
        pvals = groupedPhenotypeTable.aggregate(
            lambda x: sorted(x, key=abs, reverse=True)[nth - 1] if nth <= len(x) else np.nan)
        counts = groupedPhenotypeTable.count()
        result = pd.concat([pvals, counts], axis=1, keys=['%dth best score' % nth, 'sgRNA count_nth best'], sort=True)
    else:
        raise ValueError('Analysis %s not recognized or not implemented' % analysis)

    return result
