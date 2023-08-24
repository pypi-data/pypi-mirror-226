"""merge counts files into a data table, combine reads from multiple sequencing runs,
"""

import pandas as pd
import numpy as np


def readCountsFile(countsFileName):
    """return Series of counts from a counts file indexed by element id
    """
    countsTable = pd.read_csv(countsFileName, header=None, delimiter='\t', names=['id', 'counts'])
    countsTable.index = countsTable['id']
    return countsTable['counts']


def readLibraryFile(libraryFastaFileName, elementTypeFunc, geneNameFunc, miscFuncList=None):
    """return DataFrame of library features indexed by element id
    """
    elementList = []
    with open(libraryFastaFileName) as infile:
        idLine = infile.readline()
        while idLine != '':
            seqLine = infile.readline()
            if idLine[0] != '>' or seqLine == None:
                raise ValueError('Error parsing fasta file')

            elementList.append((idLine[1:].strip(), seqLine.strip()))

            idLine = infile.readline()

    elementIds, elementSeqs = zip(*elementList)
    libraryTable = pd.DataFrame(np.array(elementSeqs), index=np.array(elementIds), columns=['aligned_seq'],
                                dtype='object')

    libraryTable['element_type'] = elementTypeFunc(libraryTable)
    libraryTable['gene_name'] = geneNameFunc(libraryTable)

    if miscFuncList != None:
        colList = [libraryTable]
        for miscFunc in miscFuncList:
            colList.append(miscFunc(libraryTable))
        if len(colList) != 1:
            libraryTable = pd.concat(colList, axis=1)

    return libraryTable


def loadData(experimentName, collapsedToTranscripts=True, premergedCounts=False):
    """load data for given experiment name into python
    """
    dataDict = {'library': pd.read_csv(experimentName + '_librarytable.txt', sep='\t', header=0, index_col=0),
                'counts': pd.read_csv(experimentName + '_mergedcountstable.txt', sep='\t', header=list(range(2)),
                                      index_col=list(range(1))),
                'phenotypes': pd.read_csv(experimentName + '_phenotypetable.txt', sep='\t', header=list(range(2)),
                                          index_col=list(range(1)))}

    if premergedCounts:
        dataDict['premerged counts'] = pd.read_csv(experimentName + '_rawcountstable.txt', sep='\t',
                                                   header=list(range(3)), index_col=list(range(1)))

    if collapsedToTranscripts:
        dataDict['transcript scores'] = pd.read_csv(experimentName + '_genetable.txt', sep='\t', header=list(range(3)),
                                                    index_col=list(range(2)))
        dataDict['gene scores'] = pd.read_csv(experimentName + '_genetable_collapsed.txt', sep='\t',
                                              header=list(range(3)), index_col=list(range(1)))
    else:
        dataDict['gene scores'] = pd.read_csv(experimentName + '_genetable.txt', sep='\t', header=list(range(3)),
                                              index_col=list(range(1)))

    return dataDict


def getNormScore(screen, score, rename=None, rep='ave_rep1_rep2'):
    """extract given phenotype score from screen data and normalize by Negative Control sgRNAs
    """
    df = screen['gene scores'].xs(score, level=0, axis=1).xs(rep, level=0, axis=1)
    del df['transcripts']
    if rename:
        score = rename
    df = df.loc[:, ['average phenotype of strongest 3', 'Mann-Whitney p-value']].rename({
        'average phenotype of strongest 3': f'{score}_score',
        'Mann-Whitney p-value': f'{score}_MW_p-value'
    }, axis='columns')

    # step 1: select neg ctrl gRNAs scores
    ctrl_gRNA = np.array(['pseudo' in g for g in df.index])
    # step 2: measure mean neg ctrl gRNAs scores
    mean_ctrl_gRNA = np.median(df.loc[ctrl_gRNA, score + '.rho'])
    # step 3: subtract mean of neg ctrl gRNAs scores
    df.loc[:, score + '.rho.norm'] = df.loc[:, score + '.rho'] - mean_ctrl_gRNA
    # step 4: measure std of neg ctrl gRNAs scores
    sigma = np.std(df.loc[ctrl_gRNA, score + '.rho'])
    # step 5: divide by std of neg ctrl gRNAs scores
    df.loc[:, score + '.rho.norm'] = df.loc[:, score + '.rho.norm'] / sigma
    # step 6: remove rows with pseudo index, neg control gRNAs
    df = df.loc[ctrl_gRNA == False, :]

    print(f'{score} ->\n\tmean(neg control gRNAs rho score): {mean_ctrl_gRNA}')
    print(f'\tstd(neg control gRNAs rho score): {sigma}')

    return df


def getTopScore(df, value, value_thr, stat, stat_thr, drop_dup=False, silent=False):
    """get top hits from given score dataframe
    value >= value_thr & stat < stat_thr
    """
    up = df.iloc[
         [i for i, l in enumerate(
             np.array([
                 np.array(df.loc[:, value] >= value_thr),
                 np.array(df.loc[:, stat] < stat_thr)]).all(axis=0)) if l == 1], :]
    dn = df.iloc[
         [i for i, l in enumerate(
             np.array([
                 np.array(df.loc[:, value] <= -1 * (value_thr)),
                 np.array(df.loc[:, stat] < stat_thr)]).all(axis=0)) if l == 1], :]

    if drop_dup:
        up = up.sort_values(stat).drop_duplicates(subset='gene_id', keep="last")
        dn = dn.sort_values(stat).drop_duplicates(subset='gene_id', keep="last")

    if not silent:
        print('up: ', up.shape[0])
        print('down:', dn.shape[0])

    return up, dn
