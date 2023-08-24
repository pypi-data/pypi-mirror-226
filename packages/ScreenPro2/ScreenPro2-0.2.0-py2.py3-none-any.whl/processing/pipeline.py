"""screen processing pipeline that requires just a config file and a directory of supported libraries
error checking in config parser is fairly robust, so not checking for input errors here
"""
import sys
import argparse

from processing.configs import parseExptConfig, parseLibraryConfig
from processing.utils import makeDirectory, printNow
from processing.phenotypes.scores import *
from processing.plots.phenotype_level import *
from processing.plots.count_level import *
from processing.plots.volcano import *

defaultLibConfigName = 'library_config.txt'


def processExperimentsFromConfig(configFile, libraryDirectory, generatePlots='png'):
    # load in the supported libraries and sublibraries
    try:
        librariesToSublibraries, librariesToTables = parseLibraryConfig(
            os.path.join(libraryDirectory, defaultLibConfigName))
    except ValueError as err:
        print(' '.join(err.args))
        return

    exptParameters, parseStatus, parseString = parseExptConfig(configFile, librariesToSublibraries)

    printNow(parseString)

    if parseStatus > 0:  # Critical errors in parsing
        print('Exiting due to experiment config file errors\n')
        return

    makeDirectory(exptParameters['output_folder'])
    outbase = os.path.join(exptParameters['output_folder'], exptParameters['experiment_name'])

    if generatePlots != 'off':
        plotDirectory = os.path.join(exptParameters['output_folder'], exptParameters['experiment_name'] + '_plots')
        makeDirectory(plotDirectory)

        print("changeDisplayFigureSettings!")
        # changeDisplayFigureSettings(newDirectory=plotDirectory, newImageExtension=generatePlots,
        #                                             newPlotWithPylab=False)

    # load in library table and filter to requested sublibraries
    printNow('Accessing library information')

    libraryTable = pd.read_csv(os.path.join(libraryDirectory, librariesToTables[exptParameters['library']]), sep='\t',
                               header=0, index_col=0).sort_index()
    sublibColumn = libraryTable.apply(lambda row: row['sublibrary'].lower() in exptParameters['sublibraries'], axis=1)

    if sum(sublibColumn) == 0:
        print('After limiting analysis to specified sublibraries, no elements are left')
        return

    libraryTable[sublibColumn].to_csv(outbase + '_librarytable.txt', sep='\t')

    # load in counts, create table of total counts in each and each file as a column
    printNow('Loading counts data')

    columnDict = dict()
    for tup in sorted(exptParameters['counts_file_list']):
        if tup in columnDict:
            print(
                'Asserting that tuples of condition, replicate, and count file should be unique; '
                'are the cases where this should not be enforced?'
            )
            raise Exception('condition, replicate, and count file combination already assigned')

        countSeries = readCountsFile(tup[2]).reset_index().drop_duplicates('id').set_index(
            'id')  # for now also dropping duplicate ids in counts for overlapping linc sublibraries
        countSeries = libraryTable[sublibColumn].align(countSeries, axis=0, join='left', fill_value=0)[
            1]  # expand series to fill 0 for every missing entry

        columnDict[tup] = countSeries['counts']  # [sublibColumn] #then shrink series to only desired sublibraries

    # print columnDict
    countsTable = pd.DataFrame(columnDict)  # , index=libraryTable[sublibColumn].index)
    countsTable.to_csv(outbase + '_rawcountstable.txt', sep='\t')
    countsTable.sum().to_csv(outbase + '_rawcountstable_summary.txt', sep='\t', header=False)

    # merge counts for same conditions/replicates, and create summary table
    # save scatter plot before each merger, and histogram of counts post mergers
    printNow('Merging experiment counts split across lanes/indexes')

    exptGroups = countsTable.groupby(level=[0, 1], axis=1)
    mergedCountsTable = exptGroups.aggregate(np.sum)
    mergedCountsTable.to_csv(outbase + '_mergedcountstable.txt', sep='\t')
    mergedCountsTable.sum().to_csv(outbase + '_mergedcountstable_summary.txt', sep='\t', header=False)

    if generatePlots != 'off' and max(exptGroups.count().iloc[0]) > 1:
        printNow('-generating scatter plots of counts pre-merger')

        tempDataDict = {'library': libraryTable[sublibColumn],
                        'premerged counts': countsTable,
                        'counts': mergedCountsTable}

        for (phenotype, replicate), countsCols in exptGroups:
            if len(countsCols.columns) == 1:
                continue

            else:
                premergedCountsScatterMatrix(tempDataDict, phenotype, replicate)

    if generatePlots != 'off':
        printNow('-generating sgRNA read count histograms')

        tempDataDict = {'library': libraryTable[sublibColumn],
                        'counts': mergedCountsTable}

        for (phenotype, replicate), countsCol in mergedCountsTable.iteritems():
            countsHistogram(tempDataDict, phenotype, replicate)

    # create pairs of columns for each comparison, filter to na, then generate sgRNA phenotype score
    printNow('Computing sgRNA phenotype scores')

    growthValueDict = {(tup[0], tup[1]): tup[2] for tup in exptParameters['growth_value_tuples']}
    phenotypeList = list(set(list(zip(*exptParameters['condition_tuples']))[0]))
    replicateList = sorted(list(set(list(zip(*exptParameters['counts_file_list']))[1])))

    phenotypeScoreDict = dict()
    for (phenotype, condition1, condition2) in exptParameters['condition_tuples']:
        for replicate in replicateList:
            column1 = mergedCountsTable[(condition1, replicate)]
            column2 = mergedCountsTable[(condition2, replicate)]
            filtCols = filterLowCounts(pd.concat((column1, column2), axis=1, sort=True), exptParameters['filter_type'],
                                       exptParameters['minimum_reads'])

            score = computePhenotypeScore(filtCols[(condition1, replicate)], filtCols[(condition2, replicate)],
                                          libraryTable[sublibColumn], growthValueDict[(phenotype, replicate)],
                                          exptParameters['pseudocount_behavior'], exptParameters['pseudocount'])

            phenotypeScoreDict[(phenotype, replicate)] = score

    if generatePlots != 'off':
        tempDataDict = {'library': libraryTable[sublibColumn],
                        'counts': mergedCountsTable,
                        'phenotypes': pd.DataFrame(phenotypeScoreDict)}

        printNow('-generating phenotype histograms and scatter plots')

        for (phenotype, condition1, condition2) in exptParameters['condition_tuples']:
            for replicate in replicateList:
                countsScatter(tempDataDict, condition1, replicate, condition2, replicate,
                                              colorByPhenotype_condition=phenotype,
                                              colorByPhenotype_replicate=replicate)

                phenotypeHistogram(tempDataDict, phenotype, replicate)
                sgRNAsPassingFilterHist(tempDataDict, phenotype, replicate)

    # scatterplot sgRNAs for all replicates, then average together and add columns to phenotype score table
    if len(replicateList) > 1:
        printNow('Averaging replicates')

        for phenotype in phenotypeList:
            repCols = pd.DataFrame(
                {(phen, rep): col for (phen, rep), col in phenotypeScoreDict.items() if phen == phenotype})
            # average nan and real to nan; otherwise this could lead to data points with just one rep informing results
            phenotypeScoreDict[(phenotype, 'ave_' + '_'.join(replicateList))] = repCols.mean(axis=1,
                                                                                             skipna=False)

    phenotypeTable = pd.DataFrame(phenotypeScoreDict).sort_index(axis=1)
    phenotypeTable.to_csv(outbase + '_phenotypetable.txt', sep='\t')

    if len(replicateList) > 1 and generatePlots != 'off':
        tempDataDict = {'library': libraryTable[sublibColumn],
                        'phenotypes': phenotypeTable}

        printNow('-generating replicate phenotype histograms and scatter plots')

        for phenotype, phengroup in phenotypeTable.groupby(level=0, axis=1):
            for i, ((p, rep1), col1) in enumerate(phengroup.iteritems()):
                if rep1[:4] == 'ave_':
                    phenotypeHistogram(tempDataDict, phenotype, rep1)

                for j, ((p, rep2), col2) in enumerate(phengroup.iteritems()):
                    if rep2[:4] == 'ave_' or j <= i:
                        continue

                    else:
                        phenotypeScatter(tempDataDict, phenotype, rep1, phenotype, rep2)

                        # generate pseudogenes
    negTable = phenotypeTable.loc[libraryTable[sublibColumn].loc[:, 'gene'] == 'negative_control', :]

    if exptParameters['generate_pseudogene_dist'] != 'off' and len(exptParameters['analyses']) > 0:
        print('Generating a pseudogene distribution from negative controls')
        sys.stdout.flush()

        pseudoTableList = []
        pseudoLibTables = []
        negValues = negTable.values
        negColumns = negTable.columns

        if exptParameters['generate_pseudogene_dist'].lower() == 'manual':
            for pseudogene in range(exptParameters['num_pseudogenes']):
                randIndices = np.random.randint(0, len(negTable), exptParameters['pseudogene_size'])
                pseudoTable = negValues[randIndices, :]
                pseudoIndex = ['pseudo_%d_%d' % (pseudogene, i) for i in range(exptParameters['pseudogene_size'])]
                pseudoSeqs = ['seq_%d_%d' % (pseudogene, i) for i in
                              range(exptParameters['pseudogene_size'])]  # so pseudogenes aren't treated as duplicates
                pseudoTableList.append(pd.DataFrame(pseudoTable, index=pseudoIndex, columns=negColumns))
                pseudoLib = pd.DataFrame({'gene': ['pseudo_%d' % pseudogene] * exptParameters['pseudogene_size'],
                                          'transcripts': ['na'] * exptParameters['pseudogene_size'],
                                          'sequence': pseudoSeqs}, index=pseudoIndex)
                pseudoLibTables.append(pseudoLib)

        elif exptParameters['generate_pseudogene_dist'].lower() == 'auto':
            for pseudogene, (gene, group) in enumerate(
                    libraryTable[sublibColumn].drop_duplicates(['gene', 'sequence']).groupby('gene')):
                if gene == 'negative_control':
                    continue
                for transcript, (transcriptName, transcriptGroup) in enumerate(group.groupby('transcripts')):
                    randIndices = np.random.randint(0, len(negTable), len(transcriptGroup))
                    pseudoTable = negValues[randIndices, :]
                    pseudoIndex = ['pseudo_%d_%d_%d' % (pseudogene, transcript, i) for i in range(len(transcriptGroup))]
                    pseudoSeqs = ['seq_%d_%d_%d' % (pseudogene, transcript, i) for i in range(len(transcriptGroup))]
                    pseudoTableList.append(pd.DataFrame(pseudoTable, index=pseudoIndex, columns=negColumns))
                    pseudoLib = pd.DataFrame({'gene': ['pseudo_%d' % pseudogene] * len(transcriptGroup),
                                              'transcripts': ['pseudo_transcript_%d' % transcript] * len(
                                                  transcriptGroup),
                                              'sequence': pseudoSeqs}, index=pseudoIndex)
                    pseudoLibTables.append(pseudoLib)

        else:
            print('generate_pseudogene_dist parameter not recognized, defaulting to off')

        phenotypeTable = phenotypeTable.append(pd.concat(pseudoTableList, sort=True))
        libraryTableGeneAnalysis = libraryTable[sublibColumn].append(pd.concat(pseudoLibTables, sort=True))
    else:
        libraryTableGeneAnalysis = libraryTable[sublibColumn]

    # compute gene scores for replicates, averaged reps, and pseudogenes
    if len(exptParameters['analyses']) > 0:
        print('Computing gene scores')
        sys.stdout.flush()

        phenotypeTable_deduplicated = phenotypeTable.loc[
            libraryTableGeneAnalysis.drop_duplicates(['gene', 'sequence']).index]
        if exptParameters['collapse_to_transcripts'] == True:
            geneGroups = phenotypeTable_deduplicated.loc[libraryTableGeneAnalysis.loc[:, 'gene'] != 'negative_control',
                         :].groupby([libraryTableGeneAnalysis['gene'], libraryTableGeneAnalysis['transcripts']])
        else:
            geneGroups = phenotypeTable_deduplicated.loc[libraryTableGeneAnalysis.loc[:, 'gene'] != 'negative_control',
                         :].groupby(libraryTableGeneAnalysis['gene'])

        analysisTables = []
        for analysis in exptParameters['analyses']:
            print('--' + analysis)
            sys.stdout.flush()

            analysisTables.append(
                applyGeneScore(
                    groupedPhenotypeTable = geneGroups,
                    negativeTable =  negTable,
                    analysis = analysis,
                    analysisParamList = exptParameters['analyses'][analysis]
                ))

        geneTable = pd.concat(analysisTables, axis=1, sort=True).reorder_levels([1, 2, 0], axis=1).sort_index(axis=1)
        geneTable.to_csv(outbase + '_genetable.txt', sep='\t')

        # collapse the gene-transcript indices into a single score for a gene by best MW p-value, where applicable
        if exptParameters['collapse_to_transcripts'] == True and 'calculate_mw' in exptParameters['analyses']:
            print('Collapsing transcript scores to gene scores')
            sys.stdout.flush()

            geneTableCollapsed = scoreGeneByBestTranscript(geneTable)
            geneTableCollapsed.to_csv(outbase + '_genetable_collapsed.txt', sep='\t')

    if generatePlots != 'off':
        if 'calculate_ave' in exptParameters['analyses'] and 'calculate_mw' in exptParameters['analyses']:
            tempDataDict = {'library': libraryTable[sublibColumn],
                            'gene scores': geneTableCollapsed if exptParameters[
                                'collapse_to_transcripts'] else geneTable}

            for (phenotype, replicate), gtable in geneTableCollapsed.groupby(level=[0, 1], axis=1):
                if len(replicateList) == 1 or replicate[:4] == 'ave_':  # just plot averaged reps where available
                    volcanoPlot(tempDataDict, phenotype, replicate, labelHits=True)

    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate sgRNA- and gene-level phenotypes based on sequencing read counts, as specified by the experiment config file.')
    parser.add_argument('Config_File',
                        help='Experiment config file specifying screen analysis settings (see accomapnying BLANK and DEMO files).')
    parser.add_argument('Library_File_Directory',
                        help='Directory containing reference library tables and the library_config.txt file.')

    parser.add_argument('--plot_extension', default='png',
                        help='Image extension for plot files, or \"off\". Default is png.')

    args = parser.parse_args()
    # print args

    processExperimentsFromConfig(args.Config_File, args.Library_File_Directory, args.plot_extension.lower())
