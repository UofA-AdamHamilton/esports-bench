def clique_completion(network, k = 2):
    """
    Code that treats the 
    inputs: network
            k: even integer  
    """
    # check that k is an even integer
    if k%2 != 0:
        raise Exception('k must be an even integer')
    pass

if __name__ == '__main__':
    clique_completion(1,3)