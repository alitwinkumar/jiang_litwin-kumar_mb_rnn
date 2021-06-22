
#helper function to find the stimulus pattern corresponding to the first presented stimulus
def findstimA(s0):
    T,S,B = s0.shape
    sA = np.zeros([S,B])
    sums0 = np.sum(s0,1)
    for bi in range(B):
        tind = np.where(sums0[:,bi] > 0)[0][0]
        sA[:,bi] = s0[tind,:,bi]
    
    return sA


####################### initial conditions ########################
def geninitialcond(B):
    m0 = minit*np.ones([M,B],dtype=np.float32)
    d0 = dinit*np.ones([D,B],dtype=np.float32)
    o0 = oinit*np.ones([O,B],dtype=np.float32)
    w0 = np.ones([M,S,B],dtype=np.float32)/(S*f)
    sbar0 = np.zeros([S,B],dtype=np.float32)
    dabar0 = np.zeros([M,B],dtype=np.float32)

    return m0,d0,o0,w0,sbar0,dabar0


####################### trials ########################

def genrandtrials(B,probs):
    s = np.zeros([T,S,B],dtype=np.float32)
    u = np.zeros([T,U,B],dtype=np.float32)
    rtarg = np.zeros([T,R,B],dtype=np.float32)

    trialinfo = [dict() for bi in range(B)]

    for bi in range(B):
        valence = np.random.choice([-1,1])
        ttype = np.random.choice(["firstorder","secondorder","extinction"],p=[probs["firstorder"],probs["secondorder"],probs["extinction"]])
        isvalid = np.random.rand() < probs["valid"]

        if ttype == "extinction":
            if isvalid:
                s[:,:,bi],u[:,:,bi],rtarg[:,:,bi],trialinfo[bi] = extinctiontrial(valence,True,False,True,True)
            else:
                s[:,:,bi],u[:,:,bi],rtarg[:,:,bi],trialinfo[bi] = extinctiontrial(valence,np.random.randint(2),np.random.randint(2),np.random.randint(2),np.random.randint(2))

        elif ttype == "secondorder":
            if isvalid:
                s[:,:,bi],u[:,:,bi],rtarg[:,:,bi],trialinfo[bi] = secondordertrial(valence,True,True,True,False)
            else:
                s[:,:,bi],u[:,:,bi],rtarg[:,:,bi],trialinfo[bi] = secondordertrial(valence,np.random.randint(2),np.random.randint(2),np.random.randint(2),np.random.randint(2))

        elif ttype == "firstorder":
            if isvalid:
                s[:,:,bi],u[:,:,bi],rtarg[:,:,bi],trialinfo[bi] = firstordertrial(valence,True,False)
            else:
                s[:,:,bi],u[:,:,bi],rtarg[:,:,bi],trialinfo[bi] = firstordertrial(valence,np.random.randint(2),np.random.randint(2))

    return s,u,rtarg,trialinfo


####################### trial types ########################
def firstordertrial(valence,doUS,doC,teststart=65):
    s = np.zeros([T,S])
    u = np.zeros([T,U])
    rtarg = np.zeros([T,R])

    ainds = np.random.choice(S,int(f*S),replace=False)
    cinds = np.random.choice(S,int(f*S),replace=False)
    stimA = np.zeros(S); stimA[ainds] = 1
    stimC = np.zeros(S); stimC[cinds] = 1


    trialinfo = dict()

    tA = int(np.random.randint(5,15)/dt)
    s[tA:(tA+cslen),:] = stimA
    tUS = tA + dus


    ttest = int(np.random.randint(teststart,teststart+10)/dt)
    if doC:
        s[ttest:(ttest+cslen),:] = stimC
    else:
        s[ttest:(ttest+cslen),:] = stimA

    if doUS:
        if valence > 0:
            u[tUS:(tUS+uslen),0] = 1.
        else:
            u[tUS:(tUS+uslen),1] = 1.

    if doUS and not doC:
        rtarg[ttest:(ttest+cslen),0] = valence

    trialinfo["type"] = "firstorder"
    trialinfo["tA"] = tA
    trialinfo["tUS"] = tUS
    trialinfo["valence"] = valence
    trialinfo["ttest"] = ttest
    trialinfo["stimA"] = stimA
    trialinfo["stimC"] = stimC
    trialinfo["doUS"] = doUS
    trialinfo["doC"] = doC

    return s,u,rtarg,trialinfo

