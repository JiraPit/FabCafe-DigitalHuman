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

def TextDictVerify(textDict : dict) -> List[dict]:
    result = []
    for sylDict in textDict:
        i,v,f = (sylDict["init"],sylDict["vowel"],sylDict["final"])
        if True: #####
            result.append(sylDict)
    return result