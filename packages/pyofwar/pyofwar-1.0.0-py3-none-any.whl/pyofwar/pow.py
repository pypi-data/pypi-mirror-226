import random
from .quote_list import artofwar

def quote(n, quotation_marks = False):

    output = artofwar[n-1]
    
    if quotation_marks == True:
        output = f'"{output}"'
        
    return output

def quote_random(n=1, quotation_marks=False, start=0, end=371):

    quotes = []

    for i in range(n):
        random_index = random.choice(range(start, end+1))
        output = artofwar[random_index]

        if quotation_marks == True:
            output = (f'"{output}"')

        quotes.append(output)

    return ("\n".join(quotes))