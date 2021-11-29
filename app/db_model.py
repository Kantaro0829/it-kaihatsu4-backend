import sys
from typing import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, TEXT
from sqlalchemy.sql.expression import text, true
from setting import Base
from setting import ENGINE



class User(Base):
    """
    user テーブル用
    """
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    password = Column('password', String(255))
    mail = Column('email', String(200), unique=True)
    lang_id = Column('lang_id', Integer)

class Languages(Base):
    """
    Language テーブル用
    """

    __tablename__ = 'languages'
    lang_id = Column('lang_id', Integer, primary_key=True)
    lang_code = Column('lang_code', String(40), unique=True)
    lang_name = Column('lang_name', String(40), unique=True)

class History(Base):
    """
    History テーブル用
    """

    __tablename__ = "historys"
    data_id = Column('data_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    before_translation = Column('before_translation', TEXT)
    after_translation = Column('after_translation', TEXT)
    before_lang_code = Column('before_lang_code', String(40))
    after_lang_code = Column('after_lang_code', String(40))
    recoded_date = Column('recoded_date', Date)





def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)