from part3 import *
from ext1 import ioc, generalIntelligence

# noinspection SpellCheckingInspection, PyTypeChecker
def calculate_key_length(obj):
    """Searches for a good column length for the message."""

    obj.touch = None
    if VC.quadgrams is None:
        VC.loadquadgrams()

    message.clean(VC)

    results = dict([key, 0] for key in range(3, 30))
    for colLength in results.keys():
        sc = 0
        for column in range(colLength):
            sc += ioc(''.join(x for n, x in enumerate(message.rawText) if n % colLength == column))
        results[colLength] = sc

    results = [[a, results[a]] for a in sorted(list(results), key=(lambda x: results[x]), reverse=True)]
    average = sum([a[1] for a in results]) / len(results)
    print('In columnise operation, average score was', average, 'and the highest score was', results[0][1],
          'for keylength', str(results[0][0]) + '. The message has been updated.')

    column_length = results[0][0]
    VC.gridSize = column_length
    VC.gridSizeField.text = [str(column_length)]
    message.rendUpdate()


def doColumnVis(obj):
    """Works out columnar iOC for all columns."""
    obj.text = ['Col. IoC', '']
    obj.height = 40
    for n in range(VC.gridSize):
        apply = ''.join([x for n2, x in enumerate(message.operationText()) if
                         n2 % VC.gridSize == n and not x == VC.BlankLetter])

        obj.text.append(str(n) + ' ' + str(ioc(apply))[:6])
        obj.height += 20


def doReplaceL(obj):
    """Remaps button click for function with arguments."""
    obj.touch = None
    message.doReplace(replaceFieldA, replaceFieldB)


def debug(obj):
    """Can perform various debug functions. Triggered by key escape."""
    print("Looks like we haven't got anything set up for debug right now.")


def makeAll(obj):
    """Sets the Select mode to All."""
    selectPanel.mode = 'All'
    message.rendUpdate()
    obj.colour = VC.Red
    for o in obj.partners:
        o.colour = VC.Green


def makeColumn(obj):
    """Sets the Select mode to Column."""
    VC.selectPanel.mode = 'Column'
    message.rendUpdate()
    obj.colour = VC.Red
    VC.whichColumnField.textInputted = copy.deepcopy(VC.whichColumnField.text)
    for o in obj.partners:
        o.colour = VC.Green


def makeGrid(obj):
    """Sets the View Control Message View mode to Grid."""
    VC.isGrid = True
    obj.textColour = VC.Red
    obj.partner.textColour = VC.Black


def makeLC(obj):
    """Sets the Select mode to Letter + Column."""
    VC.selectPanel.mode = 'LC'
    message.rendUpdate()
    obj.colour = VC.Red
    for o in obj.partners:
        o.colour = VC.Green


def makeLetter(obj):
    """Sets the Select mode to Letter."""
    selectPanel.mode = 'Letter'
    message.rendUpdate()
    obj.colour = VC.Red
    for o in obj.partners:
        o.colour = VC.Green


def makeSmooth(obj):
    """Sets the View Control Message View mode to Smooth."""
    VC.isGrid = False
    obj.textColour = VC.Red
    obj.partner.textColour = VC.Black


def makeWord(obj):
    """Sets the Select mode to Word."""
    selectPanel.mode = 'Word'
    message.rendUpdate()
    obj.colour = VC.Red
    for o in obj.partners:
        o.colour = VC.Green


def morseDecrypt(text, wordSeparator=None, letterSeparator=' '):
    output = ''
    if wordSeparator is None:
        wordSeparator = VC.whatSeparatorField.text[0]
    for word in text.split(wordSeparator):
        for letter in word.split(letterSeparator):
            try:
                output += VC.morseDict[letter]
            except KeyError:
                pass
        output += ' '
    return output


def morseDo(obj):
    obj.touch = None
    message.resetRawText(morseDecrypt(message.operationText()))


def printMessage(obj):
    """Prints the message to the console."""
    obj.touch = None
    print('Raw message text:')
    print(message.rawText)
    if not VC.selectPanel.mode == 'All':
        print('Highlighted text:')
        print(message.operationText())


def stageGeneralAnalysis(obj):
    obj.touch = None
    generalIntelligence(''.join([x for x in message.operationText() if x != VC.BlankLetter]))


