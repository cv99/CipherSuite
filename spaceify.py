import random

text = 'thebombingraidonvemorkwascarriedoutduringdaylightonnovembersixteenththeattacksquadronconsistingofthirteenplanessplitintotwogroupseachmakingtworunsonthetargetswhichappearedtobethenorskhydropowerstationandthenitrateplantthreemilestotheeasttheattackwasnotforeseennorwasitinterceptedbyaircoverandalloftheattackingaircraftseemtohavereturnedfromthemissioneyewitnessesstatethatintermittentcloudcoverappearedtodisrupttheattackbutthemajorityoftheexplosivesaroundthirtytonsweredroppedwithveryhighaccuracyonthenitrateplantonlytwotothreetonshitthepowerstationandthereinforcedstructurewithstoodtheworstoftheassaultthebombsfailedtodamagetherebuiltdeuteriumelectrolysisfacilityandournewstocksofheavywaterwereprotectedbythesevenstoreysofreinforcedconcreteabovehoweverthepowerplantitselfhasbeendamagedandthissecondraidontheplantraisesthepossibilitythatourenemieshaveagentsworkingwithinitindiscussionwithofficialsfromdiealchemistengroupithasbeendecidedthatthefacilityshouldbeshutdownexistingstocksofheavywaterandpotassiumhydroxidewillbeshippedtotheirlaboratoriesandmanufacturingfacilitiesingermanyforfurtherenrichmentandexperimentationgiventheriskoflocalespionagewewillneedtosignificantlyenhancesecurityforthisoperationfinallyweshouldnotethattheattackkilledtwentyonenorwegianciviliansthisisvaluablepropagandaandouragentsaredoingtheirbesthereandinlondontoensurethatthenorwegianpopulationunderstandswhoistoblamefortheseneedlessdeaths'


def permute(textIn: str, _changes_min=1, _changes_max=10, _max_move_distance=10):
    # _ means variable is temp and shouldn't be referenced outside this function

    # Count Spaces
    _spaces = 0
    _space_at = []
    for i in range(len(textIn)):
        if textIn[i] == ' ':
            _space_at.append(i)
            _spaces += 1

    # Number of spaces to move
    _moving = random.randrange(_changes_min, _changes_max)

    # Get rid of all spaces
    _newtext = ''
    for c in textIn:
        if c != ' ':
            _newtext += c

    # Make a list of the spaces we'll actually move
    _spaces_to_move = []
    for i in range(_moving):
        _space_place = random.randrange(0, len(_space_at))
        _spaces_to_move.append(_space_at[_space_place])
        _space_at.pop(_space_place)

    # Alter the positions of the spaces in the list
    for i in range(len(_spaces_to_move)):
        _spaces_to_move[i] = _spaces_to_move[i] + random.randrange(-_max_move_distance, _max_move_distance)

    # Perform checks before adding
    _passed = True
    for i in range(len(_spaces_to_move)):
        # Space on the edge check
        if _spaces_to_move[i] == 0 or _spaces_to_move[i] == len(_newtext):
            _passed = False
        for x in range(len(_spaces_to_move)):
            # Two spaces in the same space check
            if _spaces_to_move[i] == _spaces_to_move[x] and i != x:
                _passed = False
            # Two spaces next to each other
            if _spaces_to_move[i] == _spaces_to_move[x] + 1 or _spaces_to_move[i] == _spaces_to_move[x] - 1:
                _passed = False

    # Add in spaces
    for i in range(len(_space_at)):
        _newtext = _newtext[:_space_at[i]] + ' ' + _newtext[_space_at[i]:]
    for i in range(len(_spaces_to_move)):
        _newtext = _newtext[:_spaces_to_move[i]] + ' ' + _newtext[_spaces_to_move[i]:]

    # Final checks
    # Spaces Next to each other
    for i in range(len(_newtext) - 1):
        if _newtext[i] == _newtext[i + 1] == ' ':
            _passed = False
    # Spaces at ends
    if _newtext[0] == ' ' or _newtext[len(_newtext) - 1] == ' ':
        _passed = False

    # Passed?
    if True:  # if _passed:
        # Return text
        return _newtext
    else:
        # Try the whole thing again
        return permute(textIn, _changes_min=_changes_min, _changes_max=_changes_max,
                       _max_move_distance=_max_move_distance)


words = {}
with open('20k.txt', 'r') as f:
    for n, x in enumerate(f.readlines()):
        if not len(x[:-1]) == 1:
            words[x[:-1]] = 1000 * 1 / (n + 1) + (len(x[:-1]) * 2)


def score(potentialWord):
    if potentialWord in words:
        return words[potentialWord] + len(potentialWord)
    else:
        return 0 + len(potentialWord)


def initialAdd():
    blockSize = len(text) // noOfSpaces
    endOfBlocks = blockSize * noOfSpaces
    return ' '.join([text[y:y + blockSize] for y in range(0, endOfBlocks, blockSize)]) + text[endOfBlocks:]


def scoreText(t):
    return sum([score(word) for word in t.split(' ')])  # len(text.split(' ')


populationSize = 100
noOfSpaces = 280
text = initialAdd()
print(text)

population = [text for _ in range(populationSize // 2)]
running = True
generationCount = 0
try:
    while running:
        population += [permute(x) for x in population]
        population = sorted(population, key=scoreText, reverse=True)[:populationSize]

        print('Gen', generationCount, 'best score:', str(scoreText(population[0]))[:5], population[0][:90])

        generationCount += 1
except KeyboardInterrupt:
    print(population[0])
