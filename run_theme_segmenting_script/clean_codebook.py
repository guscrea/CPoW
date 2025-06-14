# this script deletes the examples in the codebook #

import re
import os

with open('themes_list.txt') as f:
    txt = f.readlines()
    f.close()

acc_str = ""
for line in txt:
    acc_str += line

txt = acc_str

txt = re.sub(r'\* Examples.*?________________', " \n________________", txt, flags=re.DOTALL)

print(txt)