def swapOrder(obj):
    """Swaps the frequency view mode between alphabetical and by frequency."""
    obj.touch = None
    VC.alphaOrder = not VC.alphaOrder
    VC.Screen.fill(VC.Black)
    for o in VC.visualObjects:
        o.render()


def undo():
    print('Undo, depth = ', message.canRedo)
    try:
        message.canRedo -= 1
        message.rawText = message.rawTextDataBase[message.canRedo]
        message.rendUpdate()
        print(message.rawText)
    except IndexError:
        print('Insufficient actions to undo.')
        message.canRedo += 1


def redo():
    if not message.canRedo == 0:
        print('Redo, depth = ', message.canRedo)
        message.rawText = message.rawTextDataBase[message.canRedo]
        message.rendUpdate()
        message.canRedo += 1
    else:
        print('No undo to redo. ')


def updateGridSize(val):
    """Updates the size of the grid (i.e. keylength)"""
    VC.gridSize = int(val[0])
    message.rendUpdate()


def updateSmoothSize(val):
    """Updates the line size in smooth mode."""
    VC.lineSize = int(val[0])
    message.rendUpdate()


messagePanel = Panel(VC, 10, 70, 600, 450)
gridButton = Panel(VC, 80, 15, 140, 40, typ='button', text=['Grid'], text_colour=VC.Red,
                   font=VC.MainFont, on_click=makeGrid, text_offset=(50, 10))
smoothButton = Panel(VC, 300, 15, 140, 40, typ='button', text=['Smooth'], text_colour=VC.Black,
                     font=VC.MainFont, on_click=makeSmooth, text_offset=(40, 10))
gridButton.partner = smoothButton
smoothButton.partner = gridButton
makeSmooth(smoothButton)
analyseText = Panel(VC, 660, 20, 200, 40, typ='text', text=['Analyse'],
                    text_colour=VC.White, font=VC.MainFont)
editText = Panel(VC, 1010, 20, 200, 40, typ='text', text=['Edit'],
                 text_colour=VC.White, font=VC.MainFont)
replacePanel = Panel(VC, 1000, 50, 160, 120)
replaceText = Panel(replacePanel, 20, 20, 100, 100, typ='text', text=['Replace:', '', 'with:'],
                    text_colour=VC.Black, font=VC.MainFont)
replaceFieldA = TextField(replacePanel, 110, 20, 30, 30, default_text=['A'])
replaceFieldB = TextField(replacePanel, 110, 60, 30, 30, default_text=['b'])
gridSizeField = TextField(VC, 20, 20, 40, 30, default_text=['6'], onReturn=updateGridSize, doNotLeaveBlank=True)
VC.gridSizeField = gridSizeField
smoothSizeField = TextField(VC, 240, 20, 40, 30, default_text=['56'], onReturn=updateSmoothSize)
replaceButton = Panel(replacePanel, 30, 80, 30, 30, typ='button', text=['Go'], text_colour=VC.Black,
                      font=VC.MainFont, on_click=doReplaceL, text_offset=(4, 4), colour=VC.Green)
makeUpperCaseButton = Panel(VC, 1000, 180, 160, 40, typ='button', text=['Make uppercase'], text_colour=VC.Black,
                            font=VC.MainFont, on_click=message.makeUpperCase, text_offset=(10, 10))
makeLowerCaseButton = Panel(VC, 1000, 230, 160, 40, typ='button', text=['Make lowercase'], text_colour=VC.Black,
                            font=VC.MainFont, on_click=message.makeLowerCase, text_offset=(10, 10))
reverseButton = Panel(VC, 1000, 280, 160, 40, typ='button', text=['Reverse'], text_colour=VC.Black,
                      font=VC.MainFont, on_click=message.reverse, text_offset=(10, 10))
cleanUpButton = Panel(VC, 1000, 330, 160, 40, typ='button', text=['Clean Up'], text_colour=VC.Black,
                      font=VC.MainFont, on_click=message.clean, text_offset=(10, 10))
columniseButton = Panel(VC, 1000, 380, 160, 40, typ='button', text=['Columnise'], text_colour=VC.Black,
                        font=VC.MainFont, on_click=calculate_key_length, text_offset=(10, 10))
