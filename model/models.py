# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import pytz

Base = declarative_base()
metadata = Base.metadata


class Draft(Base):
    __tablename__ = 'draft'

    iddraft = Column(Integer, primary_key=True, nullable=False)
    player_idplayer = Column(ForeignKey('player.idplayer'), primary_key=True, nullable=False, index=True)
    team_idteam = Column(ForeignKey('team.idteam'), primary_key=True, nullable=True, index=True)
    edition = Column(String(45), nullable=False)
    game = Column(String(45), nullable=False)
    draftDate = Column(DateTime)
    finalDate = Column(DateTime)
    teamsQuantity = Column(Integer)
    playersPerTeam = Column(Integer)
    groupsQuantity = Column(Integer)
    teamsPerGroup = Column(Integer)
    isActive = Column(Integer)

    player = relationship('Player')
    team = relationship('Team')

    def to_dict(self):
        if self.team:
            return {
                'iddraft': self.iddraft,
                'player_idplayer': self.player_idplayer,
                'team_idteam': self.team_idteam,
                'edition': self.edition,
                'game': self.game,
                'draftDate': self.draftDate.isoformat() if self.draftDate else None,
                'finalDate': self.finalDate.isoformat() if self.finalDate else None,
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
                    'score_pingpong': self.player.score_pingpong,
                    'score_racing': self.player.score_racing,
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
        else:
            return {
            'iddraft': self.iddraft,
            'player_idplayer': self.player_idplayer,
            'team_idteam': self.team_idteam,
            'edition': self.edition,
            'game': self.game,
            'draftDate': self.draftDate.isoformat() if self.draftDate else None,
            'finalDate': self.finalDate.isoformat() if self.finalDate else None,
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
                'score_pingpong': self.player.score_pingpong,
                'score_racing': self.player.score_racing,
                },
            }


class Match(Base):
    __tablename__ = 'match'

    idmatch = Column(Integer, primary_key=True, nullable=False)
    team_idteam1 = Column(ForeignKey('team.idteam'), primary_key=True, nullable=False, index=True)
    team_idteam2 = Column(ForeignKey('team.idteam'), primary_key=True, nullable=False, index=True)
    draftEdition = Column(String(45))
    phase = Column(String(45))
    group = Column(Integer)
    format = Column(String(45))
    isDone = Column(Integer)
    isScheduled = Column(Integer)
    scheduledDate = Column(DateTime)
    winner = Column(String(45))
    scoreTeam1 = Column(String(45))
    scoreTeam2 = Column(String(45))
    freeSchedule = Column(Text)
    reschedule = Column(Text)
    confirmation = Column(Text)
    conclusionDate = Column(DateTime)

    team1 = relationship('Team', primaryjoin='Match.team_idteam1 == Team.idteam')
    team2 = relationship('Team', primaryjoin='Match.team_idteam2 == Team.idteam')

    def to_dict(self):
        def convert_to_brazilian_time(dt):
            if dt:
                brazil_tz = pytz.timezone('America/Sao_Paulo')
                return dt.astimezone(brazil_tz).isoformat()
            return None
        return {
            'idmatch': self.idmatch,
            'team_idteam1': self.team_idteam1,
            'team_idteam2': self.team_idteam2,
            'team1': self.team1.to_dict() if self.team1 else None,
            'team2': self.team2.to_dict() if self.team2 else None,
            'draftEdition': self.draftEdition,
            'phase': self.phase,
            'group': self.group,
            'format': self.format,
            'isDone': self.isDone,
            'isScheduled': self.isScheduled,
            'scheduledDate': convert_to_brazilian_time(self.scheduledDate),
            'reschedule': self.reschedule,
            'winner': self.winner,
            'scoreTeam1': self.scoreTeam1,
            'scoreTeam2': self.scoreTeam2,
            'freeSchedule': self.freeSchedule,
            'confirmation': self.confirmation,
            'conclusionDate': convert_to_brazilian_time(self.conclusionDate)
        }


class Player(Base):
    __tablename__ = 'player'

    idplayer = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(45), nullable=False)
    nick = Column(String(45))
    twitch = Column(String(45))
    email = Column(String(45))
    schedule = Column(Text)
    coins = Column(Integer)
    stars = Column(String(45))
    medal = Column(Integer)
    wins = Column(Integer)
    trophy = Column(Integer)
    gold = Column(Integer)
    silver = Column(Integer)
    bronze = Column(Integer)
    participations = Column(Integer)
    tags = Column(String(45))
    photo = Column(Text)
    mobile = Column(String(45))
    title = Column(String(45))
    level = Column(String(45))
    border = Column(String(45))
    bestTeam = Column(String(45))
    bestPlacement = Column(String(45))
    favoriteGame = Column(String(45))
    evaluations = Column(Integer)
    achievments = Column(Integer)
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
    score_pingpong = Column(Integer)
    score_racing = Column(Integer)

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
            'trophy': self.trophy,
            'gold': self.gold,
            'silver': self.silver,
            'bronze': self.bronze,
            'participations': self.participations,
            'tags': self.tags,
            'photo': self.photo,
            'mobile': self.mobile,
            'title': self.title,
            'level': self.level,
            'border': self.border,
            'bestTeam': self.bestTeam,
            'bestPlacement': self.bestPlacement,
            'favoriteGame': self.favoriteGame,
            'evaluations': self.evaluations,
            'achievments': self.achievments,
            'isCaptain': self.isCaptain,
            'isBackup': self.isBackup,
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
            'score_pingpong': self.score_pingpong,
            'score_racing': self.score_racing,
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
    auth = Column(String(45))

    def to_dict(self):
      return {
          'iduser': self.iduser,
          'name': self.name,
          'email': self.email,
          'creation_date': self.creation_date,
          'auth': self.auth
      }
    
class Notification(Base):
    __tablename__ = 'notification'

    idnotification = Column(Integer, primary_key=True)
    player_idplayer = Column(Integer, nullable=False)
    isRead = Column(Integer)
    text = Column(Text)
    link = Column(String(45))
    created = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
      return {
          'idnotification': self.idnotification,
          'player_idplayer': self.player_idplayer,
          'isRead': self.isRead,
          'text': self.text,
          'link': self.link,
          'created': self.created
      }

