import re
text = "My email id is kulkarniprajwal.01@gmail.com!"

pat = re.compile(r'@.+\.\w+')
print(pat.findall(text))