freqPanel = FreqPanel(VC, 650, 50, 140, 515)
trigPanel = TrigPanel(VC, 800, 350, 100, 180)
columnarIocPanel = Panel(VC, 910, 350, 80, 140, on_click=doColumnVis, typ='button', text=['Col. IoC'],
                         text_colour=VC.Black, font=VC.SmallFont, colour=VC.White)
VC.columnarIocPanel = columnarIocPanel
VC.doColumnVis = doColumnVis
doColumnVis(columnarIocPanel)
message.freqObjectLink = freqPanel
message.trigObjectLink = trigPanel
letterCheckButton = Panel(VC, 800, 300, 130, 40, typ='button', text=['Check letters'], text_colour=VC.Black,
                          font=VC.MainFont, on_click=message.basicAnalysis, text_offset=(10, 10))
selectPanel = Panel(VC, 800, 50, 190, 240)
selectPanel.mode = 'All'
selectPanel.letter = 'e'
VC.selectPanel = selectPanel

makeAllButton = Panel(selectPanel, 10, 10, 50, 40, typ='button', colour=VC.Red, text=['All'],
                      text_colour=VC.Black, font=VC.MainFont, on_click=makeAll, text_offset=(10, 10))
makeLetterButton = Panel(selectPanel, 10, 60, 100, 40, typ='button', colour=VC.Green, text=['Letter(s):'],
                         text_colour=VC.Black, font=VC.MainFont, on_click=makeLetter, text_offset=(10, 10))
makeColumnButton = Panel(selectPanel, 10, 110, 90, 40, typ='button', colour=VC.Green, text=['Column:'],
                         text_colour=VC.Black, font=VC.MainFont, on_click=makeColumn, text_offset=(10, 10))
makeLCButton = Panel(selectPanel, 150, 110, 35, 40, typ='button', colour=VC.Green, text=['L+C'],
                     text_colour=VC.Black, font=VC.MainFont, on_click=makeLC, text_offset=(3, 10))
makeWordButton = Panel(selectPanel, 10, 190, 60, 40, typ='button', colour=VC.Green, text=['Word:'],
                       text_colour=VC.Black, font=VC.MainFont, on_click=makeWord, text_offset=(3, 10))
makeAllButton.partners = [makeLetterButton, makeColumnButton, makeLCButton, makeWordButton]
makeLetterButton.partners = [makeAllButton, makeColumnButton, makeLCButton, makeWordButton]
makeColumnButton.partners = [makeAllButton, makeLetterButton, makeLCButton, makeWordButton]
makeLCButton.partners = [makeAllButton, makeLetterButton, makeColumnButton, makeWordButton]
makeWordButton.partners = [makeAllButton, makeLetterButton, makeColumnButton, makeLCButton]
whichLetterField = TextField(selectPanel, 120, 65, 30, 30)
VC.whichLetterField = whichLetterField
whichColumnField = TextField(selectPanel, 110, 115, 30, 30)
VC.whichColumnField = whichColumnField
whatSeparatorField = TextField(selectPanel, 75, 200, 30, 30, default_text='/')
VC.whatSeparatorField = whatSeparatorField
whatIndexField = TextField(selectPanel, 125, 200, 30, 30)
VC.whatIndexField = whatIndexField


allowMouseCheck = CheckBox(selectPanel, 130, 155)
message.allowMouseCheck = allowMouseCheck
allowMouseText = Panel(selectPanel, 10, 160, 200, 40, typ='text', text=['Set by hovering:'],
                       text_colour=VC.Black, font=VC.VerySmallFont)
wordInfoText = Panel(selectPanel, 75, 185, 0, 0, typ='text', text=['Separator-Index'],
                     text_colour=VC.Black, font=VC.VerySmallFont)
msgScroll = ScrollBar(message, 303, 0, 150, 3, VC.Blue)
caesarPanel = Panel(VC, 1000, 430, 160, 260)
doCaesarButton = Panel(caesarPanel, 10, 10, 120, 39, typ='button', colour=VC.Green, text=['Caesar'],
                       text_colour=VC.Black, font=VC.MainFont, on_click=message.caesar, text_offset=(10, 10))
