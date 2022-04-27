#<import>
import pythainlp as pyth
try:
    from typing import List
except:
    pass
#</import>

#<define>
VOWELS = list(pyth.thai_vowels)
LETTERS = list(pyth.thai_consonants)
TONES = list(pyth.thai_tonemarks)
#</define>

#<function>
def isLead(vowel : str) -> bool: 
    return vowel in list(pyth.thai_lead_vowels)

def GetSyllables(text : str) -> List[str]:
    result = pyth.subword_tokenize(text, engine="ssg")
    return result

def GetPart(syl : str) -> List[dict]:
    result = []
    used_vowel = []
    for letter in syl:
        if (letter == "์"):
            index = syl.find(letter)
            syl = syl.replace(syl[index-1]+letter,"")
            continue
        if (letter == "็"):
            index = syl.find(letter)
            continue
        if (letter in TONES):
            syl = syl.replace(letter,"")
            continue
    for letter in syl:
        if (letter in VOWELS):
            used_vowel.append(letter)
    if ("รร" in syl[1:]):
        used_vowel.append("รร")
    print(f"Processed Syllable: {syl} \nUsed Vowels: {used_vowel} ({len(used_vowel)})")
    if (len(used_vowel) == 0):
        if("อ" in syl[1:]):
            used_vowel.append("อ")
            v_index = syl.rfind("อ")
            result.append({
                "init":syl[:v_index],
                "vowel":"อ",
                "final":syl[v_index+1:],
            })
        elif("ว" in syl[1:]):
            used_vowel.append("ว")
            v_index = syl.rfind("ว")
            result.append({
                "init":syl[:v_index],
                "vowel":"ัว",
                "final":syl[v_index+1:],
            })
        else:
            if(len(syl)==1):
                result.append({
                    "init":syl[0],
                    "vowel":"ะ",
                    "final":"",
                })
            elif(len(syl)==2):
                if(syl[1]=="ร"):
                    result.append({
                        "init":syl[0],
                        "vowel":"อ",
                        "final":syl[1],
                    })
                else:   
                    result.append({
                        "init":syl[0],
                        "vowel":"โ",
                        "final":syl[1],
                    })
            elif(len(syl)==3):
                if(syl[1] in ["ร","ล"]):
                    result.append({
                        "init":syl[:2],
                        "vowel":"โ",
                        "final":syl[2],
                    })
                elif(syl[0] in ['ห']):
                    result.append({
                        "init":syl[:2],
                        "vowel":"โ",
                        "final":syl[2],
                    })
                elif(syl[1] in ['ว']):
                    result.append({
                        "init":syl[0],
                        "vowel":"ัว",
                        "final":syl[2:],
                    })
                else:
                    if("ว" in syl[1:3]):
                        v_index = syl.find("ว")
                        result.append({
                            "init":syl[:v_index],
                            "vowel":"ัว",
                            "final":syl[v_index:],
                        })
                    else:
                        result += GetPart(syl[0])
                        result.append(
                            {
                            "init":syl[1],
                            "vowel":"โ",
                            "final":syl[2],
                            })
            else:
                print("Error: too many letters")
    elif (len(used_vowel) == 1):
        if (isLead(used_vowel[0])):
            if(used_vowel[0]==syl[0]):
                if (len(syl)==2):
                    result.append({
                        "init":syl[1],
                        "vowel":used_vowel[0],
                        "final":'',
                    })
                elif (len(syl)==3):
                    if (syl[2] == "อ"):
                        result.append({
                            "init":syl[1],
                            "vowel":used_vowel[0]+syl[2],
                            "final":'',
                        })
                    else:
                        result.append({
                            "init":syl[1],
                            "vowel":used_vowel[0],
                            "final":syl[2],
                        })
                elif (len(syl)==4):
                    if (syl[3] == "อ"):
                        result.append({
                            "init":syl[1:3],
                            "vowel":used_vowel[0]+syl[3],
                            "final":'',
                        })

                    elif (syl[2] in ["ร","ล","ว"]):
                        result.append({
                        "init":syl[1:3],
                        "vowel":used_vowel[0],
                        "final":syl[3:],
                        })

                    elif(syl[1] in ['ห']):
                        result.append({
                            "init":syl[1:3],
                            "vowel":used_vowel[0],
                            "final":syl[3:],
                        })
                    else:
                        result.append({
                            "init":syl[1],
                            "vowel":used_vowel[0],
                            "final":syl[2:],
                        })
                else:
                    print("Error: too many letters")   
            else:
                result+=GetPart(syl[0])
                result+=GetPart(syl[1:])
        else:
            v_index = syl.find(used_vowel[0])
            if (len(syl) >= 3):
                if ((used_vowel[0]=="ั") and (syl[v_index+1] == "ว")):
                    result.append({
                        "init":syl[:v_index],
                        "vowel":"ัว",
                        "final":syl[v_index+2:],
                    })
                elif(used_vowel[0]=="รร"):
                    result.append({
                        "init":syl[:v_index],
                        "vowel":"า",
                        "final":syl[v_index+2:],
                    })
                else:
                    result.append({
                        "init":syl[:v_index],
                        "vowel":used_vowel[0],
                        "final":syl[v_index+1:],
                    })
            else:
                result.append({
                    "init":syl[:v_index],
                    "vowel":used_vowel[0],
                    "final":syl[v_index+1:],
                })
    elif (len(used_vowel) == 2):
        if(set(used_vowel) in [set(["เ","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            if((v_index[1]-v_index[0] >= 2) and (syl[v_index[1]-1] == "อ")):
                result.append({
                    "init":syl[v_index[0]+1:v_index[1]-1],
                    "vowel":"เอ",
                    "final":syl[v_index[1]+1:],
                })
            else:
                result.append({
                    "init":syl[v_index[0]+1:v_index[1]],
                    "vowel":"เ",
                    "final":syl[v_index[1]+1:],
                })
        if(set(used_vowel) in [set(["แ","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            result.append({
                "init":syl[v_index[0]+1:v_index[1]],
                "vowel":"แ",
                "final":syl[v_index[1]+1:],
            })
        if(set(used_vowel) in [set(["โ","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            result.append({
                "init":syl[v_index[0]+1:v_index[1]],
                "vowel":"โ",
                "final":syl[v_index[1]+1:],
            })
        if(set(used_vowel) in [set(["เ","ิ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            result.append({
                "init":syl[v_index[0]+1:v_index[1]],
                "vowel":"เอ",
                "final":syl[v_index[1]+1:],
            })
        if(set(used_vowel) in [set(["เ","า"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            result.append({
                "init":syl[v_index[0]+1:v_index[1]],
                "vowel":"เา",
                "final":syl[v_index[1]+1:],
            })
        if(set(used_vowel) in [set(["เ","ี"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            if (syl[v_index[1]+1] == "ย"):
                result.append({
                    "init":syl[v_index[0]+1:v_index[1]],
                    "vowel":"เีย",
                    "final":syl[v_index[1]+2:],
                })
        if(set(used_vowel) in [set(["เ","ื"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            if(syl[v_index[1]+1] == "อ"):
                result.append({
                    "init":syl[v_index[0]+1:v_index[1]],
                    "vowel":"เือ",
                    "final":syl[v_index[1]+2:],
                })
        if(set(used_vowel) in [set(["ั","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1])])
            if(syl[v_index[1]-1] == "ว"):
                result.append({
                    "init":syl[:v_index[0]],
                    "vowel":"ัว",
                    "final":syl[v_index[1]:],
                })
    elif (len(used_vowel) == 3):  
        if(set(used_vowel) in [set(["เ","า","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1]),syl.find(used_vowel[2])])
            result.append({
                "init":syl[v_index[0]+1:v_index[1]],
                "vowel":"อ",
                "final":syl[v_index[2]+1:],
            })
        if(set(used_vowel) in [set(["เ","ี","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1]),syl.find(used_vowel[2])])
            if(syl[v_index[1]+1] == "ย"):
                result.append({
                    "init":syl[v_index[0]+1:v_index[1]],
                    "vowel":"เีย",
                    "final":syl[v_index[2]+3:],
                })
        if(set(used_vowel) in [set(["เ","ื","ะ"])]):
            v_index = sorted([syl.find(used_vowel[0]),syl.find(used_vowel[1]),syl.find(used_vowel[2])])
            if(syl[v_index[1]+1] == "อ"):
                result.append({
                    "init":syl[v_index[0]+1:v_index[1]],
                    "vowel":"เือ",
                    "final":syl[v_index[2]+3:],
                })
    else:
        print("ERROR: Too many vowels in a syllable")
    return result

def TextProcess(text : str) -> List[dict]:
    result = []
    syllables = GetSyllables(text=text)
    for syllable in syllables:
        result += GetPart(syl=syllable)
    return result
#</function>
