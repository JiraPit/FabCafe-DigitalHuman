import os
os.chdir("C:/Users/pitak/Desktop/DigitalHuman-Speak")
import script.util.TextProcessingUtil as tpu
import script.util.TextVerifyingUtil as tvu

while True:
    inputs = input("กรอกข้อความ: ")
    result = tpu.text_process(inputs)
    result = tvu.text_dict_verify(result)
    print(result)