doAffineButton = Panel(caesarPanel, 10, 50, 120, 39, typ='button', colour=VC.Green, text=['Affine'],
                       text_colour=VC.Black, font=VC.MainFont, on_click=message.affine, text_offset=(10, 10))
doSubstButton = Panel(caesarPanel, 10, 90, 120, 39, typ='button', colour=VC.Green, text=['Substitution'],
                      text_colour=VC.Black, font=VC.MainFont, on_click=message.substitution, text_offset=(10, 10))
doTransButton = Panel(caesarPanel, 10, 130, 120, 39, typ='button', colour=VC.Green, text=['Transposition'],
                      text_colour=VC.Black, font=VC.MainFont, on_click=message.transposition, text_offset=(10, 10))
doMorseButton = Panel(caesarPanel, 10, 170, 120, 39, typ='button', colour=VC.Green, text=['De-Morse'],
                      text_colour=VC.Black, font=VC.MainFont, on_click=morseDo, text_offset=(10, 10))
doGeneralIntelligenceButton = Panel(caesarPanel, 10, 210, 120, 39, typ='button', colour=VC.Green,
                                    text=['General'], text_colour=VC.Black, font=VC.MainFont,
                                    on_click=stageGeneralAnalysis, text_offset=(10, 10))

pict = pygame.Surface((40, 40))
pict.fill(VC.ChrisBlue)
undoIcon = pygame.transform.scale(pygame.image.load('undo.png'), (30, 30))
pict.blit(undoIcon, (5, 0))
pygame.display.set_icon(undoIcon)
undoButton = CustomButton(480, 15, pict, undo)
pict = pygame.transform.flip(pict, True, False)
redoButton = CustomButton(530, 15, pict, redo)

VC.visualObjects = [messagePanel, gridButton, smoothButton, replacePanel, replaceFieldA, replaceFieldB,
                    replaceText, editText, analyseText, replaceButton, message, makeUpperCaseButton,
                    makeLowerCaseButton, reverseButton, freqPanel, trigPanel, letterCheckButton, selectPanel,
                    makeAllButton, whichLetterField, makeLetterButton, makeColumnButton, whichColumnField,
                    allowMouseCheck, allowMouseText, makeLCButton, gridSizeField, smoothSizeField,
                    msgScroll, columnarIocPanel, caesarPanel, doCaesarButton, doSubstButton, doAffineButton,
                    VC, cleanUpButton, columniseButton, undoButton, redoButton, doTransButton, doMorseButton,
                    makeWordButton, wordInfoText, whatSeparatorField, whatIndexField, doGeneralIntelligenceButton]

VC.keyBindings = {
    pygame.K_ESCAPE: [debug, None],
    pygame.K_a: [makeAll, makeAllButton],
    pygame.K_l: [makeLetter, makeLetterButton],
    pygame.K_c: [makeColumn, makeColumnButton],
    pygame.K_k: [makeLC, makeLCButton],
    pygame.K_w: [makeWord, makeWordButton],
    pygame.K_1: [message.caesar, message],
    pygame.K_2: [message.affine, message],
    pygame.K_3: [message.substitution, message],
    pygame.K_b: [swapOrder, freqPanel],
    pygame.K_p: [printMessage, VC],
    pygame.K_u: [message.makeUpperCase, VC],
    pygame.K_i: [message.makeLowerCase, VC],
    pygame.K_r: [message.reverse, VC],
    pygame.K_g: [stageGeneralAnalysis, VC]
}

VC.keyBindingHints = [
    'Escape: Prints debug information.',
    'A: Sets the select mode to All.',
    'B: Switches the frequency panel between alphabetical mode and frequency-ordered mode.',
    'C: Sets the select mode to Column.',
    'I: Makes the selected letters lowercase.',
    'K: Sets the select mode to Letter + Column.',
    'L: Sets the select mode to Letter(s).',
    'W: Sets the select mode to Word.',
    'P: Prints the message rawText (and the selected text if applicable) to the console.',
    'R: Reverses the selected letters',
    'U: Makes the selected letters uppercase.',
    '1: Applies a frequency-based caesar solve to the selected letters.',
    '2: Applies a frequency-based affine solve to the selected letters.',
    '3: Applies a quadgram-based substitution solve to the selected letters.',
]
