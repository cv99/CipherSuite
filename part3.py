import copy

from part4 import *


class Buttons:
    selectedLetter = None
    selectedColumn = None


# noinspection PyShadowingNames
class Panel:
    def __init__(self, parent, x, y, length, h, typ='struct', colour=None, on_click=None, text=None,
                 font=None, text_colour=VC.Black, on_motion=None, text_offset=None):
        """Creates a new panel.

        Used variously for on-screen grouping, buttons, and text-headers."""
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.height = h
        self.typ = typ
        self.partner = None
        if colour is None:
            colour = VC.White
        self.colour = colour
        self.onClick = on_click
        if typ in ['text', 'button']:
            self.text = text
            self.font = font
            self.textColour = text_colour
        self.onMotion = on_motion
        if on_motion is not None:
            self.mouseOn = False
        if text_offset is not None:
            self.textOffset = text_offset
        else:
            self.textOffset = (0, 0)

    def parents(self):
        """Standard: Returns the parent list for the panel."""
        o = self
        output = []
        while o is not VC:
            output.append(o)
            o = [o.parent][0]
        return output

    def render(self):
        """Renders the panel to VC.Screen."""
        if self.typ in ['struct', 'button']:
            pygame.draw.rect(VC.Screen, self.colour,
                             pygame.Rect(sum([p.x for p in self.parents()]), sum([p.y for p in self.parents()]),
                                         self.length, self.height))
        if self.typ in ['text', 'button']:
            for n, x in enumerate(self.text):
                plq = self.font.render(x, False, self.textColour)
                VC.Screen.blit(plq, (sum([p.x for p in self.parents()]) + self.textOffset[0],
                                     sum([p.y for p in self.parents()]) + self.textOffset[1] + n * VC.lineWidth))

    def check_click(self, pos):
        """Standard: Checks for a mouse-click."""
        if self.onClick is not None:
            if sum([p.x for p in self.parents()]) + self.length > pos[0] > sum([p.x for p in self.parents()]) and \
                    sum([p.y for p in self.parents()]) + self.height > pos[1] > sum([p.y for p in self.parents()]):
                self.onClick(self)
                return True
        return False

    def check_motion(self, pos):
        """Standard: Checks for mouse-motion."""
        if self.onMotion is not None:
            if sum([p.x for p in self.parents()]) + self.length > pos[0] > sum([p.x for p in self.parents()]) and \
                    sum([p.y for p in self.parents()]) + self.height > pos[1] > sum([p.y for p in self.parents()]):

                if not self.mouseOn:
                    self.mouseOn = True
                    self.onMotion(self)
                return True
            if self.mouseOn:
                self.mouseOn = False
                self.onMotion(self)
            return False


# noinspection PyShadowingNames
class TextField:
    def __init__(self, parent, x, y, length, h, default_text=None, text_color=None, text_offset=(5, 5), onReturn=None):
        """Creates a new text field. Used for text entry."""
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.height = h
        self.font = VC.MainFont
        if default_text is None:
            default_text = ['']
        self.onReturn = onReturn
        self.text = default_text
        self.textInputted = default_text
        self.textOffset = text_offset
        if text_color is None:
            self.textColour = VC.Black
        else:
            self.textColor = text_color

    def parents(self):
        """Standard: Returns the parent list for the object."""
        o = self
        output = []
        while o is not VC:
            output.append(o)
            o = [o.parent][0]
        return output

    def render(self, green=False):
        """Renders the object to the screen."""
        pygame.draw.rect(VC.Screen, VC.White, pygame.Rect(sum([p.x for p in self.parents()]),
                                                          sum([p.y for p in self.parents()]),
                                                          self.length,
                                                          self.height))
        if green:
            pygame.draw.rect(VC.Screen, VC.Green, pygame.Rect(sum([p.x for p in self.parents()]),
                                                              sum([p.y for p in self.parents()]),
                                                              self.length,
                                                              self.height), 2)
        else:
            pygame.draw.rect(VC.Screen, VC.Blue, pygame.Rect(sum([p.x for p in self.parents()]),
                                                             sum([p.y for p in self.parents()]),
                                                             self.length,
                                                             self.height), 2)
        if type(self.text) is str:
            td = [(0, self.text)]
        else:
            td = enumerate(self.text)
        for n, x in td:
            plq = self.font.render(x, False, self.textColour)
            VC.Screen.blit(plq, (sum([p.x for p in self.parents()]) + self.textOffset[0],
                                 sum([p.y for p in self.parents()]) + self.textOffset[1] + VC.lineWidth * n))

    def check_motion(self, pos):
        """Standard: Checks for a mouse-motion."""
        pass

    def check_click(self, pos):
        """Standard: Checks for a mouse-click."""
        if sum([p.x for p in self.parents()]) + self.length > pos[0] > sum([p.x for p in self.parents()]) and \
                sum([p.y for p in self.parents()]) + self.height > pos[1] > sum([p.y for p in self.parents()]):
            self.text = [input2(self)]
            self.textInputted = copy.deepcopy(self.text)
            message.rendUpdate()
        if self.onReturn is not None:
            self.onReturn(self.text)


