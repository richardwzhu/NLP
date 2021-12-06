import string

trainingFile = open('WSJ_02-21.pos-chunk', 'r').readlines()
tFeatureValues = [None]*len(trainingFile)
tInput = [[None for x in range(3)] for y in range(len(trainingFile))] 

developmentFile = open('WSJ_24.pos', 'r').readlines()
dFeatureValues = [None]*len(developmentFile)
dInput = [[None for x in range(2)] for y in range(len(developmentFile))] 

#Training
for i in range(len(trainingFile)):
    fields = trainingFile[i].split('\t')
    if fields[0] == '\n': continue
    tInput[i][0] = fields[0]
    tInput[i][1] = fields[1]
    tInput[i][2] = fields[2] 
    
for i in range(len(tInput)):
    if tInput[i][0] == None:
        tFeatureValues[i] = '\n'
        continue
    token = tInput[i][0]
    pos = tInput[i][1]
    previousPOS = tInput[i-1][1]
    if previousPOS == None:
         previousPOS = 'None'
    previousWord = tInput[i-1][0]
    if previousWord == None:
        previousWord = 'None'
    nextPOS = 'None'
    nextWord = 'None'
    if i<len(tInput)-1:
        if tInput[i+1][1] != None:
            nextPOS = tInput[i+1][1]
        if tInput[i+1][0] != None:
            nextWord = tInput[i+1][0]
    uppercase = "F"
    if token[0].isupper():
        uppercase = "T"
    punctuation = "F"
    if token in string.punctuation:
        punctuation = "T"
    numeric = "F"
    if token.isnumeric():
        numeric = "T"
    bio = tInput[i][2]
    tFeatureValues[i] = token+"\tPOS="+pos+"\tpreviousPOS="+previousPOS\
        +"\tpreviousWord="+previousWord+"\tnextPOS="+nextPOS+"\tnextWord="\
            +nextWord+"\tisUpperCase="+uppercase+"\tisPunctuation="\
            +punctuation+"\tisNumeric="+numeric+"\tpreviousBIO=@@\t"+bio


#Development
for i in range(len(developmentFile)):
    fields = developmentFile[i].split('\t')
    if fields[0] == '\n': continue
    dInput[i][0] = fields[0]
    dInput[i][1] = fields[1][0:len(fields[1])-1]
    
for i in range(len(dInput)):
    if dInput[i][0] == None:
        dFeatureValues[i] = '\n'
        continue
    token = dInput[i][0]
    pos = dInput[i][1]
    previousPOS = dInput[i-1][1]
    if previousPOS == None:
        previousPOS = 'None'
    previousWord = dInput[i-1][0]
    if previousWord == None:
        previousWord = 'None'
    nextPOS = 'None'
    nextWord = 'None'
    if i<len(dInput)-1:
        if dInput[i+1][1] != None:
            nextPOS = dInput[i+1][1]
        if dInput[i+1][0] != None:
            nextWord = dInput[i+1][0]
    uppercase = "F"
    if token[0].isupper():
        uppercase = "T"
    punctuation = "F"
    if token in string.punctuation:
        punctuation = "T"
    numeric = "F"
    if token.isnumeric():
        numeric = "T"
    dFeatureValues[i] = token+"\tPOS="+pos+"\tpreviousPOS="+previousPOS\
        +"\tpreviousWord="+previousWord+"\tnextPOS="+nextPOS+"\tnextWord="\
            +nextWord+"\tisUpperCase="+uppercase+"\tisPunctuation="\
            +punctuation+"\tisNumeric="+numeric+"\tpreviousBIO=@@\n"
 
#Output
output = open("training.feature", "w")
for i in range(len(tFeatureValues)):
    output.write(tFeatureValues[i]) 
output.close()

output = open('test.feature', 'w')
for i in range(len(dFeatureValues)):
    output.write(dFeatureValues[i])
output.close()