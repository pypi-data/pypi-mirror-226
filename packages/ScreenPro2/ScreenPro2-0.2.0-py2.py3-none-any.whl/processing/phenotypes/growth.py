

def parseGKFile(gkFileName):
    """parse a tab-delimited file (calculated with martin's parse_growthdata.py)
    column headers: experiment, replicate_id, G_value, K_value"""

    gkdict = dict()

    with open(gkFileName, 'rU') as infile:
        for line in infile:
            if line.split('\t')[0] == 'experiment':
                continue
            else:
                linesplit = line.strip().split('\t')
                gkdict[(linesplit[0], linesplit[1])] = (float(linesplit[2]), float(linesplit[3]))

    return gkdict
