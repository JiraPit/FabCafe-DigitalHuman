import sys
sys.path.append("C:/Users/pitak/Desktop/DigitalHuman-Speak")
import script.util.TextProcessingUtil as tpu
import script.util.TextVerifyingUtil as tvu

while True:
    inputs = input("กรอกข้อความ: ")
    result = tpu.text_process(inputs)
    print(result)