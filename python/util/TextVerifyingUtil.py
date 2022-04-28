#<import>
import util.TextProcessingUtil as tpu
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

def TextDictVerify(textDict : List[dict]) -> List[dict]:
    result = []
    for sylDict in textDict:
        i,v,f = (sylDict["init"],sylDict["vowel"],sylDict["final"])
        if True: #####
            print("Verifying: ",sylDict)
            result.append(sylDict)
    return result