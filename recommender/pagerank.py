

"""
    This function return a vector as big as the number of papers, and for each paper of the vector contain a coefficient
    The first parameter is the set with all the papers
    The second parameter is a function telling for a certain paper all the papers that cites it
    (Optional) The third argument is the minimum of changes required to said that a loop has been useful
    (Optional) The fourth argument is te max rounds we like the algorithm to do
"""

def pagerank(paperSet, paperCites, minChanges=2, maxRounds=150):
    ranks = [0]*len(paperSet)  # Creating the answer array
    changes = minChanges + 1 # Just to be sure to enter the while once
    rounds = 0
    avgRank = 1
    jumpProbability = 0.15
    while (changes<minChanges & rounds < maxRounds):
        for i in range (len(paperSet)):       # For each paper of the paperSet, we calculate a rank
            citingPaper = paperCites(paperSet[i])     #Here, we get the citation from the paper i (in the paperSet Array
            previousRank = ranks[i]
            if (len(citingPaper) == 0) :              # If there is no citations from this paper, it get only the average rank
                ranks[i] = avgRank
            else :
                ranks[i] = 0
                for j in range(len(citingPaper)):
                    ranks[i] = ranks[citingPaper[j][0]] * citingPaper[j][1] # WARNING HERE : the citing paper needs to be an array of tuples that contains :
                                                                            # as first argument the paper ID (to retrieve the paper in the paperSet)
                                                                            # as second argument the number of citations
                ranks[i]*= (1-jumpProbability) + jumpProbability

            if (previousRank - ranks[i]) > 0.1 :            # To be adapted if it is too strong or too light
                changes += 1
        avgRank = avgArray(ranks)
        rounds += 1
    return ranks

"""
    This function simply makes an average of an array passed as a parameter
    The only argument is the array
"""

def avgArray(foo):
    avg = 0
    for i in range (len(foo)):
        avg += foo[i]
    avg /= len(foo)
    return avg


