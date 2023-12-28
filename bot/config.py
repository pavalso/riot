from pylol import Configuration, ApiConfiguration


class LoggingConfiguration(Configuration):
    configuration_file: str
    development_logger: str
    production_logger: str

class DatabaseConfiguration(Configuration):
    driver: Configuration
    drivers: dict[str, Configuration]

    def load(self, config: dict):
        super().load(config)
        _drivers = self.drivers
        self.drivers = {_d: Configuration().load(_c) for _d, _c in _drivers.items()}
        return self

class DiscordConfiguration(ApiConfiguration):
    prefix: str
    redirect_url: str
    intents: list
    embed: 'EmbedConfiguration'

    class EmbedConfiguration(Configuration):
        footer: str
        primary_color: int
        secondary_color: int
        error_color: int

    def load(self, _config: dict):
        super().load(_config)
        _embed = self.embed
        self.embed = self.EmbedConfiguration().load(_embed)
        return self

DISCORD_CONFIG = DiscordConfiguration()
DATABASE_CONFIG = DatabaseConfiguration()
LOGGING_CONFIG = LoggingConfiguration()

def load_configuration(config: dict):
    DISCORD_CONFIG.load(config.get("discord", {}))
    DATABASE_CONFIG.load(config.get("database", {}))
    LOGGING_CONFIG.load(config.get("logging", {}))