def secondordertrial(valence,doUS,doA,doA2,doC):
    ainds = np.random.choice(S,int(f*S),replace=False)
    binds = np.random.choice(S,int(f*S),replace=False)
    cinds = np.random.choice(S,int(f*S),replace=False)
    stimA = np.zeros(S); stimA[ainds] = 1
    stimB = np.zeros(S); stimB[binds] = 1
    stimC = np.zeros(S); stimC[cinds] = 1

    s = np.zeros([T,S])
    u = np.zeros([T,U])
    rtarg = np.zeros([T,R])

    tA = int(np.random.randint(5,15)/dt)
    tUS = tA + dus

    tB = int(np.random.randint(35,45)/dt)
    tA2 = tB + dus

    ttest = int(np.random.randint(65,75)/dt)

    trialinfo = dict()

    if doA:
        s[tA:(tA+cslen),:] = stimA

    if doUS:
        if valence > 0:
            u[tUS:(tUS+uslen),0] = 1.
        else:
            u[tUS:(tUS+uslen),1] = 1.

    s[tB:(tB+cslen),:] = stimB

    if doA2:
        s[tA2:(tA2+cslen),:] = stimA
    elif doC:
        s[tA2:(tA2+cslen),:] = stimC

    s[ttest:(ttest+cslen),:] = stimB

    if doUS and doA and doA2:
        rtarg[ttest:(ttest+cslen),0] = valence
        rtarg[tA2:(tA2+cslen),0] = valence

    trialinfo["type"] = "secondorder"
    trialinfo["tA"] = tA
    trialinfo["tUS"] = tUS
    trialinfo["tB"] = tB
    trialinfo["tA2"] = tA2
    trialinfo["valence"] = valence
    trialinfo["ttest"] = ttest
    trialinfo["stimA"] = stimA
    trialinfo["stimB"] = stimB
    trialinfo["stimC"] = stimC
    trialinfo["doUS"] = doUS
    trialinfo["doA"] = doA
    trialinfo["doA2"] = doA2
    trialinfo["doC"] = doC

    return s,u,rtarg,trialinfo

def extinctiontrial(valence,doUS,doUS2,doA,doA2):
    ainds = np.random.choice(S,int(f*S),replace=False)
    binds = np.random.choice(S,int(f*S),replace=False)
    stimA = np.zeros(S); stimA[ainds] = 1
    stimB = np.zeros(S); stimB[binds] = 1

    s = np.zeros([T,S])
    u = np.zeros([T,U])
    rtarg = np.zeros([T,R])

    tA = int(np.random.randint(5,15)/dt)
    tUS = tA + dus

    tA2 = int(np.random.randint(35,45)/dt)
    tUS2 = tA2 + dus

    ttest = int(np.random.randint(65,75)/dt)

    if doA:
        s[tA:(tA+cslen),:] = stimA

    if doUS:
        if valence > 0:
            u[tUS:(tUS+uslen),0] = 1.
        else:
            u[tUS:(tUS+uslen),1] = 1.

    if doA2:
        s[tA2:(tA2+cslen),:] = stimA
    else:
        s[tA2:(tA2+cslen),:] = stimB

    if doUS2:
        if valence > 0:
            u[tUS2:(tUS2+uslen),0] = 1.
        else:
            u[tUS2:(tUS2+uslen),1] = 1.

    s[ttest:(ttest+cslen),:] = stimA

    trialinfo = dict()

    if doA:
        if doUS:
            if doA2:
                rtarg[tA2:(tA2+cslen),0] = valence
                if doUS2: #two pairings
                    rtarg[ttest:(ttest+cslen),0] = valence
                else: #one pairing, extinction
                    rtarg[ttest:(ttest+cslen),0] = valence/2
            else: #one pairing, second odor presentation omitted (no extinction)
                rtarg[ttest:(ttest+cslen),0] = valence
        else: #no initial pairing
            if doA2 and doUS2:
                rtarg[ttest:(ttest+cslen),0] = valence
    else: #no initial odor
        if doA2 and doUS2:
            rtarg[ttest:(ttest+cslen),0] = valence
    trialinfo["type"] = "extinction"
    trialinfo["tA"] = tA
    trialinfo["tUS"] = tUS
    trialinfo["tUS2"] = tUS2
    trialinfo["tA2"] = tA2
    trialinfo["valence"] = valence
    trialinfo["ttest"] = ttest
    trialinfo["stimA"] = stimA
    trialinfo["stimB"] = stimB
    trialinfo["doUS"] = doUS
    trialinfo["doA"] = doA
    trialinfo["doA2"] = doA2
    trialinfo["doUS2"] = doUS2


    return s,u,rtarg,trialinfo

