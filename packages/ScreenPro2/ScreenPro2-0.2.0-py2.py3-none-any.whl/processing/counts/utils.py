"""utility functions
"""
import os
import sys
import glob
import fnmatch


acceptedFileTypes = [('*.fastq.gz', 'fqgz'),
                     ('*.fastq', 'fq'),
                     ('*.fq', 'fq'),
                     ('*.fa', 'fa'),
                     ('*.fasta', 'fa'),
                     ('*.fna', 'fa')]

testLines = 10000


def parseSeqFileNames(fileNameList):
    """

    Parameters
    ----------
    fileNameList :


    Returns
    -------

    """
    infileList = []
    outfileBaseList = []

    for inputFileName in fileNameList:  # iterate through entered filenames for sequence files
        for filename in glob.glob(inputFileName):  # generate all possible files given wildcards
            for fileType in list(zip(*acceptedFileTypes))[0]:  # iterate through allowed filetypes
                if fnmatch.fnmatch(filename, fileType):
                    infileList.append(filename)
                    outfileBaseList.append(os.path.split(filename)[-1].split('.')[0])

    return infileList, outfileBaseList


def getMismatchDict(table, column, trim_range = None, allowOneMismatch=True):
    mismatch_dict = dict()

    if trim_range:
        col = table[column].apply(lambda seq: seq[trim_range[0]:trim_range[1]])
    else:
        col = table[column]

    for sgRNA, seq in col.iteritems():
        if seq in mismatch_dict:
            print('clash with 0 mismatches', sgRNA, seq)
            mismatch_dict[seq] = 'multiple'
        else:
            mismatch_dict[seq] = sgRNA

        if allowOneMismatch:
            for position in range(len(seq)):
                mismatchSeq = seq[:position] + 'N' + seq[position + 1:]

                if mismatchSeq in mismatch_dict:
                    print('clash with 1 mismatch', sgRNA, mismatchSeq)
                    mismatch_dict[seq] = 'multiple'
                else:
                    mismatch_dict[mismatchSeq] = sgRNA

    return mismatch_dict


def matchBarcode(mismatch_dict, barcode, allowOneMismatch=True):
    if barcode in mismatch_dict:
        match = mismatch_dict[barcode]

    elif allowOneMismatch:
        match = 'none'
        for position in range(len(barcode)):
            mismatchSeq = barcode[:position] + 'N' + barcode[position + 1:]

            if mismatchSeq in mismatch_dict:
                if match == 'none':
                    match = mismatch_dict[mismatchSeq]
                else:
                    match = 'multiple'

    else:
        match = 'none'

    return match

# def printCountsFilePaths(baseDirectoryPathList):
#     """print all counts file paths, to assist with making an experiment table
#     """
#     print('Make a tab-delimited file with the following columns:')
#     print('counts_file\texperiment\tcondition\treplicate_id')
#     print('and the following list in the counts_file column:')
#     for basePath in baseDirectoryPathList:
#         for root, dirs, filenames in os.walk(basePath):
#             for filename in fnmatch.filter(filenames, '*.counts'):
#                 print(os.path.join(root, filename))
