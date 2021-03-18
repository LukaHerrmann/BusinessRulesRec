
def getitems(collection, filter, limit=False, sortterm=False):
    '''Deze functie haalt alle items op uit een MongoDB collection'''
    result = collection.find(filter)
    if sortterm:
        result = result.sort(sortterm)
    if limit:
        return result[:limit]
    return result