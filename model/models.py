# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Draft(Base):
    __tablename__ = 'draft'

    iddraft = Column(Integer, primary_key=True, nullable=False)
    player_idplayer = Column(ForeignKey('player.idplayer'), primary_key=True, nullable=False, index=True)
    team_idteam = Column(ForeignKey('team.idteam'), primary_key=True, nullable=True, index=True)
    edition = Column(String(45), nullable=False)
    game = Column(String(45), nullable=False)
    draftdate = Column(DateTime)
    finaldate = Column(DateTime)
    teamsQuantity = Column(Integer)
    playersPerTeam = Column(Integer)
    groupsQuantity = Column(Integer)
    teamsPerGroup = Column(Integer)
    isActive = Column(Integer)

    player = relationship('Player')
    team = relationship('Team')

    def to_dict(self):
        return {
            'iddraft': self.iddraft,
            'player_idplayer': self.player_idplayer,
            'team_idteam': self.team_idteam,
            'edition': self.edition,
            'game': self.game,
            'draftdate': self.draftdate.isoformat() if self.draftdate else None,
            'finaldate': self.finaldate.isoformat() if self.finaldate else None,
            'teamsQuantity': self.teamsQuantity,
            'playersPerTeam': self.playersPerTeam,
            'groupsQuantity': self.groupsQuantity,
            'teamsPerGroup': self.teamsPerGroup,
            'isActive': self.isActive,
            'player': {
                'idplayer': self.player.idplayer,
                'name': self.player.name,
                'nick': self.player.nick,
                'twitch': self.player.twitch,
                'email': self.player.email,
                'schedule': self.player.schedule,
                'coins': self.player.coins,
                'stars': self.player.stars,
                'medal': self.player.medal,
                'wins': self.player.wins,
                'tags': self.player.tags,
                'photo': self.player.photo,
                'isCaptain': self.player.isCaptain,
                'riot': self.player.riot,
                'steam': self.player.steam,
                'epic': self.player.epic,
                'xbox': self.player.xbox,
                'psn': self.player.psn,
                'score_cs': self.player.score_cs,
                'score_valorant': self.player.score_valorant,
                'score_lol': self.player.score_lol,
                'score_rocketleague': self.player.score_rocketleague,
                'score_fallguys': self.player.score_fallguys,
                },
            'team': {
                'idteam': self.team.idteam,
                'name': self.team.name,
                'logo': self.team.logo,
                'wins': self.team.wins,
                'number': self.team.number,
                'group': self.team.group
                }
            }


class Match(Base):
    __tablename__ = 'match'

    idmatch = Column(Integer, primary_key=True, nullable=False)
    team_idteam1 = Column(ForeignKey('team.idteam'), primary_key=True, nullable=False, index=True)
    team_idteam2 = Column(ForeignKey('team.idteam'), primary_key=True, nullable=False, index=True)
    phase = Column(String(45))
    group = Column(Integer)
    format = Column(String(45))
    day = Column(String(45))
    hour = Column(String(45))
    isDone = Column(Integer)
    isScheduled = Column(Integer)
    score = Column(String(45))
    freeSchedule = Column(String(150))

    team = relationship('Team', primaryjoin='Match.team_idteam1 == Team.idteam')
    team1 = relationship('Team', primaryjoin='Match.team_idteam2 == Team.idteam')

    def to_dict(self):
        return {
            'idmatch': self.idmatch,
            'team_idteam1': self.team_idteam1,
            'team_idteam2': self.team_idteam2,
            'phase': self.phase,
            'group': self.group,
            'format': self.format,
            'day': self.day,
            'hour': self.hour,
            'isDone': self.isDone,
            'isScheduled': self.isScheduled,
            'score': self.score,
            'freeSchedule': self.freeSchedule
        }


class Player(Base):
    __tablename__ = 'player'

    idplayer = Column(Integer, primary_key=True, unique=True)
    name = Column(String(45), nullable=False)
    nick = Column(String(45))
    twitch = Column(String(45))
    email = Column(String(45))
    schedule = Column(String(150))
    coins = Column(Integer)
    stars = Column(String(45))
    medal = Column(Integer)
    wins = Column(Integer)
    tags = Column(String(45))
    photo = Column(String(150))
    isCaptain = Column(Integer)
    isBackup = Column(Integer)
    riot = Column(String(45))
    steam = Column(String(45))
    epic = Column(String(45))
    xbox = Column(String(45))
    psn = Column(String(45))
    score_cs = Column(Integer)
    score_valorant = Column(Integer)
    score_lol = Column(Integer)
    score_rocketleague = Column(Integer)
    score_fallguys = Column(Integer)

    def to_dict(self):
        return {
            'idplayer': self.idplayer,
            'name': self.name,
            'nick': self.nick,
            'twitch': self.twitch,
            'email': self.email,
            'schedule': self.schedule,
            'coins': self.coins,
            'stars': self.stars,
            'medal': self.medal,
            'wins': self.wins,
            'tags': self.tags,
            'photo': self.photo,
            'riot': self.riot,
            'steam': self.steam,
            'epic': self.epic,
            'xbox': self.xbox,
            'psn': self.psn,
            'score_cs': self.score_cs,
            'score_valorant': self.score_valorant,
            'score_lol': self.score_lol,
            'score_rocketleague': self.score_rocketleague,
            'score_fallguys': self.score_fallguys,
            'inEditions': self.inEditions
        }



class Team(Base):
    __tablename__ = 'team'

    idteam = Column(Integer, primary_key=True)
    name = Column(String(45))
    logo = Column(String)
    wins = Column(Integer)
    number = Column(Integer)
    group = Column(Integer)

    def to_dict(self):
        return {
            'idteam': self.idteam,
            'name': self.name,
            'logo': self.logo,
            'wins': self.wins,
            'number': self.number,
            'group': self.group
        }

class User(Base):
    __tablename__ = 'user'

    iduser = Column(Integer, primary_key=True)
    name = Column(String(45))
    email = Column(String(45))
    password = Column(String(45))
    creation_date = Column(DateTime)

    def to_dict(self):
      return {
          'iduser': self.iduser,
          'name': self.name,
          'email': self.email,
          'password': self.password,  # Note: You might want to exclude this for security reasons
          'creation_date': self.creation_date
      }

