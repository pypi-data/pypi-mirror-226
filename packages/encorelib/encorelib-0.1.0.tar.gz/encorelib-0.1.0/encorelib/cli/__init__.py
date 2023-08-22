from configparser import ConfigParser
from colorama import init
from .utils import *
from encorelib.datastructures.stack import Stack

init(
    autoreset=True,
)


class Text(object):

    def __init__(self,
                 text      : str,
                 alignment = 'center',
                 padding   = 0,
                 fill_char = ' ',
                 ) -> None:

        # Check inputs types and bounds
        assert isinstance(text, str),                    f"Text should be str instance, but it is {type(text)}"
        assert alignment in ('left', 'center', 'right'), f'Alignment can be only "left", "center" or "right", but received {alignment}'
        assert isinstance(padding, int),                 f"Padding should be int instance, but it is {type(padding)}"
        assert isinstance(fill_char, str),               f"Fill char should be str instance, but is is {type(fill_char)}"
        assert len(fill_char) == 1,                      f"Fill char shoud be one-symbol"

        # Save values in instance
        self.__lines     = text.split('\n')
        self.__alignment = alignment
        self.__fill_char = fill_char
        self.__padding   = padding


    def get_representation(self, width: int, colorscheme: ConfigParser) -> str:

        # Check inputs and bounds
        assert isinstance(width, int), f"Width should be int instance, but it is {type(width)}"
        assert width >= 0,             f"Width should be positive"

        # Process
        representation = ''
        for line in self.__lines:
            # Use padding
            if self.__padding >= 0:
                line = self.__fill_char * self.__padding + line
            else:
                line = line + self.__fill_char * (-self.__padding)

            # Use alignment
            if self.__alignment == 'left':
                line = line.ljust(width, self.__fill_char)

            elif self.__alignment == 'center':
                line = line.center(width, self.__fill_char)

            elif self.__alignment == 'right':
                line = line.rjust(width, self.__fill_char)


            # Use colors
            representation += termcolor.colored(
                text     = line,
                color    = colorscheme['information']['foreground'],
                on_color = 'on_' + colorscheme['information']['background'],
            )

        return representation


class Button(object):

    def __init__(self,
                 text             : str,
                 alignment        = 'center',
                 padding          = 0,
                 fill_char        = ' ',
                 callback         = echo('Main callback is not set'),
                 ) -> None:

        # Check inputs
        assert isinstance(text, str),                    f"Text should be str instance, but it is {type(text)}"
        assert alignment in ('left', 'center', 'right'), f"Alignment can be only 'left', 'center' or 'right', but received {alignment}"
        assert isinstance(padding, int),                 f"Padding should be int instance, but it is {type(padding)}"
        assert isinstance(fill_char, str),               f"Fill char should be str instance, but is is {type(fill_char)}"
        assert len(fill_char) == 1,                      f"Fill char shoud be one-symbol"

        # Save values in instance
        self.__fill_char        = fill_char
        self.__alignment        = alignment
        self.__callback         = callback
        self.__padding          = padding
        self.__text             = text
        ## State
        self.__is_active        = False
        self.__is_selected      = False


    def change_state(self) -> None:
        self.__is_active = bool((self.__is_active + 1) % 2)

    def change_selection(self) -> None:
        self.__is_selected = bool((self.__is_selected + 1) % 2)

    def get_state(self) -> bool:
        return self.__is_active

    def get_selection(self) -> bool:
        return self.__is_selected

    def get_callback(self):
        return self.__callback

    def get_representation(self, width: int, colorscheme: ConfigParser) -> str:
        res = self.__text

        # Case: current selection
        if self.__is_selected:
            res = termcolor.colored(
                text     = res,
                color    = colorscheme['current selection']['foreground'],
                on_color = 'on_' + colorscheme['current selection']['background'],
            )

        else:
            # Case: secondary highlyting
            if self.__is_active:
                res = termcolor.colored(
                    text     = res,
                    color    = colorscheme['selected']['foreground'],
                    on_color = 'on_' + colorscheme['selected']['background'],
                )
            else:
                res = termcolor.colored(
                    text     = res,
                    color    = colorscheme['not selected']['foreground'],
                    on_color = 'on_' + colorscheme['not selected']['background']
                )

        # Use alignment
        delta = len(res) - len(self.__text) - 1

        if self.__alignment == 'left':
            res = colored_ljust(
                text             = res,
                width            = width+delta,
                fill_char        = self.__fill_char,
                background_color = 'on_' + colorscheme['terminal']['background'],
                padding          = self.__padding
            )

        elif self.__alignment == 'center':
            res = colored_center(
                text             = res,
                width            = width+delta,
                fill_char        = self.__fill_char,
                background_color = 'on_' + colorscheme['terminal']['background'],
                padding          = self.__padding
            )

        elif self.__alignment == 'right':
            res = colored_rjust(
                text             = res,
                width            = width+delta,
                fill_char        = self.__fill_char,
                background_color = 'on_' + colorscheme['terminal']['background'],
                padding          = self.__padding
            )

        self.__is_selected = False
        return termcolor.colored(res, on_color='on_' + colorscheme['terminal']['background'])


