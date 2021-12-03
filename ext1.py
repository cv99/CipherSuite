alphabet = 'abcdefghijklmnopqrstuvwxyz'


def ioc(text: str):
    """Calculates the Index of Coincidence for the text argument."""
    try:
        return sum([text.upper().count(letter) * (text.upper().count(letter) - 1) for letter in alphabet.upper()]) / \
               (len(text) * (len(text) - 1) / len(alphabet))
    except ZeroDivisionError:
        return 'N/A'


def generalIntelligence(strippedText):
    result = ioc(strippedText)
    print('Index of Coincidence:', result)
    if result > 0.055:
        print('IoC high, treating as simple substitution or transposition:')
    else:
        print('Treating as polysubstitution')
