import pygame

pygame.init()
pygame.font.init()


class VC:
    """View Control: A container for various variables related to appearance."""
    displayDims = (1200, 800)
    Screen = pygame.display.set_mode(displayDims)
    pygame.display.set_caption('CipherSuite 1.0')
    MainFont = pygame.font.SysFont('Calibri', 20, False)
    SmallFont = pygame.font.SysFont('Courier New', 16, False)
    VerySmallFont = pygame.font.SysFont('Calibri', 16, False)
    BlankLetter = '_'
    lineWidth = 20
    lineSize = 56
    gridSize = 6
    keyBindings = {}
    keyBindingHints = []
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Green = (0, 255, 0)
    Orange = (255, 255, 0)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Purple = (117, 12, 150)
    WindowsBlueScreenOfDeath = (160, 240, 120)
    alphaOrder = False
    isGrid = True
    selectPanel = None
    whichLetterField = None
    whichColumnField = None
    visualObjects = None
    quadgrams = None
    gridSizeField = None
    touch = None
    doColumnVis = None
    columnarIocPanel = None

    @classmethod
    def check_click(cls, pos: tuple):
        pass

    @classmethod
    def check_motion(cls, pos: tuple):
        pass

    @classmethod
    def loadquadgrams(cls):
        qg = open('qgrams.txt', 'r')
        rl = list(qg.readlines())
        for n in range(len(rl)):
            rl[n] = rl[n].split()
        cls.quadgrams = dict(rl)

    @classmethod
    def render(cls):
        for n, x in enumerate(cls.keyBindingHints):
            plq = cls.SmallFont.render(x, 0, cls.Orange)
            cls.Screen.blit(plq, (10, (790 - (20 * len(cls.keyBindingHints))) + (n * 20)))

    @classmethod
    def simplePump(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        cls.Screen.fill(cls.WindowsBlueScreenOfDeath)
        plq = cls.MainFont.render('A solve is in operation. Refer to the console. Press the close button in the '
                                  'corner to interrupt it.', 0, cls.Black)
        cls.Screen.blit(plq, (50, 50))
        plq = cls.MainFont.render('If the console is waiting for an input, it will not work immediately.', 0, cls.Black)
        cls.Screen.blit(plq, (50, 100))
        pygame.display.flip()
        return True


def input2(obj):
    """Used by input fields for text entry."""
    r = True
    t = ''
    while r:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                r = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    r = False
                elif pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                    try:
                        t += alphabet.upper()[event.key - 97]
                    except IndexError:
                        try:
                            t += '0123456789'[event.key - 48]
                        except IndexError:
                            pass
                else:
                    try:
                        t += alphabet[event.key - 97]
                    except IndexError:
                        try:
                            t += '0123456789'[event.key - 48]
                        except IndexError:
                            pass
            if event.type == pygame.QUIT:
                r = False

            obj.render(green=True)
            pygame.display.flip()
    return t


def plural(n: int):
    """Prevents '1 items' errors."""
    if n == 1:
        return ''
    else:
        return 's'


def factorise(n: int):
    x = 2
    result = []
    while x < n:
        if n // x == n / x:
            result.append(x)
            n /= x
        else:
            x += 1
    result.append(int(n))
    return result


alphabet = 'abcdefghijklmnopqrstuvwxyz'
numbers = '1234567890'
otherAllowedChars = ['', ',', '.', '-', '0', '1', '2']

englishLetterFrequencies = [
    ('E', '12.02%'),
    ('T', '9.10%'),
    ('A', '8.12%'),
    ('O', '7.68%'),
    ('I', '7.31%'),
    ('N', '6.95%'),
    ('S', '6.28%'),
    ('R', '6.02%'),
    ('H', '5.92%'),
    ('D', '4.32%'),
    ('L', '3.98%'),
    ('U', '2.88%'),
    ('C', '2.71%'),
    ('M', '2.61%'),
    ('F', '2.30%'),
    ('Y', '2.11%'),
    ('W', '2.09%'),
    ('G', '2.03%'),
    ('P', '1.82%'),
    ('B', '1.49%'),
    ('V', '1.11%'),
    ('K', '0.69%'),
    ('X', '0.17%'),
    ('Q', '0.11%'),
    ('J', '0.10%'),
    ('Z', '0.07%'),
    (' ', '')]

sortedELF = [float(x[1][:-1]) for x in sorted(englishLetterFrequencies, key=(lambda x: x[0]))[1:]]
