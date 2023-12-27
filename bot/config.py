from pylol.config import CONFIG


DISCORD_CONFIG = CONFIG["discord"]
DATABASE_CONFIG = CONFIG["database"]
LOGGING_CONFIG = CONFIG.get("logging") or {}
