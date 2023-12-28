from typing import Any

import gspread

from pylol.config import RIOT_CONFIG

from bot.dbdrivers.mongodb import MongoDBDriver


class GSheetsMongoDBDriver(MongoDBDriver):

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.gc = gspread.service_account(filename=self._config["credentials_path"])
        self.wk = self.gc.open_by_key(self._config["spreadsheet_id"])

        self.aux_headers = ["id"]
        self.match_headers = RIOT_CONFIG["params"]["match"]
        self.aux_headers.extend(self.match_headers)

        self.match_sheet = self._get_sheet("matches", self.aux_headers)

        self.player_headers = ["player_id", "match_id", "champion", "team_position"]
        self.stats_headers = RIOT_CONFIG["params"]["stats"]
        self.player_headers.extend(self.stats_headers)

        self.players_sheet = self._get_sheet("players", self.player_headers)

        self.__version__ = f"{gspread.__version__}+{super().__version__}"

    def _get_sheet(self, sheet_name, headers: list[str] = None):
        try:
            ws = self.wk.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            ws = self.wk.add_worksheet(sheet_name, 1000, len(headers))

        ws.delete_row(1)
        ws.insert_row(headers)

        return ws

    def _format_data(self, _id: str, data: dict[str, Any]) -> (list, list):
        stats = []

        for player_id, player in data.get("players").items():
            buf = []
            buf.extend([player_id, _id, player.get("champion"), player.get("team_position")])
            buf.extend([player["stats"].get(stat) for stat in self.stats_headers])
            stats.append(buf)

        match = [_id]
        match.extend([data.get("match").get(param) for param in self.match_headers])

        return match, stats

    def insert(self, _id: Any, _data: dict[str, Any]):
        if not super().insert(_id, _data):
            return False
        match, stats = self._format_data(_id, _data)
        self.match_sheet.append_row(match)
        self.players_sheet.append_rows(stats)
        return True

def setup(config: dict) -> GSheetsMongoDBDriver:
    return GSheetsMongoDBDriver(config)
