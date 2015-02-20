import re

my_file = open('./surnames.txt')
text = my_file.read()


names = []
# for line in text:
#     result = re.search(r'<b>(\w+)</b>', line)
#     if result:
#         names.append(result.group(0))
#         
search = re.findall(r'<td>(P\w+)</td>', text)
title_cased = [name.title() for name in search]
print title_cased