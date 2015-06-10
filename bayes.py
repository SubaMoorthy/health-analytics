'''
Created on Apr 15, 2015
@author: Suba
'''
import sys
import json
import itertools

diseaseDict = {}
def parseInput():
    file  = open(sys.argv[2])
    startIndex =sys.argv[2].rfind('/') + 1
    endIndex = sys.argv[2].rfind('.txt')
    outputFile = open(sys.argv[2][startIndex:endIndex] + "_inference.txt", "w")
    numData  =  file.readline().split()
    numDisease = int(numData[0])
    numPatients = int(numData[1])
    patDetailsLen = numDisease * numPatients
    diseases = []
    currDisease = ""
    i = 1
    while i <  4*numDisease:
        basicInfo  = file.readline()
        data = basicInfo.split()
        currDisease = data[0]
        diseases.append(currDisease)
        PD = float(data[2])
        symptoms = eval(file.readline())
        symptomsPositive = eval(file.readline())
        symptomsNegative = eval(file.readline())
        diseaseDict[currDisease] = [PD, symptoms,symptomsPositive, symptomsNegative]
        i +=4

    while i < 4*numDisease + patDetailsLen:
        j = 1
        diseaseProbability = {}
        minMaxProbability = {}
        minMaxSymptoms = {}
        while j <= numDisease:
            patientData = eval(file.readline())
            diseaseData = diseaseDict[diseases[j-1]]
            PD = diseaseData[0]
            PND = 1 - PD
            symptoms = diseaseData[1]
            symptomsPositive = diseaseData[2]
            symptomsNegative = diseaseData[3]
            numerator = 1
            denominator1 = 1
            denominator2 = 1
            unknownIndices = []
            for k in range(0, len(patientData)  ):
                if patientData[k] == "T":
                    numerator *= float(symptomsPositive[k])
                    denominator1 *= float(symptomsPositive[k])
                    denominator2 *= float(symptomsNegative[k])
                if patientData[k] == "F":
                    numerator *= 1 - float(symptomsPositive[k])
                    denominator1 *=1 -  float(symptomsPositive[k])
                    denominator2 *= 1 - float(symptomsNegative[k])
                if patientData[k] == "U":
                    unknownIndices.append(k)
              
            bayesFormula = (numerator * PD ) / ( (denominator1 * PD) + (denominator2 * PND) )
            diseaseProbability[diseases[j-1]] =  '{:.4f}'.format(round(bayesFormula , 4)).__str__()
            binList = list(itertools.product([0, 1], repeat=len(unknownIndices)))
            minProb =  -1
            maxProb =  -1
            for bin in binList:
                currTuple = bin
                numerator_new =  numerator
                denominator1_new  =  denominator1
                denominator2_new= denominator2
                for x in range(0, len(unknownIndices)):
                    currSymptomIndex = unknownIndices[x]
                    if currTuple[x] == 1:
                        numerator_new *=  float(symptomsPositive[currSymptomIndex])
                        denominator1_new  *=  float(symptomsPositive[currSymptomIndex])
                        denominator2_new *=  float(symptomsNegative[currSymptomIndex])
                    if currTuple[x] == 0:
                        numerator_new *=   (1- float(symptomsPositive[currSymptomIndex]))
                        denominator1_new  *=   (1 - float(symptomsPositive[currSymptomIndex]))
                        denominator2_new *=  (1 - float(symptomsNegative[currSymptomIndex]))
                value =  (numerator_new * PD  ) / ( (denominator1_new * PD) + (denominator2_new * PND) )
                if minProb == -1 : 
                    minProb = value
                if maxProb == -1:
                    maxProb = value
                if minProb > value:
                    minProb = value
                if maxProb < value:
                    maxProb = value
            
            minMaxProbability[diseases[j-1]] =  ['{:.4f}'.format(round(minProb , 4)).__str__(), '{:.4f}'.format(round(maxProb , 4)).__str__()]        
            
            minProb =  -1
            maxProb =  -1
            minSymptom = ""
            minValue = ""
            maxSymptom = ""
            maxValue = ""
            for x in range(0, len(unknownIndices)):      
                numerator_new =  numerator
                denominator1_new  =  denominator1
                denominator2_new= denominator2
                currSymptom = unknownIndices[x] 
                #U is positive
                numerator_new *= float(symptomsPositive[currSymptom])
                denominator1_new  *=  float(symptomsPositive[currSymptom])
                denominator2_new *=  float(symptomsNegative[currSymptom])
                value =  (numerator_new * PD ) / ( (denominator1_new * PD) + (denominator2_new * PND) )
                
                if minProb == -1 : 
                    minProb = value
                    minValue = "T"
                    minSymptom = symptoms[currSymptom]
                if maxProb == -1:
                    maxProb = value
                    maxValue = "T" 
                    maxSymptom = symptoms[currSymptom]
                    
                if minProb == value:
                    if  symptoms[currSymptom] < minSymptom:
                        minProb = value
                        minValue = "T"
                        minSymptom = symptoms[currSymptom]
                    
                if minProb > value:
                    minProb = value
                    minValue = "T"
                    minSymptom = symptoms[currSymptom]
                    
                if maxProb == value:
                    if  symptoms[currSymptom] < maxSymptom:
                        maxProb = value
                        maxValue = "F" 
                        maxSymptom = symptoms[currSymptom]
                        
                if maxProb < value:
                    maxProb = value
                    maxValue = "T" 
                    maxSymptom = symptoms[currSymptom]
                    #U is negative
                numerator_new =  numerator * (1- float(symptomsPositive[currSymptom]))
                denominator1_new  =  denominator1 * (1 - float(symptomsPositive[currSymptom]))
                denominator2_new= denominator2 * (1 - float(symptomsNegative[currSymptom]))
                value =  (numerator_new * PD ) / ( (denominator1_new * PD) + (denominator2_new * PND) )
                if minProb == -1 : 
                    minProb =value
                    minValue = "F" 
                    minSymptom = symptoms[currSymptom]
                if maxProb == -1:
                    maxProb = value
                    maxValue = "F" 
                    maxSymptom = symptoms[currSymptom]
                if minProb == value:
                    if  symptoms[currSymptom] < minSymptom:
                        minProb = value
                        minValue = "T"
                        minSymptom = symptoms[currSymptom]
                if minProb > value:
                    minProb = value
                    minValue = "F" 
                    minSymptom = symptoms[currSymptom]
                    
                if maxProb == value:
                    if  symptoms[currSymptom] < maxSymptom:
                        maxProb = value
                        maxValue = "F" 
                        maxSymptom = symptoms[currSymptom]
                        
                if maxProb < value:
                    maxProb = value
                    maxValue = "F" 
                    maxSymptom = symptoms[currSymptom]
            if maxSymptom == "":
                maxSymptom = "none"
                maxValue = "N"     
            if minSymptom == "":
                minSymptom = "none"
                minValue = "N"
            minMaxSymptoms[diseases[j-1]] = [maxSymptom, maxValue, minSymptom, minValue]
            
            j+=1
        i +=numDisease 
        outputFile.write( "Patient-" + str( (i - (4 * numDisease)) / numDisease) + ":") 
        outputFile.write("\n")
        json.dump(diseaseProbability, outputFile)
        outputFile.write("\n")
        json.dump(minMaxProbability, outputFile)
        outputFile.write("\n")
        json.dump(minMaxSymptoms, outputFile)
        outputFile.write("\n")
        
        
if __name__ == '__main__':
    parseInput()