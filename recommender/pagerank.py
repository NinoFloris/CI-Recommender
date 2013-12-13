import collections

def pagerank(paperCitations, paperCitedBy, minChanges=10, maxRounds=150):
    """Calculates the pagerank for every citation of the papers we have citation data of.

    Keyword arguments:
    paperCitations -- the dict containing all the papers and their citations
    paperCitedBy -- the inversed dict of paperCitations
    minChanges -- the minimum of changes required for the loop to continue (default 10)
    maxRounds -- the max rounds pagerank should do, minChanges breaks out of this loop first (default 150)

    Returns -- tuple: (rounds=int, {pmid: pagerank})

    """
    ranks = {}  # Creating the answer array
    changes = minChanges + 1  # Just to be  sure to enter the while once
    rounds = 0
    avgRank = 1.0
    jumpProbability = 0.15

    while (changes > minChanges and rounds < maxRounds):
        changes = 0
        for pmid, citations in paperCitations.iteritems():      
            # For each paper of the paperSet, we calculate a rank #Baudouin
            if (len(citations) > 0):
                oldRank = ranks.setdefault(pmid, avgRank)
                rank = 0.0

                for reference in paperCitedBy[pmid]:
                    try:
                        # Try to apply the PR formula : PR(n) / citations#(n) #Baudouin
                        rank += (ranks[reference] / len(paperCitations[reference]))
                    except KeyError:
                        # Otherwise : default value (PR average and average outgoing citations of 3) #Baudouin
                        # If this paper is outside the dataset use the avgRank divided by the supposed amount of cited papers. #Nino
                        rank += avgRank / 3

                ranks[pmid] = (1-jumpProbability) * rank + jumpProbability
                if (oldRank - ranks[pmid]) > 0.01:            # To be adapted if it is too strong or too light
                    changes += 1
            else:
                ranks[pmid] = avgRank
        rounds += 1
    return (rounds, ranks)



def citedBy(paperCitations):
    """Creates the inverse of the citation dataset

        Keyword arguments:
        paperCitations -- the dict containing all the papers and their citations

        Returns -- {pmid: [references]}
        
    """
    cited_by = collections.defaultdict(list)
    for ref, papers_citing_ref in paperCitations.iteritems():
        for pmid in papers_citing_ref:
            cited_by[pmid].append(ref)
    return cited_by


