#<import>
import sys
sys.path.append("C:/Users/pitak/Desktop/DigitalHuman-Speak")
import script.util.TextProcessingUtil as tpu
try:
    from typing import List
except:
    pass
#</import>

#</define>
VERIFIED_INIT = []
VERIFIED_VOWEL = []
VERIFIED_FINAL = []
#</define>

def text_dict_verify(textDict : List[dict]) -> List[dict]:
    result = []
    for sylDict in textDict:
        i,v,f = (sylDict["init"],sylDict["vowel"],sylDict["final"])
        if True: #####
            print("Verifying: ",sylDict)
            result.append(sylDict)
    return result