class Keyboard(object):

    def __init__(self, *buttons, selection=1) -> None:

        # Check inputs
        assert isinstance(buttons, tuple),  f"Placeholder type should be list, but it is {type(buttons)}"
        assert isinstance(selection, int), f"Max Selection type should be int, but it is {type(selection)}"
        assert selection > 0,              f"Max Selection should be positive"

        # Save values in instance
        self.__buttons = buttons
        self.__selection = selection

    def select(self, row: int):
        self.__buttons[row].change_state()

    def highlight(self, row: int):
        self.__buttons[row].change_selection()

    def clear(self):
        for button in self.__buttons:
            if button.get_state():
                button.change_state()
            if button.get_selection():
                button.change_selection()

    def get_representation(self, width: int, colorscheme: ConfigParser) -> str:
        res = ''
        for button in self.__buttons:
            res += button.get_representation(width, colorscheme) + '\n'
        return res

    def get_selection(self) -> int:
        return self.__selection

    def enter(self) -> list:
        res = []
        for button in self.__buttons:
            if button.get_state():
                res.append(button.get_callback()())
        return res

    def __len__(self) -> int:
        return len(self.__buttons)


class Slide(object):

    def __init__(self, *text, keyboard = None) -> None:

        self.__text = text
        self.__keyboard = keyboard

    def update(self, width: int, colorscheme: ConfigParser) -> list:
        preview = []
        for text in self.__text:
            preview.append(text.get_representation(width, colorscheme))

        if self.__keyboard:
            preview.append(self.__keyboard.get_representation(width, colorscheme))

        return preview

    def clear(self):
        if self.__keyboard:
            self.__keyboard.clear()


    def run(self, width: int, height: int, colorscheme: ConfigParser):
        current_line = -1

        # get sizes of keypads
        selection = self.__keyboard.get_selection() if self.__keyboard else 0
        max_lines = len(self.__keyboard) if self.__keyboard else 0

        while True:
            resize_terminal(width, height)

            for line in self.update(width, colorscheme):
                print(line)

            ##############
            # Use keyboard
            ##############

            while True:
                if self.__keyboard:
                    key = get_key()

                    if key in ('BACKSPACE',):
                        return None

                    elif key == 'unknown':
                        continue

                    # Move up
                    elif key in ('W', 'UP_ARROW', 'KP_UP'):
                        current_line = (current_line - 1) % max_lines

                    # Move down
                    elif key in ('S', 'DOWN_ARROW', 'KP_DOWN'):
                        current_line = (current_line + 1) % max_lines

                    # Selected
                    elif key in ('SPACE',):
                        self.__keyboard.select(current_line)
                        if selection == 1:
                            return self.__keyboard.enter()[0]

                    # Entered
                    elif key in ('ENTER', 'KP_ENTER'):
                        if selection == 1:
                            self.__keyboard.select(current_line)
                        res = self.__keyboard.enter()
                        if len(res) == 0: continue
                        return res[0] if selection == 1 else res

                    # Highlight
                    self.__keyboard.highlight(current_line)
                else:
                    return [input('>>> ')]
                break


class Menu(object):

    def __init__(self, states: dict):

        # Check inputs
        assert isinstance(states, dict), f"States type should be dict, but it is {type(dict)}"

        # Save value in instance
        self.states = states

    def run(self, width: int, height: int, colorscheme: ConfigParser, entry_state='main',) -> list:

        clear_terminal()
        resize_terminal(width, height)
        color_terminal(
            foreground_color=colorscheme['terminal']['foreground'],
            background_color=colorscheme['terminal']['background'],
        )



        stack = Stack()
        stack.push(self.states[entry_state])

        while not stack.is_empty():
            top = stack.pop()
            result = top.run(width, height, colorscheme)
            if isinstance(result, list):
                color_terminal('white', 'black')
                return result

            elif isinstance(result, str):
                top.clear()
                self.states[result].clear()

                stack.push(top)
                stack.push(self.states[result])
