import util.TextProcessingUtil as tpu
import util.TextVerifyingUtil as tvu

while True:
    inputs = input("กรอกข้อความ: ")
    result = tpu.TextProcess(inputs)
    result = tvu.TextDictVerify(result)
    print(result)