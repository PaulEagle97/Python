"""
"""
import math
import random
import urllib.request

import matplotlib.pyplot as plt
import project_4 as helper_module
    

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib.request.urlopen(filename)
    ykeys = scoring_file.readline().decode('utf-8')
    ykeychars = ykeys.split()
    lines = scoring_file.readlines()
    for line in lines:
        line_dec = line.decode('utf-8')
        vals = line_dec.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib.request.urlopen(filename)
    protein_seq = str(protein_file.read(), "utf-8")
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib.request.urlopen(filename)
    
    # read in files as string
    words = str(word_file.read(), "utf-8")
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print ("Loaded a dictionary with", len(word_list), "words")
    return word_list




if __name__ == "__main__":
    # URLs for data files
    PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
    HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
    FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
    CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
    WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"

    scoring_matrix = read_scoring_matrix(PAM50_URL)
    human_protein = read_protein(HUMAN_EYELESS_URL)
    fly_protein = read_protein(FRUITFLY_EYELESS_URL)
    consensus = read_protein(CONSENSUS_PAX_URL)

    allignment_matrix = helper_module.compute_alignment_matrix(human_protein, fly_protein, scoring_matrix, False)
    score, human_local, fly_local = helper_module.compute_local_alignment(human_protein, fly_protein, scoring_matrix, allignment_matrix)
    print(score)

    human_local = human_local.replace("-", "")
    fly_local = fly_local.replace("-", "")

    human_consensus = helper_module.compute_global_alignment(human_local, consensus, scoring_matrix, allignment_matrix)
    fly_consensus = helper_module.compute_global_alignment(fly_local, consensus, scoring_matrix, allignment_matrix)

    counter = 0
    for idx in range(len(human_consensus[1])):
        if human_consensus[1][idx] == human_consensus[2][idx]:
            counter += 1
    human_perc = counter / len(human_consensus[1]) * 100
    print (human_perc)

    counter = 0
    for idx in range(len(fly_consensus[1])):
        if fly_consensus[1][idx] == fly_consensus[2][idx]:
            counter += 1
    fly_perc = counter / len(fly_consensus[1]) * 100
    print (fly_perc)

