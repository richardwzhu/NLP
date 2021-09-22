
import sys
import re

numbers = '\$?((one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|(ten))'
metrics = '(\shundred)|(\sthousand)|(\smillion)'
regex = r'\$[0-9\.,]+'+'(\sdollars)?|('+numbers+'('+metrics+')?(\sdollars))'

pattern = re.compile(regex)

output = open("dollar_output.txt", "w")

for i, line in enumerate(open(sys.argv[1])):
    for match in re.finditer(pattern, line):
        output.write(str(match.group())+"\n")
        
output.close()