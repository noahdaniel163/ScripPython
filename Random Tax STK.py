import random

# generate a random sequence of numbers with length 10
sequence = ''.join(random.choices('0123456789', k=10))

# encode the sequence within the XML tags
xml_string = f'<SOHIEU_TK>{sequence}</SOHIEU_TK>'

print(xml_string)
