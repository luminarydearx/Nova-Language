from typing import Optional

class NovaConsole:
    END = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    @classmethod
    def print_logo(cls):
        logo = (
            f"{cls.BOLD}{cls.MAGENTA}"
            "  _   _           _              _         ____\n"
            " | \\ | | ___  ___(_) ___ _ __  (_) ___   |  _ \\\n"
            " |  \\| |/ _ \\/ __| |/ _ \\ '_ \\ | |/ _ \\  | |_) |\n"
            " | |\\  |  __/ (__| |  __/ | | || | (_) | |  __/\n"
            " |_| \\_|\\___|\\___|_|\\___|_| |_|/ |\\___/  |_|\n"
            "                              |__/\n"
            f"{cls.END}{cls.WHITE}Version 0.5.7 (Python Port){cls.END}\n"
            "        "
        )
        print(logo)

    @classmethod
    def info(cls, message: str):
        print(f"{cls.BLUE}[INFO]{cls.END} {message}")

    @classmethod
    def success(cls, message: str):
        print(f"{cls.GREEN}[SUCCESS]{cls.END} {message}")

    @classmethod
    def warning(cls, message: str):
        print(f"{cls.YELLOW}[WARNING]{cls.END} {message}")

    @classmethod
    def error(cls, message: str):
        print(f"{cls.RED}[ERROR]{cls.END} {message}")

    @classmethod
    def magenta(cls, text: str) -> str:
        return f"{cls.MAGENTA}{text}{cls.END}"

    @classmethod
    def green(cls, text: str) -> str:
        return f"{cls.GREEN}{text}{cls.END}"

    @classmethod
    def red(cls, text: str) -> str:
        return f"{cls.RED}{text}{cls.END}"

    @classmethod
    def blue(cls, text: str) -> str:
        return f"{cls.BLUE}{text}{cls.END}"

    @classmethod
    def cyan(cls, text: str) -> str:
        return f"{cls.CYAN}{text}{cls.END}"

    @classmethod
    def white(cls, text: str) -> str:
        return f"{cls.WHITE}{text}{cls.END}"

    @classmethod
    def bold(cls, text: str) -> str:
        return f"{cls.BOLD}{text}{cls.END}"
