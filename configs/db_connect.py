import os

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

APP_ENV = os.environ.get('APP_ENV', 'DEV')

from configs.env import config

engine = create_engine(
    f'postgresql://{config[APP_ENV]["DB_USER"]}:{config[APP_ENV]["DB_PASSWORD"]}@{config[APP_ENV]["DB_HOST"]}:5432/{config[APP_ENV]["DB_NAME"]}')

Base = declarative_base(engine)


########################################################################
class BookieBashingAccounts(Base):
    """"""
    __tablename__ = 'bets_bookiebashingaccounts'
    __table_args__ = {'autoload': True}


class BetAccounts(Base):
    """"""
    __tablename__ = 'bets_betaccounts'
    __table_args__ = {'autoload': True}


class BetWesites(Base):
    """"""
    __tablename__ = 'bets_betwebsites'
    __table_args__ = {'autoload': True}


class GlobalSettings(Base):
    """"""
    __tablename__ = 'bets_globalsettings'
    __table_args__ = {'autoload': True}


class Logs(Base):
    """"""
    __tablename__ = 'logs_logs'
    __table_args__ = {'autoload': True}


class ReportLogs(Base):
    """"""
    __tablename__ = 'logs_reportlogs'
    __table_args__ = {'autoload': True}


# ----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata.create_all()

    Session = sessionmaker(bind=engine, autoflush=True)
    session = Session()
    return session

