# Minimal_Pairs

This Python script provides 2 independent functions:

1) Function 'extractLexemesFromLiftFile(liftFile, dialect ='')' generates a list containing all the lexemes found in a LIFT file, e.g. exported from a lexicon in the FieldWorks Explorer software (LIFT files are written in XML).
- This function takes the name of the LIFT file as its single mandatory argument. In case your FieldWorks lexicon deals with several dialect labels and you want to generate seperate lists of lexemes for each dialect, the function takes the name of the dialect you want to extract lexemes from as its second, optional argument.
– To use this function, place your LIFT file in the same directory as this Python script, and type in your terminal: extractLexemesFromLiftFile('<name of your LIFT file>.lift', '<name of the dialect you want to extract minimal pairs from>')', or just: extractLexemesFromLiftFile('<name of your LIFT file>')


2) Function 'generateSetsOfMinimalPairs(listOfLexemes, setOfVowels = '<default set of IPA vowel characters>', setOfConsonants = '<default set of IPA consonant characters>', setOfTones = '<default set of IPA tone characters>')' generates a TXT file containg all the minimal pairs found in the Python list of lexemes that you passed as argument. The minimal pairs are classified as vocalic, consonantal and tonal. A fourth list contains mixed pairs and pairs comprising an unrecognized character. To classify minimal pairs, the function uses default sets of IPA vowels, consonants and tones.

– This function takes the name of the list containg your lexemes as its single mandatory argument. It also takes strings containing your personal sets of vowels, consonants and tones (in that order) as three optional arguments, in case your lexicon contains characters that are not in the default sets, or if you use a vowel character as a consonant (e.g. y).

– To use this function, you need to create a Python list containing all your lexemes. This list can be generated from a LIFT file using function 'extractLexemesFromLiftFile' provided by this script. If your lexicon is stored in a file with another extension, you need to extract the lexemes from it by your own means.

– In your terminal, type: generateSetsOfMinimalPairs(<name of your Python list of lexemes>) or generateSetsOfMinimalPairs(<name of your Python list of lexemes>, '<set of vowels of your language>', '<set of consonants of your language>', '<set of tones of your language>'). If you have a LIFT file (in the same directory as this script), you can extract the list of lexemes at the same time as you generate the minimal pairs by writing : generateSetsOfMinimalPairs(extractLexemesFromLiftFile('<name of your LIFT file>.lift') as the first argument of the function.

A TXT file containing all the minimal pairs will be created in the same directory as this Python script.


Example of use of the two functions together: generateSetsOfMinimalPairs(extractLexemesFromLiftFile('Minimal_Pairs.lift', 'M'bottiny'), 'aæeəɛiɪoɔuʊʌɜ', 'ptkbdgqβɸɣrxχʁlnmjɲŋɴɢhywfvˠɾycsʸʙ', '́̄̀̂̌')
WARNING: the output file 'minimalPairs.txt' of function 'generateSetsOfMinimalPairs' is overwritten everytime you run the function. To save the output file, copy it in another directory or rename it.








