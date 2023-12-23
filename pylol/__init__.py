try:
    from pylol.config import init_key
    from pylol.bot import main as start_bot
except ImportError:
    from config import init_key


def main():
    init_key()
    start_bot()