# noinspection PyShadowingNames
class CheckBox:
    def __init__(self, parent, x, y, colour=VC.Black, checked=True):
        """Creates a new CheckBox. Used for boolean user-entry."""
        self.parent = parent
        self.x = x
        self.y = y
        self.font = VC.MainFont
        self.colour = colour
        self.checked = checked

    def parents(self):
        """Standard: returns the parent list for the object."""
        o = self
        output = []
        while o is not VC:
            output.append(o)
            o = [o.parent][0]
        return output

    def render(self):
        """Renders the CheckBox to VC.Screen."""
        pygame.draw.rect(VC.Screen, VC.Black, pygame.Rect(sum([p.x for p in self.parents()]),
                                                          sum([p.y for p in self.parents()]),
                                                          20, 20), 2)
        if self.checked:
            pygame.draw.line(VC.Screen, VC.Black,
                             (sum([p.x for p in self.parents()]) + 4, sum([p.y for p in self.parents()]) + 4),
                             (sum([p.x for p in self.parents()]) + 16, sum([p.y for p in self.parents()]) + 16))
            pygame.draw.line(VC.Screen, VC.Black,
                             (sum([p.x for p in self.parents()]) + 4, sum([p.y for p in self.parents()]) + 16),
                             (sum([p.x for p in self.parents()]) + 16, sum([p.y for p in self.parents()]) + 4))

    def check_motion(self, pos):
        """Standard: Checks for mouse-motion"""
        pass

    def check_click(self, pos):
        """Standard: Checks for a mouse-click."""
        if sum([p.x for p in self.parents()]) + 20 > pos[0] > sum([p.x for p in self.parents()]) and \
                sum([p.y for p in self.parents()]) + 20 > pos[1] > sum([p.y for p in self.parents()]):
            self.checked = not self.checked


# noinspection PyShadowingNames
class FreqPanel:
    def __init__(self, parent, x, y, length, height):
        """Creates a new frequency panel - used to display the frequency information of the message."""
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def render(self):
        """Renders the existing information to VC.Screen."""
        pygame.draw.rect(VC.Screen, VC.White, pygame.Rect(self.x, self.y, self.length, self.height))
        c = 0
        if VC.alphaOrder:
            li = sorted(message.freqAnalysis, key=(lambda p: p[0]))
            el = sorted(englishLetterFrequencies, key=(lambda p: p[0]))[1:]
        else:
            li = message.freqAnalysis
            el = englishLetterFrequencies
        for letter, number, in li:
            plq = VC.SmallFont.render((letter + ' ' + str(number) + '    ')[:7] +
                                      el[c][0] + ' ' + el[c][1],
                                      False, VC.Black)
            VC.Screen.blit(plq, (self.x + 10, self.y + VC.lineWidth * c))
            if not c == 25:
                c += 1

    def check_click(self, pos):
        """Standard: Checks for mouse-clicks."""
        pass

    def check_motion(self, pos):
        """Standard: Checks for mouse-motion."""
        pass


# noinspection PyShadowingNames
class TrigPanel:
    def __init__(self, parent, x, y, length, height):
        """Creates a new trigram analysis panel. Used to display trigram analysis information."""
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def render(self):
        """Renders the trigram information to the screen."""
        pygame.draw.rect(VC.Screen, VC.White, pygame.Rect(self.x, self.y, self.length, self.height))
        if message.trigramAnalysis:
            for i, x in enumerate(message.trigramAnalysis):
                if i * VC.lineWidth < self.height:
                    plq = VC.SmallFont.render(x[0] + ' ' + x[1], False, VC.Black)
                    VC.Screen.blit(plq, (self.x + 5, self.y + 5 + (VC.lineWidth * i)))

    def check_click(self, pos):
        """Standard: Checks for mouse-clicks."""
        pass

    def check_motion(self, pos):
        """Standard: Checks for mouse-motion."""
        pass


class CustomButton:
    def __init__(self, x, y, picture, action):
        self.x = x
        self.y = y
        self.width = picture.get_rect()[2]
        self.height = picture.get_rect()[3]
        self.picture = picture
        self.action = action

    def render(self):
        VC.Screen.blit(self.picture, (self.x, self.y))

    def check_click(self, pos):
        if self.x + self.width > pos[0] > self.x:
            if self.y + self.height > pos[1] > self.y:
                self.action()

    def check_motion(self, pos):
        pass
