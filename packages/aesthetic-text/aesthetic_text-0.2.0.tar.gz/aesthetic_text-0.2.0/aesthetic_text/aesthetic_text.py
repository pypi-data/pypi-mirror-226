# ------- Basic command ----
reset = "\033[0m"
clear_terminal = "\033[2J\033[H"

# ------- Style text -------
class style:
    bold = "\033[1m"
    dim = "\033[2m"
    italic = "\033[3m"
    underline = "\033[4m"
    highlight = "\033[7m"
    hidden = "\033[8m"
    strikethrough = "\033[9m"
    
# ------- Color text -------
class color:
    white = "\033[97m"
    grey = "\033[90m"
    black = "\033[30m"
    purple = "\033[95m"
    blue = "\033[94m"
    cyan = "\033[96m"
    green = "\033[92m"
    lime_green = "\033[38;5;46m"
    yellow = "\033[93m"
    red = "\033[91m"
    pink = "\033[38;5;206m"
    orange = "\033[38;5;208m"
    brown = "\033[38;5;130m"

class icon:
    check = "\033[38;5;46m✔\033[0m"
    cross = "\033[38;5;196m✘\033[0m"
    arrow_up = "\033[38;5;39m↑\033[0m"
    arrow_down = "\033[38;5;39m↓\033[0m"
    arrow_left = "\033[38;5;39m←\033[0m"
    arrow_right = "\033[38;5;39m→\033[0m"
    warning_sign = "\033[38;5;208m⚠\033[0m"
    no_entry_sign = "\033[38;5;196m⛔\033[0m"
    euro = "\033[38;5;226m€\033[0m"
    dollar = "\033[38;5;226m$\033[0m"
    pending = "\033[38;5;226m⏳\033[0m"
    infinity = "\033[38;5;226m∞\033[0m"
    reminder = "\033[38;5;226m⏰\033[0m"
    info = "\033[38;5;226mℹ\033[0m"
    add = "\033[37m✚\033[0m"
    remove = "\033[38;5;196m−\033[0m"