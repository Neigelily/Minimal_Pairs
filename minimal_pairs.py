#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:09:05 2020

@author: Neige Rochant
"""

import re, os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(__file__)

# Automatic message when starting the script
print("\n\nWelcome to the Python script Minimal_Pairs created by Neige Rochant. This script provides 2 functions:\n")
print("1) extractLexemesFromLiftFile(liftFile, dialect ='')\n")
print("2) generateSetsOfMinimalPairs(listOfLexemes, setOfVowels = '<default set of IPA vowel characters>', setOfConsonants = '<default set of IPA consonant characters>', setOfTones = '<default set of IPA tone characters>')\n")
print("Example of use of the two functions together: generateSetsOfMinimalPairs(extractLexemesFromLiftFile('Minimal_Pairs.lift', 'M'bottiny'), 'aæeəɛiɪoɔuʊʌɜ', 'ptkbdgqβɸɣrxχʁlnmjɲŋɴɢhywfvˠɾycsʸʙ', '́̄̀̂̌')")
print("WARNING: the output file 'minimalPairs.txt' of function 'generateSetsOfMinimalPairs' is overwritten everytime you run the function. To save the output file, copy it in another directory or rename it.\n")
print("For details, type: help()")

# Optional instruction message if you type help()
def help() :
    print("1) Function 'extractLexemesFromLiftFile(liftFile, dialect ='')' generates a list containing all the lexemes found in a LIFT file, e.g. exported from a lexicon in the FieldWorks Explorer software (LIFT files are written in XML).\n")
    print("\t– This function takes the name of the LIFT file as its single mandatory argument. In case your FieldWorks lexicon deals with several dialect labels, the function takes the name of the dialect you want to extract lexemes from as its second, optional argument.\n")
    print("\t– To use this function, place your LIFT file in the same directory as this Python script, and type in your terminal: extractLexemesFromLiftFile('<name of your LIFT file>.lift', '<name of the dialect you want to extract minimal pairs from>')', or just: extractLexemesFromLiftFile('<name of your LIFT file>')\n")
    print("2) Function 'generateSetsOfMinimalPairs(listOfLexemes, setOfVowels = '<default set of IPA vowel characters>', setOfConsonants = '<default set of IPA consonant characters>', setOfTones = '<default set of IPA tone characters>')' generates a TXT file containg all the minimal pairs found in the Python list of lexemes that you passed as argument. The minimal pairs are classified as vocalic, consonantal and tonal. A fourth list contains mixed pairs and pairs comprising an unrecognized character. To classify minimal pairs, the function uses default sets of IPA vowels, consonants and tones.\n")
    print("\t– This function takes the name of the list containg your lexemes as its single mandatory argument. It also takes strings containing your personal sets of vowels, consonants and tones (in that order) as three optional arguments, in case your lexicon contains characters that are not in the default sets, or if you use a vowel character as a consonant (e.g. y).\n")
    print("\t– To use this function, you need to create a Python list containing all your lexemes. This list can be generated from a LIFT file using function 'extractLexemesFromLiftFile' provided by this script. If your lexicon is stored in a file with another extension, you need to extract the lexemes from it by your own means.\n") 
    print("\t– In your terminal, type: generateSetsOfMinimalPairs(<name of your Python list of lexemes>) or generateSetsOfMinimalPairs(<name of your Python list of lexemes>, '<set of vowels of your language>', '<set of consonants of your language>', '<set of tones of your language>'). If you have a LIFT file (in the same directory as this script), you can extract the list of lexemes at the same time as you generate the minimal pairs by writing : generateSetsOfMinimalPairs(extractLexemesFromLiftFile('<name of your LIFT file>.lift') as the first argument of the function.\n")
    print("\tA TXT file containing all the minimal pairs will be created in the same directory as this Python script.\n")




# Replace special characters by their XML equivalent (to be used for the argument 'dialect' in Function extractLexemesFromLiftFile))
def replaceSpecialCharactersbyXML(string) :
    XMLfriendlyString = string.replace("&", "&amp;").replace("'", "&apos;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    return XMLfriendlyString



# Function 1: extract a list of all lexemes from a LIFT lexicon file
def extractLexemesFromLiftFile(liftFile, dialect="") : # the argument 'dialect' is to be used if your LIFT lexicon contains several dialect labels. You need to select one of the dialects to extract lexemes from.
    
    # 1 – Read the lexicon file
    global dir_path
    file=open(dir_path+"/"+liftFile, "r")
    contents =file.read()
    
    regexEntries = r'<\s*entry.*?>(?:.|\s)*?</\s*entry\s*>' # identify each entry
    regexDialect = r'<\s*trait\s*name\s*=\s*"dialect-labels"\s*value\s*=\s*"'+replaceSpecialCharactersbyXML(dialect)+'"\s*/>' # identify each entry by dialect
    regexLexemeForms = r'<\s*lexical-unit.*?>\s*<\s*form.*?>\s*<\s*text.*?>(.*?)</\s*text\s*>\s*</\s*form\s*>(?:.|\s)*?</\s*lexical-unit\s*>' # Identify the lexical unit of each entry

    # Extract all entries :
    listOfEntries = re.findall(regexEntries, contents)

    listLexemes = []

    # Extract lexemes from all entries (or only lexemes of entries in the target dialect, if a dialect is passed as argument)
    for entry in listOfEntries :
        lexeme = re.search(regexLexemeForms, entry)
        match = re.search(regexDialect, entry) # check if the entry is in the target dialect (passed as argument)
        if lexeme:
            if match or (dialect == ""):
                listLexemes.append(lexeme.group(1))
                
    return (listLexemes) 
            
          

vocalicMinimalPairs = []
consonantalMinimalPairs = []
tonalMinimalPairs = []
otherMinimalPairs = []
consonants = ""
vowels = ""
tones = ""
unrecognizedCharacters = []


# Remove tones from a word (to be called in Function analyzeNewPair, in order to include near-minimal pairs (minimal pairs which also have one or different tones) in minimal pairs)
def removeTones(word) :
    tonalValue = "" # tonalValue keeps track of the tones which have been removed
    tonelessWord = ""
    for i in range(0, len(word)):
        if word[i] in tones:
            tonalValue = tonalValue[:-1] + word[i]
        else:
            tonalValue += "0"
            tonelessWord += word[i]         
    return (tonelessWord, tonalValue) 

# Check if a pair of lexemes is a minimal pair (segmental or tonal) or a (segmental) near-minimal pair. To be called in functions treatANewMinimalPair and chechWhichMinimalPair.
def analyzeNewPair(x, y) :
    (tonelessx, tonalValuex) = removeTones(x)
    (tonelessy, tonalValuey) = removeTones(y)
    numberOfDifferentSegmentalSigns = 0
    numberOfDistinctiveDifferentTones = 0
    lastSegmentalDifferentSigns = []
    if len(tonelessx) == len(tonelessy):
        for i in range(0, len(tonelessy)) :         
            if tonelessx[i] != tonelessy[i] :
                numberOfDifferentSegmentalSigns += 1
                lastSegmentalDifferentSigns = [tonelessx[i], tonelessy[i]]
            else:
                if tonalValuex[i] !=tonalValuey[i]:
                    numberOfDistinctiveDifferentTones += 1                  
        return (numberOfDifferentSegmentalSigns, numberOfDistinctiveDifferentTones, lastSegmentalDifferentSigns)
    else:
        return (-1, -1, "")

# Check which member(s) of a pair of lexemes exist in a list of lexemes. To be called in function treatANewMinimalPair in order to avoid doublets in the final list of minimal pairs, and merge all sister minimal pairs (e.g. ["bla", "bli"], ["bli", "bla] and ["bli", "blo"]) together in the same "pair" ["bla", "bli", "blo"]
def whichCoupleeIsNotInList(liste, couple) :
    if couple[0] in liste and couple[1] not in liste:
        return 1
    elif couple[1] in liste and couple[0] not in liste:
        return 0
    elif couple[0] in liste and couple[1] in liste:
        return "none"
    else :
        return "all"
    
# Decide what to do with a minimal pair with respect to the list of minimal pairs passed as argument : add it to the list if it's new, merge it with an existent minimal pair if only one of its members is new (and forms a minimal pair with the existent pair), or do nothing if the minimal pair already exists in the list in a different order. To be called in function checkWhichMinimalPair.
def treatANewMinimalPair(setOfMinimalPairs, newCouple) :
    addNewCoupleInSet = True
    for paire in setOfMinimalPairs:
        coupleeNotInList = whichCoupleeIsNotInList(paire, newCouple)
        if isinstance(coupleeNotInList, int) == True :           
            matchesWithExistingPair = 0
            for i in range(0, len(paire)):
                (numberOfDifferentSegmentalSigns, numberOfDistinctiveDifferentTones, lastSegmentalDifferentSign) = analyzeNewPair(newCouple[coupleeNotInList], paire[i])
                if numberOfDifferentSegmentalSigns == 1 or (numberOfDifferentSegmentalSigns == 0 and numberOfDistinctiveDifferentTones > 0):
                    matchesWithExistingPair += 1
            if matchesWithExistingPair == len(paire):
                addNewCoupleInSet = False
                paire.append(newCouple[coupleeNotInList])
        if coupleeNotInList == "none":
            addNewCoupleInSet = False
    if addNewCoupleInSet == True:
        setOfMinimalPairs.append(newCouple)
            
# Put minimal pairs in relevant lists (vocalic, consonantal, tonal, others (= trash)). To be called in Function 2: generateSetsOfMinimalPairs.
def checkWhichMinimalPair(lexeme1, lexeme2) :
    numberOfDifferentSegmentalSigns, numberOfDistinctiveDifferentTones, lastSegmentalDifferentSigns = analyzeNewPair(lexeme1, lexeme2)
    if numberOfDifferentSegmentalSigns == 1:
        if lastSegmentalDifferentSigns[0] in vowels and lastSegmentalDifferentSigns[1] in vowels:
            treatANewMinimalPair(vocalicMinimalPairs, [lexeme1, lexeme2])   
        elif lastSegmentalDifferentSigns[0] in consonants and lastSegmentalDifferentSigns[1] in consonants :
            treatANewMinimalPair(consonantalMinimalPairs, [lexeme1, lexeme2])
        else:
            for unrecognizedCharacter in lastSegmentalDifferentSigns:
                if not unrecognizedCharacter in vowels and not unrecognizedCharacter in consonants :
                    if not unrecognizedCharacter in unrecognizedCharacters :
                        unrecognizedCharacters.append(unrecognizedCharacter)
            treatANewMinimalPair(otherMinimalPairs, [lexeme1, lexeme2])  
    elif numberOfDifferentSegmentalSigns == 0 and numberOfDistinctiveDifferentTones > 0 :
        treatANewMinimalPair(tonalMinimalPairs, [lexeme1, lexeme2])               

# Pretreat every lexeme of your list by replacing uppercases by lowercases and single characters containing a tone (which messe up with the analysis of the pair) by 1 vowel character + 1 tone character. To be used in Function 2 : generateSetsOfMinimalPairs.    
def normalize(listOfLexemes) :
    listOfNormalizedLexemes = []
    charactersToReplace = "àáâāǎȁǽǣèéêēěȅìíîīǐȉòóôōőǒȍǿùúûūűǔȕ"
    charactersWithTones = "àáâāǎȁœ́œ̄èéêēěȅìíîīǐȉòóôōőǒȍǿùúûūűǔȕ"
    for item in listOfLexemes:
        lexeme = item.lower()
        for i in range(0, len(charactersToReplace)) :
            lexeme = lexeme.replace(charactersToReplace[i], charactersWithTones[i*2:i*2+2])
        listOfNormalizedLexemes.append(lexeme)       
    return(listOfNormalizedLexemes)  
        

# Function 2 : generates sets of minimal pairs classified by phonological nature (consonantal, vocalic, tonal) from a list of lexemes passed as argument. You can pass sets of vowels, consonants and tones as optional arguments, if the default sets (used to decide the phonological nature of a minimal pair) do not fit your language.
def generateSetsOfMinimalPairs(listOfLexemes, setOfVowels = "aɑɐɒæeɛɜəɤiɪɨıuʉʊʌʏɯɞʚᴀᴁᴂᴇᴈᴏoᴐɔᴑᴒᴓᴔᶏᶐᶒᶓᶔᶕᶖᶗŒɵøœɶˑːɩɷᴕᴜᴝᴞᵫI", setOfConsonants = "bʙɓβcçƈɕdðɗɖfɡɢɠʛɣhʜɦħʰˠɧjɟʝʄᴊʲkƙlʟɬɭɮɫˡmɰnɴŋɲɳⁿpƥɸqʠrɹʀʁɾɽɺɻsʃʂtθƭʈvʋwʍʷxχʎɥzʒʐʑʔʡʕʢˤǃʘǀǁǂčʗđʤȡɘɚɝƕʱǰʞλƛƞȵƪϸπɼɿʵʳσʴʶšʆˢʇʧȶʮʯžƺʓƻʖʅƫʦʣʨʩʪʫʥʬʭˣʼ̊ᴃᴄᴅᴆᴉᴋᴌᴍᴎᴘᴙᴚᴛᴟᴠᴡᴢᴣᴤBGƓγHLNR!ᶀᶁᶂᶃᶄᶅᶆᶇᶈᶉᶊᶋᶌᶍᶎᶑᶘᶙᶚyʸY", setOfTones = "̋̏́̄̀̌̂᷄᷅᷈᷆᷇") :
    global vowels, consonants, tones
    vowels = setOfVowels
    consonants = setOfConsonants
    tones = setOfTones
    listOfNormalizedLexemes = normalize(listOfLexemes)
    for i in range(0, len(listOfNormalizedLexemes)):      
        for j in range(i, len(listOfNormalizedLexemes)):
            checkWhichMinimalPair(listOfNormalizedLexemes[i], listOfNormalizedLexemes[j])
    f = open(os.getcwd()+"/"+"minimalPairs.txt","w+")
    f.write("Vocalic minimal pairs:\n\n")
    for vocalicMinimalPair in vocalicMinimalPairs :
        for i in range(0, len(vocalicMinimalPair)) :
            f.write(vocalicMinimalPair[i])
            if i < len(vocalicMinimalPair)-1:
                f.write(", ")
            if i == len(vocalicMinimalPair)-1:
                f.write(".")
        f.write("\n")
    f.write("\n\nConsonantal minimal pairs:\n\n")
    for consonantalMinimalPair in consonantalMinimalPairs :
        for item in consonantalMinimalPair :
            f.write(item+", ")
        f.write("\n")
    f.write("\n\nTonal minimal pairs:\n\n")
    for tonalMinimalPair in tonalMinimalPairs :
        for item in tonalMinimalPair :
            f.write(item+", ")
        f.write("\n")
    f.write("\n\nOther pairs (mixed pairs and pairs involving unrecognized characters):\n\n")
    for otherMinimalPair in otherMinimalPairs :
        for item in otherMinimalPair :
            f.write(item+", ")
        f.write("\n") 
    f.close()    
    print("The following characters could not be recognized :")
    print(unrecognizedCharacters)
    print("Consequently, minimal pairs involving one of these characters have been placed in the list 'Other pairs'.")        
       
           
