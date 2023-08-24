import os
from volcano import volcanoPlot
import matplotlib.pyplot as plt
import argparse

# def setDisplayFigure(plotDirectory=None, imageExtension='pdf', plotWithPylab=True, figureScale=1):
#     return plotDirectory, imageExtension, plotWithPylab, figureScale


def displayFigure(fig, plotDirectory=None, imageExtension='pdf', savetitle=''):
    if plotDirectory:
        figNums = [int(fileName.split('_fig_')[0]) for fileName in os.listdir(plotDirectory) if
                   len(fileName.split('_fig_')) >= 2]
        if len(figNums) == 0:
            nextFigNum = 0
        else:
            nextFigNum = max(figNums) + 1

        fullTitle = os.path.join(plotDirectory, '{0:03d}_fig_{1}.{2}'.format(nextFigNum, savetitle, imageExtension))
        print(fullTitle)
        fig.savefig(fullTitle, dpi=1000)
        plt.close(fig)

        return fullTitle


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Process raw sequencing data from screens to counts files in parallel')
    # parser.add_argument('Library_Fasta', help='Fasta file of expected library reads.')
    # parser.add_argument('Out_File_Path', help='Directory where output files should be written.')
    # parser.add_argument('Seq_File_Names', nargs='+',
    #                     help='Name(s) of sequencing file(s). Unix wildcards can be used to select multiple files at once. The script will search for all *.fastq.gz, *.fastq, and *.fa(/fasta/fna) files with the given wildcard name.')
    #
    # parser.add_argument('-p', '--processors', type=int, default=1)
    # parser.add_argument('--trim_start', type=int)
    # parser.add_argument('--trim_end', type=int)
    # parser.add_argument('--test', action='store_true', default=False,
    #                     help='Run the entire script on only the first %d reads of each file. Be sure to delete or move all test files before re-running script as they will not be overwritten.' % testLines)
    #
    # args = parser.parse_args()

    figs = {
        "volcano": volcanoPlot()
        # add other plots
    }

    for name, fig in figs.items():
        displayFigure(fig, savetitle=name)