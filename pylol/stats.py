from dataclasses import dataclass

from .common import PylolObject


@dataclass
class Stats(PylolObject):

    physicalDamageDealt: int = None
    visionScore: int = None
    goldSpent: int = None
    goldEarned: int = None
    totalHeal: int = None
    item3: int = None
    trueDamageDealt: int = None
    inhibitorKills: int = None
    champLevel: int = None
    damageDealtToTurrets: int = None
    visionWardsBoughtInGame: int = None
    detectorWardsPlaced: int = None
    consumablesPurchased: int = None
    killingSprees: int = None
    totalMinionsKilled: int = None
    spell1Casts: int = None
    objectivesStolenAssists: int = None
    spell4Casts: int = None
    physicalDamageTaken: int = None
    magicDamageDealt: int = None
    damageDealtToObjectives: int = None
    item4: int = None
    item5: int = None
    pentaKills: int = None
    largestKillingSpree: int = None
    bountyLevel: int = None
    firstTowerKill: bool = None
    champExperience: int = None
    firstBloodAssist: bool = None
    item6: int = None
    spell3Casts: int = None
    longestTimeSpentLiving: int = None
    damageDealtToBuildings: int = None
    tripleKills: int = None
    turretKills: int = None
    dragonKills: int = None
    firstTowerAssist: bool = None
    wardsPlaced: int = None
    nexusLost: int = None
    sightWardsBoughtInGame: int = None
    timeCCingOthers: int = None
    turretTakedowns: int = None
    wardsKilled: int = None
    item2: int = None
    baronKills: int = None
    trueDamageTaken: int = None
    deaths: int = None
    totalDamageTaken: int = None
    objectivesStolen: int = None
    totalHealsOnTeammates: int = None
    totalDamageDealt: int = None
    timePlayed: int = None
    totalTimeSpentDead: int = None
    firstBloodKill: bool = None
    unrealKills: int = None
    inhibitorsLost: int = None
    itemsPurchased: int = None
    physicalDamageDealtToChampions: int = None
    magicDamageTaken: int = None
    damageSelfMitigated: int = None
    spell2Casts: int = None
    largestMultiKill: int = None
    totalUnitsHealed: int = None
    item0: int = None
    assists: int = None
    nexusKills: int = None
    kills: int = None
    totalDamageShieldedOnTeammates: int = None
    summoner2Casts: int = None
    championTransform: int = None
    summoner1Casts: int = None
    totalDamageDealtToChampions: int = None
    neutralMinionsKilled: int = None
    item1: int = None
    trueDamageDealtToChampions: int = None
    quadraKills: int = None
    magicDamageDealtToChampions: int = None
    totalTimeCCDealt: int = None
    doubleKills: int = None
    turretsLost: int = None
    inhibitorTakedowns: int = None
    nexusTakedowns: int = None
    largestCriticalStrike: int = None
    kda: float = None
