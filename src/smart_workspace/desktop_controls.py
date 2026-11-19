import pyautogui as pag

def minimize_window():
    """
    Minimizes the currently active window using the Command + M keyboard shortcut.
    """
    pag.hotkey('cmd', 'M')

def maximize_window():
    """
    Maximizes the currently active window using the Command + Control + F keyboard shortcut.
    """
    pag.hotkey('cmd', 'ctrl', 'f')

