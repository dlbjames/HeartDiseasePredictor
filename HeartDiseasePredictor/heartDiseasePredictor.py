#Darryl James TCSS 142
#Completion date: 11 March 2019

#Main function initalizes the files for input and output, the empty lists,
#and calls on other functions to get the final results
def main():
    inputFile = open("train.csv", "r")#Opens the input to train the code
    healthyCount = [0]*13             #Sets empty lists with elements of
    illCount = [0]*13                 #zero for counting
    healthyIllAccum = [0]*2
    setupCounters(inputFile, healthyCount, illCount, healthyIllAccum)
    #Calls the functions to perform
    #The calculations for the counters
    counts = getAverages(healthyCount, illCount, healthyIllAccum)        
    inputFile.close()
    inputFile = open("train.csv", "r") 
    diagCnt = getAccuracy(inputFile, counts, healthyIllAccum)
    #Calls a function that displays
    #the accuracy of the model
    inputFile.close()                                        
    inputFile = open("cleveland.csv", "r")
    outputFile = open("ClevelandDiag.csv", "w")
    writeDiagnosis(inputFile, outputFile, counts)
    inputFile.close()   #Closes the final input and 
    outputFile.close()  #output file for the program
    
def setupCounters(inputFile, healthyCount, illCount, healthyIllAccum):
    for line in inputFile:          #For every line in the inputfile
        names = line.split(',')     #1 is added to an empty list
                                    #(healthyIllAccum)
        if float(names[13]) < 1:    #If the 14th element less than one
            healthyIllAccum[0] += 1 #Otherwise, 1 is added to the other              
        elif float(names[13]) >= 1: #index of healthyIllAccum
            healthyIllAccum[1] += 1
        for index in range(len(healthyCount)):
            #For every index in the range of the lendth of the list
            #Add the float of that number at the index to that same
            #index in the list
            if names[index] != '?':
                if float(names[13]) < 1:           
            #If the element at the index is '?' that value becomes zero
            #If the element at the index is not added to the healthyCount list,
            #It is added to the illCount list instead   
                    healthyCount[index] += float(names[index])
                elif float(names[13]) >= 1:
                    illCount[index] += float(names[index])
    displayCounts(healthyIllAccum) #Calls the displayCounts Function

def displayCounts(healthyIllAccum):
    total = healthyIllAccum[0] + healthyIllAccum[1]
    #Calculates the total by adding the first and second elements
    #of healthyIllAccum which is then printed out
    print("Total Lines Processed: {}".format(total))            
    print("Total Healthy Count: {}".format(healthyIllAccum[0]))
    #Prints the total number of healthy patients
    print("Total Ill Count: {}".format(healthyIllAccum[1]))
    #Prints the total number of ill patients

def getAverages(healthyCount, illCount, healthyIllAccum):
    indexH = 0  #Sets empty lists and indexes all set to 0
    indexI = 0
    avgH = [0]*13    
    avgI = [0]*13
    #Every element in the healthyCount is divided by the number of
    #healthy patients to get the average value
    for el in healthyCount:
    #The index is incremented and the process continues
    #for the next elements
        avgH[indexH] += (float(healthyCount[indexH])/healthyIllAccum[0])
        indexH += 1
    for el in illCount:
    #Every element in the healthyCount is divided by the number of
    #healthy patients to get the average value
        avgI[indexI] += (float(illCount[indexI])/healthyIllAccum[1])
        indexI += 1 
    return getSepValues(avgH, avgI)
    #Calls the getSepValues function and returns the result
    
def getSepValues(avgH, avgI):
    #Gets the average values of the averages
    sep = [0]*13
    sepI = 0
    for el in avgH:
        #Take the float of the average values in the two lists,
        #add them together, divide by 2, increment the index, repeat
        sep[sepI] += (float(avgH[sepI]) + float(avgI[sepI]))/2  
        sepI += 1
    #Calls the displaysList function
    displayList(avgH, "Healthy Patient Averages: ")
    displayList(avgI, "Ill Patient Averages: ")
    displayList(sep, "Separation Values: ")
    return sep
        
def displayList(avg, message):
    index = 0
    print(message)
    #Prints the message that was passed.
    while index < len(avg):
    #Prints the numbers in the list passed
    #2 floating points on the same line.
        print("{:.2f}".format(avg[index]), end = "")
        if index != len(avg) -1 :
    #If the last index is reached do not print a comma on the line
            print(", ", end = "")                   
        index += 1
    print() #Print empty line 

def getAccuracy(inputFile, counts, hIA):
    #Counts is sep values
    #Creates an empty list of two elements set to 0
    tot = 0
    totl = 0
    for line in inputFile:
        lines = line.split(',')
        totl += 1
        attributes = lines[:13]
        myDiag = checkDiagnosis(attributes, counts)
        realDiag = 0
        if int(lines[13]) > 0:
            realDiag = 1
        if myDiag == realDiag:
            tot += 1
    acc = tot/totl
    print("Model Accuracy: {:.2f} or {:.0f}%".format(acc, acc*100))

def checkDiagnosis(attributes, counts):
    illCnt = 0
    index = 0
    for el in attributes:
        if el != "?" and float(el) > counts[index]:
            illCnt += 1
        index += 1
    return illCnt > 6

def writeDiagnosis(inputFile, outputFile, counts):
    test = open("test.csv", "w") #Testing file to write to in place of
    index = 0                    #in place the output file
    for line in inputFile:
        countI = 0
        lines = line.split(',')
        for index in range(len(counts)):
            if lines[index+1] != '?\n' and lines[index + 1] != '?':
                if counts[index] < float(lines[index+1]):
                    #Adds 1 to the count
                    countI += 1
        if countI > 6:
            ill = 1
            #If the ill count is 7 or more write a line to the
            #output file with id and a 1 for ill
            outputFile.write("{},{}\n".format(int(lines[0]), ill))
        else:
            healthy = 0
            outputFile.write("{},{}\n".format(int(lines[0]), healthy))
            #Write a line to the output file
            #with id and a 0 for healthy
main()
