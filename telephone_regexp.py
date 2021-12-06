import sys
import re

value = r'(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?'
pattern = re.compile(value)

output = open("telephone_output.txt", "w")

for i, line in enumerate(open(sys.argv[1])):
    for match in re.finditer(pattern, line):
        output.write(str(match.group())+"\n")
        
output.close()