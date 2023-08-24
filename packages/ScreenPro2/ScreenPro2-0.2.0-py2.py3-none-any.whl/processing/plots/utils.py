import matplotlib
import os
import matplotlib.pyplot as plt


almost_black = '#111111'
dark2 = ['#1b9e77',
         '#d95f02',
         '#7570b3',
         '#e7298a',
         '#66a61e',
         '#e6ab02',
         '#a6761d',
         '#666666']
blue_yellow = matplotlib.colors.LinearSegmentedColormap.from_list('BuYl',
                                                                  [(0, '#ffff00'), (.49, '#000000'), (.51, '#000000'),
                                                                   (1, '#0000ff')])
blue_yellow.set_bad('#999999', 1)
yellow_blue = matplotlib.colors.LinearSegmentedColormap.from_list('YlBu',
                                                                  [(0, '#0000ff'), (.49, '#000000'), (.51, '#000000'),
                                                                   (1, '#ffff00')])
yellow_blue.set_bad('#999999', 1)


def setMatplotlib():
    plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'Verdana', 'Bitstream Vera Sans']
    plt.rcParams['font.size'] = 8
    plt.rcParams['font.weight'] = 'regular'

    plt.rcParams['text.color'] = almost_black
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = almost_black
    plt.rcParams['axes.labelcolor'] = almost_black
    # plt.rcParams['axes.color_cycle'] = dark2_all

    axisLineWidth = .5
    plt.rcParams['axes.linewidth'] = axisLineWidth
    plt.rcParams['lines.linewidth'] = 1.5

    plt.rcParams['patch.edgecolor'] = 'none'
    plt.rcParams['patch.linewidth'] = .25
    # plt.rcParams['patch.facecolor'] = dark2_all[0]

    plt.rcParams['savefig.dpi'] = 1000
    # plt.rcParams['savefig.format'] = savefig_format

    plt.rcParams['legend.frameon'] = False
    plt.rcParams['legend.handletextpad'] = .25
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['legend.numpoints'] = 1
    plt.rcParams['legend.scatterpoints'] = 1

    plt.rcParams['ytick.direction'] = 'out'
    plt.rcParams['ytick.color'] = almost_black
    plt.rcParams['ytick.major.width'] = axisLineWidth
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['xtick.color'] = almost_black
    plt.rcParams['xtick.major.width'] = axisLineWidth


def cleanAxes(axis, top=False, right=False, bottom=True, left=True):
    """

    Parameters
    ----------
    axis :

    top :
         (Default value = False)
    right :
         (Default value = False)
    bottom :
         (Default value = True)
    left :
         (Default value = True)

    Returns
    -------

    """
    # adapted from http://nbviewer.ipython.org/github/cs109/content/blob/master/lec_03_statistical_graphs.ipynb
    axis.spines['top'].set_visible(top)
    axis.spines['right'].set_visible(right)
    axis.spines['left'].set_visible(left)
    axis.spines['bottom'].set_visible(bottom)

    #turn off all ticks
    axis.yaxis.set_ticks_position('none')
    axis.xaxis.set_ticks_position('none')

    #now re-enable visibles
    if top:
        axis.xaxis.tick_top()
    if bottom:
        axis.xaxis.tick_bottom()
    if left:
        axis.yaxis.tick_left()
    if right:
        axis.yaxis.tick_right()


def plotGrid(axis, vert_origin=True, horiz_origin=True, unity=True):
    """

    Parameters
    ----------
    axis :

    vert_origin :
         (Default value = True)
    horiz_origin :
         (Default value = True)
    unity :
         (Default value = True)

    Returns
    -------

    """
    ylim = axis.get_ylim()
    xlim = axis.get_xlim()
    if vert_origin:
        axis.plot((0,0), ylim, color='#BFBFBF', lw=.5, alpha=.5)
    if horiz_origin:
        axis.plot(xlim,(0,0), color='#BFBFBF', lw=.5, alpha=.5)
    if unity:
        xmin = min(xlim[0], ylim[0])
        xmax = max(xlim[1], ylim[1])
        axis.plot((xmin,xmax),(xmin,xmax), color='#BFBFBF', lw=.5, alpha=.5)

    axis.set_ylim(ylim)
    axis.set_xlim(xlim)


def listOptions(data, graphType):
    """

    Parameters
    ----------
    data :

    graphType :


    Returns
    -------

    """
    if graphType == 'counts':
        print('Condition and Replicate options are:')
        print('\n'.join(['{0:15}\t{1}'.format(colname[0],colname[1]) for colname, col in data['counts'].iteritems()]))

    elif graphType == 'phenotypes':
        print('Phenotype and Replicate options are:')
        print('\n'.join(['{0:15}\t{1}'.format(colname[0],colname[1]) for colname, col in data['phenotypes'].iteritems()]))

    elif graphType == 'genes':
        colTups = sorted(list(set([colname[:2] for colname, col in data['gene scores'].iteritems()])))
        print('Phenotype and Replicate options are:')
        print('\n'.join(['{0:15}\t{1}'.format(colname[0],colname[1]) for colname in colTups]))

    else:
        print('Graph type not recognized')


def checkOptions(data, graphType, optionTuple):
    """

    Parameters
    ----------
    data :

    graphType :

    optionTuple :


    Returns
    -------

    """
    if optionTuple[0] == None or optionTuple[1] == None:
        listOptions(data, graphType)
        return False

    if graphType == 'counts':
        colTups = set([colname[:2] for colname, col in data['counts'].iteritems()])
    elif graphType == 'phenotypes':
        colTups = set([colname[:2] for colname, col in data['phenotypes'].iteritems()])
    elif graphType == 'genes':
        colTups = set([colname[:2] for colname, col in data['gene scores'].iteritems()])
    else:
        print('Graph type not recognized')
        return False

    if optionTuple in colTups:
        return True
    else:
        print('{0} {1} not recognized'.format(optionTuple[0],optionTuple[1]))
        listOptions(data, graphType)
        return False
