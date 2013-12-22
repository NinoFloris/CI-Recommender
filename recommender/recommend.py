def getRecommendedAuthors(itemMatch, author_name):
    userRatings = []   
    for i, item in enumerate(config.SUMMARIES):
        if author_name in config.SUMMARIES[i].authors:
            userRatings.append(config.SUMMARIES[i].authors)

    for item in userRatings:
        print item

    scores={}
    totalSim={}
    # Loop over items rated by this user
    for (item,rating) in userRatings:
    # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
    # Divide each total score by total weighting to get an average
    rankings=[(score/totalSim[item],item) for item,score in scores.items( )]
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings