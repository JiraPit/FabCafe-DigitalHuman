import sys
sys.path.append("E:\Data\Jira02\Assets\Python\DigitalHuman-Speak")
import script.util.TextProcessingUtil as tpu
import script.util.TextVerifyingUtil as tvu

while True:
    inputs = input("กรอกข้อความ: ")
    result = tpu.text_process(inputs)
    print(result)