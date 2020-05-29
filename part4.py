from part5 import *
import statistics
import math
import random
import time


class Message:
    """Contains message information, both visual and back-end."""

    def __init__(self, text: str, x=10, y=70):
        self.rawText = ''.join(
            [x for x in text.replace('\n', ' ') if x.lower() in alphabet or x in otherAllowedChars + list(numbers)])
        self.x = x
        self.y = y
        self.width = 600
        self.height = 450
        self.displayScroll = -5
        self.displayText = []
        self.displayMask = []
        self.freqAnalysis = []
        self.canRedo = -1
        self.rawTextDataBase = [self.rawText]

        self.grid = []
        self.gridMask = []
        self.colDragging = False
        self.startDragColumn = 0
        self.hasDragHistory = False
        self.dragHistory = None
        self.colDragRel = 0
        self.colDragStart = 0

        self.rendUpdate()
        self.freqObjectLink = None
        self.trigObjectLink = None
        self.allowMouseCheck = None
        self.trigramAnalysis = []
        self.basicAnalysis(VC)

    def affine(self, obj):
        """Applies a frequency-based affine solve on the selected letters. Returns lowercase."""
        obj.touch = None
        roll = self.operationText().lower().replace(VC.BlankLetter, '')
        results = []
        for a in range(0, 26):
            for b in range(26):
                if a not in [0, 2, 13]:
                    letter_map = dict(((alphabet[l_num], alphabet[(a * l_num + b) % 26]) for l_num in range(26)))
                    t = ''.join([letter_map[letter] for letter in roll])
                    frequencies = [t.count(letter) for letter in alphabet]
                    score_single = sum([sortedELF[l_num] * frequencies[l_num] for l_num in range(26)])
                    results.append([[a, b], score_single])
        results = sorted(results, key=(lambda z: -z[1]))
        a, b = results[0][0]
        letter_map = dict(((alphabet[l_num], alphabet[(a * l_num + b) % 26]) for l_num in range(26)))
        o = ''
        shield = self.operationText()
        for n, x in enumerate(self.rawText):
            if shield[n] == VC.BlankLetter:
                o += x
            else:
                o += letter_map[x.lower()]
        self.resetRawText(o)
        print('Affine cipher solve completed on selected text using a, b:', alphabet[a].upper(), alphabet[b].upper())

    def basicAnalysis(self, obj):
        """Calculates frequency and trigram analysis for the selected letters."""
        obj.touch = None
        x = self.operationText().upper().replace(VC.BlankLetter, '')
        self.freqAnalysis = {}
        for letter in alphabet + alphabet.upper():
            self.freqAnalysis[letter] = x.count(letter)
        self.freqAnalysis = [[x, self.freqAnalysis[x]] for x in list(self.freqAnalysis)]
        self.freqAnalysis.sort(key=(lambda z: -z[1]))

        for n, a in enumerate(self.freqAnalysis):
            a[1] = str(((a[1] * 1000) // len(x)) / 10) + '%'

        try:
            self.freqObjectLink.render()
        except AttributeError:
            pass

        x = self.operationText().upper().replace(' ', '')
        trigrams = {}
        for i, l in enumerate(x):
            if i < len(x) - 2:
                try:
                    trigrams[x[i:i + 3]] += 1
                except KeyError:
                    trigrams[x[i:i + 3]] = 1
        self.trigramAnalysis = [[j, trigrams[j]] for j in list(trigrams) if trigrams[j] > 1]
        self.trigramAnalysis.sort(key=(lambda z: -z[1]))

        for n, a in enumerate(self.trigramAnalysis):
            a[1] = str(((a[1] * 10000) // len(self.rawText)) / 100) + '%'

        try:
            self.trigObjectLink.render()
        except AttributeError:
            pass

        try:
            VC.doColumnVis(VC.columnarIocPanel)
        except TypeError:
            pass

    def caesar(self, obj):
        """Calculates a frequency-based caesar solve for the selected letters. No E-preference."""
        obj.touch = None
        roll = self.operationText().upper()
        frequencies = [roll.count(letter.upper()) for letter in alphabet]
        results = [int(sum([frequencies[(s + b) % 26] * sortedELF[b] for b in range(26)])) for s in range(26)]
        shift = results.index(max(results))
        o = ''
        for n, x in enumerate(roll):
            if x == VC.BlankLetter:
                o += self.rawText[n]
            else:
                o += alphabet[(alphabet.find(x.lower()) - shift) % 26]
        self.resetRawText(o)
        print('Caesar completed with key: ', alphabet[shift % 26].upper())

    def check_click(self, pos: tuple):
        """Standard - various effects for the start of a click."""
        if self.x < pos[0] < self.x + self.width:
            if self.y + 70 < pos[1] < self.y + 70 + self.height:
                if not (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                    r = True
                    while r:
                        if not pygame.mouse.get_pressed()[0]:
                            r = False
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEMOTION:
                                self.displayScroll -= event.rel[1]
                        VC.Screen.fill(VC.Black)
                        for o in VC.visualObjects:
                            o.render()
                        pygame.display.flip()
                    self.rendUpdate()
                elif VC.isGrid:
                    self.colDragging = True
                    self.startDragColumn = int(VC.whichColumnField.text)
                    self.colDragRel = 0
                    self.colDragStart = pos[0]
        self.end_scroll()

    def check_motion(self, pos):
        """Standard - what goes on when a user scrolls over the message."""
        if self.allowMouseCheck.checked:
            if VC.isGrid:
                s_pos = [pos[0] - 20, pos[1] - 80 + self.displayScroll + 10]
                try:
                    VC.whichLetterField.text = self.grid[int(s_pos[1] / 40)][int((15 + s_pos[0]) / 40)]
                    VC.whichColumnField.text = str(int((15 + s_pos[0]) / 40))
                    self.rendUpdate()
                except IndexError:
                    VC.whichLetterField.text = VC.whichLetterField.textInputted
                    VC.whichColumnField.text = VC.whichLetterField.textInputted
            else:
                s_pos = [pos[0] - 20, pos[1] - 95 + self.displayScroll + 10]
                try:
                    n = (s_pos[0] // 10) + (VC.lineSize * (s_pos[1] // 20))
                    if n >= 0 and 560 > pos[1] - 80 > 0 and pos[1] - 80 < 410 and 20 < pos[0] < 580:
                        VC.whichLetterField.text = ''.join(self.displayText)[int(n)]
                        VC.whichColumnField.text = str(n % VC.gridSize)
                        self.rendUpdate()
                    else:
                        raise IndexError
                except IndexError:
                    VC.whichLetterField.text = VC.whichLetterField.textInputted
                    VC.whichColumnField.text = VC.whichColumnField.textInputted
            if self.colDragging:
                if pygame.mouse.get_pressed()[0]:
                    self.colDragRel = pos[0] - self.colDragStart
                else:
                    if self.colDragRel > 0:
                        placesToDrag = self.colDragRel // 40
                    else:
                        placesToDrag = (self.colDragRel + 40) // 40

                    if 0 > self.startDragColumn + placesToDrag:
                        placesToDrag = -1 * self.startDragColumn
                    elif self.startDragColumn + placesToDrag >= VC.gridSize:
                        placesToDrag = VC.gridSize - 1 - self.startDragColumn

                    if placesToDrag != 0:
                        print('Reorder columns; column', self.startDragColumn, placesToDrag,
                              'place' + plural(placesToDrag) + ' to the right.')
                        self.columnReorder(self.startDragColumn, placesToDrag)

                    self.colDragging = False
                    self.colDragRel = 0

    def clean(self, obj):
        """Removes everything but letters from rawText and updates tne render."""
        obj.touch = None
        self.resetRawText(''.join([x for x in self.rawText.upper() if x in ''.join(x.upper() for x in alphabet)]))

    def columnReorder(self, column: int, placesToDrag: int):
        """Reorders the different columns in the rawText."""

        reLookIndexList = [x for x in range(VC.gridSize)]
        reLookIndexList.remove(column)
        reLookIndexList.insert(column + placesToDrag, column)

        if not self.hasDragHistory or not (len(self.dragHistory) == VC.gridSize):
            self.dragHistory = [str(x) for x in reLookIndexList]
        else:
            self.dragHistory = [self.dragHistory[n] for n in reLookIndexList]
        self.hasDragHistory = True

        print(reLookIndexList)

        columns = [[x for n, x in
                    enumerate(message.rawText) if n % VC.gridSize == column] for column in range(VC.gridSize)]
        newColumns = [columns[reLookIndexList[p]] for p in range(VC.gridSize)]

        newText = ''
        for n in range(len(message.rawText) + VC.gridSize):  # in final row reordering errors can cause problems.
            try:
                newText += newColumns[n % VC.gridSize][n // VC.gridSize]
            except IndexError:
                pass
        message.resetRawText(newText)

    def doReplace(self, replaceFieldA, replaceFieldB):
        """Replaces the given characters."""
        d = list(self.operationText().replace(replaceFieldA.text[0], replaceFieldB.text[0]))
        for n, x in enumerate(d):
            if x == VC.BlankLetter:
                d[n] = self.rawText[n]
        self.resetRawText(''.join(d))

    def end_scroll(self):
        """What happens when a scrolling event ends."""
        while self.displayScroll < -11:
            VC.Screen.fill(VC.Black)
            self.displayScroll = (-1 + self.displayScroll) / 1.1
            for o in VC.visualObjects:
                o.render()
            pygame.display.flip()
        if self.displayScroll < -5:
            self.displayScroll = -5
        self.rendUpdate()

    def makeLowerCase(self, obj):
        """Makes the selected characters lowercase."""
        obj.touch = None
        o = ''
        for n, x in enumerate(self.operationText()):
            if x == VC.BlankLetter:
                o += self.rawText[n]
            else:
                o += x.lower()
        self.resetRawText(o)

    def makeUpperCase(self, obj):
        """Makes the selected characters uppercase"""
        obj.touch = None
        o = ''
        for n, x in enumerate(self.operationText()):
            if x == VC.BlankLetter:
                o += self.rawText[n]
            else:
                o += x.upper()
        self.resetRawText(o)

    def operationText(self, stripNonLetters=False):
        """Returns only the selected character with everything else replaced by VC.BlankLetter"""
        if VC.selectPanel is not None:
            if stripNonLetters:
                return_onto = ''.join(
                    [x for x in self.rawText if x.upper() in (list(alphabet.upper()) + list(numbers))]
                )
            else:
                return_onto = self.rawText

            if VC.selectPanel.mode == 'All':
                return return_onto
            if VC.selectPanel.mode == 'Letter':
                o = ''
                for p in return_onto:
                    if p in VC.whichLetterField.text[0]:
                        o += p
                    else:
                        o += VC.BlankLetter
                return o
            if VC.selectPanel.mode == 'Column':
                o = ''
                for n, p in enumerate(return_onto):
                    if not VC.whichColumnField.text[0] == '':
                        if n % VC.gridSize == int(VC.whichColumnField.text[0]):
                            o += p
                        else:
                            o += VC.BlankLetter
                    else:
                        o += VC.BlankLetter
                return o
            if VC.selectPanel.mode == 'LC':
                o = ''
                for n, p in enumerate(return_onto):
                    if not VC.whichColumnField.text[0] == '':
                        if n % VC.gridSize == int(VC.whichColumnField.text[0]) and p in VC.whichLetterField.text[0]:
                            o += p
                        else:
                            o += VC.BlankLetter
                    else:
                        o += p
                return o
            if VC.selectPanel.mode == 'Word':
                index = int(VC.whatIndexField.text[0])
                separator = VC.whatSeparatorField.text[0]
                count = 0
                o = ''
                for char in self.rawText:
                    if char == separator:
                        count += 1
                        o += VC.BlankLetter
                    else:
                        if count == index:
                            o += char
                        else:
                            o += VC.BlankLetter
                return o

        return self.rawText

    def render(self):
        """Renders the message. Various modes and settings are implemented."""
        if VC.isGrid:
            for n, x in enumerate(self.grid):
                if 80 < 80 + (n * VC.lineWidth * 2) - self.displayScroll < 60 - (VC.lineWidth * 2) + self.height:
                    if n == 0:
                        plq = VC.SmallFont.render(''.join([z + '   ' for z in x]), False, VC.Black)
                    else:
                        plq = VC.SmallFont.render(''.join([z + '   ' for z in x]), False, VC.Blue)
                    VC.Screen.blit(plq, (20, 80 + (n * VC.lineWidth * 2) - self.displayScroll))
            if not VC.selectPanel.mode == 'All':
                for n, x in enumerate(self.gridMask):
                    if 80 < 80 + (n * VC.lineWidth * 2) - self.displayScroll < 60 - (VC.lineWidth * 2) + self.height:
                        plq = VC.SmallFont.render(''.join([z + '   ' for z in x]), False, VC.Red)
                        VC.Screen.blit(plq, (20, 80 + (n * VC.lineWidth * 2) - self.displayScroll))
            if self.colDragging:
                fill = pygame.Rect(20 + (self.startDragColumn * 40), 80, 30, self.height - 20)
                pygame.draw.rect(VC.Screen, VC.White, fill, 0)
                for r in range(len(self.grid)):
                    if r == 0:
                        plq = VC.SmallFont.render(self.grid[r][self.startDragColumn], False, VC.Black)
                    else:
                        plq = VC.SmallFont.render(self.grid[r][self.startDragColumn], False, VC.Blue)
                    VC.Screen.blit(plq, (20 + (40 * self.startDragColumn) + self.colDragRel,
                                         80 + (r * VC.lineWidth * 2) - self.displayScroll))
        else:
            for n, x in enumerate(self.displayText):
                if 80 < 80 + (n * VC.lineWidth) - self.displayScroll < 60 - VC.lineWidth + self.height:
                    plq = VC.SmallFont.render(x, False, VC.Blue)
                    VC.Screen.blit(plq, (20, 80 + (n * VC.lineWidth) - self.displayScroll))
            if not VC.selectPanel.mode == 'All':
                for n, x in enumerate(self.displayMask):
                    if 80 < 80 + (n * VC.lineWidth) - self.displayScroll < 60 - VC.lineWidth + self.height:
                        plq = VC.SmallFont.render(x, False, VC.Red)
                        VC.Screen.blit(plq, (20, 80 + (n * VC.lineWidth) - self.displayScroll))

    def rendUpdate(self):
        """Updates various backend variables for the render based on an updated rawText."""
        self.displayText = ['' for _ in range((len(self.rawText) // VC.lineSize) + 1)]
        for n, x in enumerate(self.rawText):
            self.displayText[n // VC.lineSize] += x
        self.displayMask = ['' for _ in range((len(self.operationText()) // VC.lineSize) + 1)]
        for n, x in enumerate(self.operationText()):
            if x == VC.BlankLetter:
                self.displayMask[n // VC.lineSize] += ' '
            else:
                self.displayMask[n // VC.lineSize] += x

        into_table = ''.join([x for x in self.rawText if x.upper() in alphabet.upper() + numbers])
        if not self.hasDragHistory:
            self.grid = [''.join([str(n) for n in range(VC.gridSize)])]
            self.gridMask = [''.join([str(n) for n in range(VC.gridSize)])]
        else:
            self.grid = [self.dragHistory]
            self.gridMask = [self.dragHistory]
        for x in range(len(into_table) // VC.gridSize):
            self.grid.append(into_table[x * VC.gridSize:(x + 1) * VC.gridSize])

        into_table = self.operationText(stripNonLetters=True)
        o = ''
        for n, x in enumerate(into_table):
            if x == VC.BlankLetter:
                o += ' '
            else:
                o += x
        for x in range(len(o) // VC.gridSize):
            self.gridMask.append(o[x * VC.gridSize:(x + 1) * VC.gridSize])

    def reverse(self, obj):
        """Reverses the selected characters."""
        obj.touch = None
        mask = ''.join([x for x in self.operationText() if not x == VC.BlankLetter])[::-1]
        o = ''
        for n, x in enumerate(self.operationText()):
            if x == VC.BlankLetter:
                o += self.rawText[n]
            else:
                o += mask[0]
                mask = mask[1:]
        self.resetRawText(o)

    def resetRawText(self, text: str):
        """Used to change the raw text for the message.

        Updates the render and the crtl+z database."""
        reMask = ''
        for n, char in enumerate(text):
            if char == VC.BlankLetter:
                reMask += message.rawText[n]
            else:
                reMask += char

        if not self.rawText == reMask:
            self.rawTextDataBase.append(self.rawText)
            self.rawText = reMask
        self.rendUpdate()

    def substitution(self, obj):
        """Applies a quadgram-based substitution solve on the selected characters."""
        if VC.quadgrams is None:
            VC.loadquadgrams()
        obj.touch = None
        mask = ''.join([x for x in self.operationText() if not x == VC.BlankLetter]).upper()
        print('Initiating substitution solve on selected characters, length:', len(mask))
        st = time.time()
        still_to_do = sorted(list(alphabet.upper()), key=(lambda y: mask.count(y)), reverse=True)
        re = [mask.count(x.upper()) for x in alphabet]
        l_num = re.index(max(re))
        mask = mask.replace(alphabet[l_num].upper(), 'e')
        still_to_do.remove(alphabet[l_num].upper())
        res = []
        for n in range(len(mask)):
            if n < len(mask) - 2 and mask[n + 2] == 'e':
                res.append(mask[n: n + 2])
        most_common = statistics.mode(res)
        mask = mask.replace(most_common[0], 't')
        mask = mask.replace(most_common[1], 'h')
        still_to_do.remove(most_common[0])
        still_to_do.remove(most_common[1])
        still_to_replace = list('abcdfgijklmnopqrsuvwxyz')

        while len(still_to_do) > 0:
            base_character = still_to_do[0]
            best_score = score(mask)
            best_char = ''
            for checkChar in still_to_replace:
                if score(mask.replace(base_character, checkChar)) > best_score:
                    best_char = checkChar
                    best_score = score(mask.replace(base_character, checkChar))
            if best_char != '':
                mask = mask.replace(base_character, best_char)
                still_to_do.remove(base_character)
                still_to_replace.remove(best_char)
                print('Replaced letter', base_character, 'with letter', best_char, len(still_to_do),
                      len(still_to_replace))
            else:
                if len(still_to_do) != 1:
                    still_to_do = still_to_do[1:] + [still_to_do[0]]
                else:
                    print('Finished')
                    mask = mask.replace(still_to_do[0], still_to_replace[0])
                    still_to_replace = []
                    still_to_do = []

        self.resetRawText(mask)
        print('Operation completed in', int((time.time() - st) * 100) / 100, 'seconds')

    def transposition(self, obj):
        VC.simplePump()  # Prevents 'not responding'
        VC.simplePump()
        obj.blank = None

        print('Loading dictionary...')
        qg = open('qgrams.txt', 'r')
        qg = list(qg.readlines())
        for n in range(len(qg)):
            qg[n] = qg[n].split()
        qg = dict(qg)

        def transpositionSolve(text):
            def score_2(string):
                string = string.upper()
                s = 0
                for counter in range(len(string) - 3):
                    snip = string[counter:counter + 4]
                    try:
                        s += math.log10(int(qg[snip]))
                    except KeyError:
                        s += math.log10(0.5)
                return s

            def key_score(k):
                shuffle = reArrange(k)
                return score_2(shuffle)

            def reArrange(k):
                blocks = [text[counter:counter + keylength] for counter in range(0, len(text), keylength)]
                for blockNumber, b in enumerate(blocks):
                    if not len(b) < keylength:
                        c = ''
                        for count in k:
                            c += b[count]
                            blocks[blockNumber] = c
                return ''.join(blocks)

            def visualise():
                plq = pygame.Surface((len(population) + 40, 400))
                plq.fill(VC.Black)
                for count, value in enumerate(scores):
                    plq.set_at((count + 20, int(value/100) + 20), VC.White)
                return plq

            def permute(k, maxChanges, pOfSplice=0.5):
                lengthOfKey = len(k)
                v2 = k[:]
                for _ in range(random.randint(0, maxChanges)):
                    flip = random.random()
                    if flip > pOfSplice:
                        a = random.randint(0, lengthOfKey - 1)
                        b = random.randint(0, lengthOfKey - 1)
                        v2[a], v2[b] = v2[b], v2[a]
                    else:
                        while True:
                            # repeat until random selects a valid splice
                            a = random.randint(0, lengthOfKey - 1)
                            b = random.randint(0, lengthOfKey - 1)
                            if a < b:
                                splice = v2[a:b]
                                return random.choice(
                                    [v2[0:a] + splice + v2[b:], splice + v2[0:a] + v2[b:], v2[0:a] + v2[b:] + splice])
                return v2

            length = len([char for char in text if char.lower() in alphabet])
            print('Message length:', length)
            print('Factors:', factorise(length))
            keylength = int(input('Keylength to try?'))
            randomnessBaseline = 4
            randomnessEndpoint = 20
            populationSize = 100
            key = list(range(keylength))
            population = []
            for _ in range(99):
                random.shuffle(key)
                population.append(key)
            gen_Number = 0
            previousBest = 0
            timeSincePreviousBest = 0
            rateOfRandomnessIncrease = 7  # lower is faster
            pOfSlice = 0.5
            scores = []
            print('Beginning Solve, with parameters:')
            print('Population Size:', populationSize)
            print('Baseline permutations:', randomnessBaseline)
            print('Generations to increase randomness:', rateOfRandomnessIncrease)
            print('Endpoint generations without improvement:', randomnessEndpoint)
            print()
            if input('Do you wish to change any of these parameters? (y/n)').upper() == 'Y':
                populationSize = int(input('Population Size?'))
                randomnessBaseline = int(input('Randomness Baseline?'))
                rateOfRandomnessIncrease = int(input('After how many generations should r increase?'))
                randomnessEndpoint = int(input('At what r should the program give up?'))

            print()
            print('Press the red X at any time to end the solve.')
            randomness = randomnessBaseline
            running = True
            while running:
                population = population + [permute(key, randomness, pOfSplice=pOfSlice) for key in population]
                population.sort(reverse=True, key=key_score)
                population = population[0:populationSize]

                print('Gen', gen_Number,
                      reArrange(population[0])[0:20], 'r', randomness, 'score',
                      int(key_score(population[0])), 'key',
                      '.'.join([str(char) for char in population[0]]))
                scores = [key_score(key) for key in population]
                running = VC.simplePump(img=visualise(), pos=(20, 150))  # Prevents 'not responding'

                gen_Number += 1
                if previousBest == key_score(population[0]):
                    timeSincePreviousBest += 1
                    if timeSincePreviousBest > rateOfRandomnessIncrease:
                        randomness += 1
                        timeSincePreviousBest = 0
                else:
                    previousBest = key_score(population[0])
                    randomness = randomnessBaseline

                if timeSincePreviousBest > randomnessEndpoint:
                    running = False

            print('Best Guess:')
            print('Key:', '.'.join([str(num) for num in population[0]]))
            print(reArrange(population[0]))
            print()
            return reArrange(population[0])

        print('Beginning Transposition ---')
        new = transpositionSolve(self.operationText())
        t = ''
        for n, x in enumerate(new):
            if x == VC.BlankLetter:
                t += self.rawText[n]
            else:
                t += x
        self.resetRawText(t)


class ScrollBar:
    def __init__(self, parent, x, y, size, expandFactor, colour=VC.Black, width=10):
        """Creates a new ScrollBar."""
        self.scrolling = False
        self.parent = parent
        self.x = x
        self.y = y
        self.lastPos = 0
        self.size = size
        self.expandFactor = expandFactor
        self.width = width
        self.font = VC.MainFont
        self.colour = colour

    @property
    def shift(self):
        """The amount by which the scroll-bar has been scrolled."""
        return self.parent.displayScroll // self.expandFactor

    def parents(self):
        """Returns the parents of the scroll-bar."""
        o = self
        output = []
        while o is not VC:
            output.append(o)
            o = [o.parent][0]
        return output

    def render(self):
        """Renders the scroll-bar."""
        pygame.draw.rect(VC.Screen, self.colour, pygame.Rect(sum([o.x for o in self.parents()]) + self.x,
                                                             sum([o.y for o in self.parents()]) + self.y + self.shift,
                                                             self.width, self.size), 0)

    def check_motion(self, pos):
        """Standard: Checks a mouse-motion."""
        if self.scrolling:
            self.parent.displayScroll -= (self.lastPos - pos[1]) * self.expandFactor
            self.lastPos = pos[1]
        if self.scrolling and not pygame.mouse.get_pressed()[0]:
            self.scrolling = False
            self.parent.end_scroll()

    def check_click(self, pos):
        """Standard: Checks a mouse-click"""
        if self.mouse_contains(pos):
            self.scrolling = True
            self.lastPos = pygame.mouse.get_pos()[1]

    def mouse_contains(self, pos):
        """Checks whether or not the position is within the scroll-bar, in its current scroll state."""
        if sum([o.x for o in self.parents()]) < pos[0] - self.x < sum([o.x for o in self.parents()]) + self.width:
            if sum([o.y for o in self.parents()]) + self.y + self.shift < pos[1] \
                    < sum([o.y for o in self.parents()]) + self.y + self.shift + self.size:
                return True
        return False


def coPrime(a, b):
    """Checks whether or not a is co-prime with 26. Used in the affine solve."""
    for x in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if a % x == b % x == 0:
            return True
    return False


def score(string):
    """Returns the quadgram score for a given string."""
    string = string.upper()
    o = 0
    for n in range(len(string) - 3):
        snip = string[n:n + 4]
        try:
            o += math.log10(int(VC.quadgrams[snip]))
        except KeyError:
            pass
    return o


with open('message.txt', 'r') as ms:
    """Creates the message object."""
    message = Message(ms.read())
    message.parent = VC
