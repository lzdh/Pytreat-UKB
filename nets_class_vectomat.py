def nets_class_vectomat(Y):
    N = len(Y)
    #uY = np.unique(Y)
    uY=list(set(Y))
    q = len(uY)
    Ym = np.zeros((N,q))
    #Ym = []
    for i, char in enumerate(Y):
        #Ym.append(uY == char)
        Ym[i, uY.index(char)]=1
    return Ym #1*np.vstack(Ym)
