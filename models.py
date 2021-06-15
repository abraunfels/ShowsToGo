from app import db

import enum

import sqlalchemy.types as types
from sqlalchemy import Column, Integer
from sqlalchemy.orm import composite
from sqlalchemy.ext.declarative import declarative_base


class Status(enum.Enum):
    one = 'past'
    two = 'denied'
    three = 'future'


class Seat(object):
    def __init__(self, row, place):
        self.row = row
        self.place = place

    def __composite_values__(self):
        return self.row, self.place

    def __repr__(self):
        return "Seat(row=%r, place=%r)" % (self.row, self.place)

    def __eq__(self, other):
        return isinstance(other, Seat) and \
            other.row == self.row and \
            other.place == self.place

    def __ne__(self, other):
        return not self.__eq__(other)

class Theatres(db.Model):
    __tablename__ = 'theatres'

    __searchable__ = ['name']

    theatreid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String())
    description = db.Column(db.Text)

    types = db.relationship('Types', secondary='theatrestypes', lazy='dynamic', backref=db.backref('Theatres'))

    halls = db.relationship('Halls', backref='Theatres')
    perfomances = db.relationship('Perfomances', lazy='dynamic', backref='Theatres')

    def __init__(self, name, address, img):
        self.name = name
        self.address = address
        self.img = img

    def __repr__(self):
        return {
            '<theatreid {}>'.format(self.theatreid),
        }


class Types(db.Model):
    __tablename__ = 'types'

    typeid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    theatres = db.relationship('Theatres', secondary='theatrestypes', lazy='dynamic', backref=db.backref('Types'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            '<typeid {}>'.format(self.typeid),
            'typename {}'.format(self.name)
        }

theatrestypes = db.Table('theatrestypes',
    db.Column('theatreid', db.Integer, db.ForeignKey('theatres.theatreid')),
    db.Column('typeid', db.Integer, db.ForeignKey('types.typeid'))
)

class Halls(db.Model):
    __tablename__ = 'halls'

    hallid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    theatreid = db.Column(db.Integer(), db.ForeignKey('theatres.theatreid'))

    db.UniqueConstraint('name', 'theatreid')

    perfomances = db.relationship('Perfomances', lazy='dynamic', backref='Halls')
    areas = db.relationship('Areas', backref = 'Halls')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.hallid)

class Perfomances(db.Model):
    __tablename__ = 'perfomances'

    perfomanceid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100))

    theatreid = db.Column(db.Integer(), db.ForeignKey('theatres.theatreid'))

    db.UniqueConstraint('name', 'theatreid')

    hallid = db.Column(db.Integer(), db.ForeignKey('halls.hallid'))

    genreid = db.Column(db.Integer(), db.ForeignKey('genres.genreid'))

    directorid = db.Column(db.Integer(), db.ForeignKey('directors.directorid'))

    rate = db.Column (db.Integer())
    synopsis = db.Column (db.Text())
    duration_min = db.Column(db.SmallInteger)

    actors = db.relationship('Actors', secondary='actorsperfomances', backref='Perfomances')
    subgenres = db.relationship('Subgenres', secondary='subgenresperfomances', backref=db.backref('Perfomances', lazy='dynamic'))

    shows = db.relationship ('Shows', lazy='dynamic', backref='Perfomances')
    comments = db.relationship ('Comments', lazy='dynamic', backref = 'Perfomances')

    def __init__(self, name, theatreid, hallid, rate, synopsis, duration_min):
        self.theatreid = theatreid
        self.hallid = hallid
        self.rate = rate
        self.synopsis = synopsis
        self.duration_min = duration_min

    def __repr__(self):
        return '<id {}>'.format(self.perfomanceid)

class Actors(db.Model):
    __tablename__ = 'actors'

    actorid = db.Column('actorid', db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(15), nullable=False)
    db.UniqueConstraint('name', 'surname')

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return '<id {}>'.format(self.actorid)


ActorsPerfomances = db.Table('actorsperfomances',
    db.Column('perfomanceid', db.Integer, db.ForeignKey('perfomances.perfomanceid')),
    db.Column('actorid', db.Integer, db.ForeignKey('actors.actorid'))
)

class Genres(db.Model):
    __tablename__ = 'genres'

    genreid = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(30), nullable=False, unique=True)

    perfomances = db.relationship('Perfomances', backref='Genres')
    #subgenres = db.relationship('Subgenres', backref='Genres')

    def __init__(self, name):
        self.name = name

class Subgenres(db.Model):
    __tablename__ = 'subgenres'

    subgenreid = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(30), nullable=False)

    parentid = db.Column(db.Integer, db.ForeignKey('genres.genreid'))

    perfomances = db.relationship('Perfomances', secondary='subgenresperfomances',
                                backref=db.backref('Subgenres', lazy='dynamic'))

    db.UniqueConstraint('parentid', 'name')

    def __init__(self, name):
        self.name = name

SubgenresPerfomances = db.Table ('subgenresperfomances',
    db.Column('perfomanceid', db.Integer, db.ForeignKey('perfomances.perfomanceid')),
    db.Column('subgenreid', db.Integer, db.ForeignKey('subgenres.subgenreid')))

class Shows(db.Model):
    __tablename__='shows'

    showid = db.Column(db.Integer, primary_key=True)

    perfomanceid = db.Column(db.Integer, db.ForeignKey('perfomances.perfomanceid'))

    tickets = db.relationship ('Ticket', backref = 'Shows')

    datetime = db.Column(db.DateTime)
    date = db.Column(db.Date)

    status = db.Column(db.Enum(Status))

    def __init__(self, perfomanceid, hallid, date, time):
        self.perfomanceid = perfomanceid
        self.hallid = hallid
        self.date = date
        self.time = time

class Areas(db.Model):
    __tablename__ = 'areas'

    areaid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    hallid = db.Column(db.Integer, db.ForeignKey('halls.hallid'))

    db.UniqueConstraint('areaid', 'name')

    rows = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)

    def __int__(self, name, hallid, rows, seats):
        self.name = name
        self.hallid = hallid

class Ticket(db.Model):
    __tablename__ = 'tickets'

    ticketid = db.Column(db.Integer, primary_key=True)
    guestname = db.Column(db.String(30))
    email = db.Column(db.String(30))

    showid = db.Column (db.Integer, db.ForeignKey('shows.showid'))
    areaid = db.Column(db.Integer, db.ForeignKey('areas.areaid'))

    def __init__(self, guestname, email, showid, areaid):
        self.guestname = guestname
        self.email = email
        self.showid = showid
        self.areaid = areaid


class SeatsForShow(db.Model):
    __tablename__ = 'seatsforshow'

    areaid = db.Column(db.Integer, db.ForeignKey('areas.areaid'))
    showid = db.Column(db.Integer, db.ForeignKey('shows.showid'))

    seatsforshowid = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer)
    place = db.Column(Integer)

    seat = composite(Seat, row, place)

    close = db.Column(db.Boolean())

    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.ticketid'))

    db.UniqueConstraint('row', 'place')

    def __init__(self, areaid, showid):
        self.areaid = areaid
        self.showid = showid


class Directors(db.Model):
    __tablename__ = 'directors'

    directorid = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(15), nullable=False)
    db.UniqueConstraint('name', 'surname')

    perfomances = db.relationship('Perfomances', backref='Directors')

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return '<id {}>'.format(self.directorid)

class Comments(db.Model):
    __tablename__ = 'comments'

    commentid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    text = db.Column(db.Text, nullable=False, unique=True)
    rate  = db.Column (db.SmallInteger)

    datetimecreated = db.Column (db.DateTime, nullable=False)

    perfomanceid = db.Column(db.Integer, db.ForeignKey('perfomances.perfomanceid'))

    def __init__(self, name, text, perfomanceid, datetimecreated):
        self.name = name
        self.perfomanceid = perfomanceid
        self.text = text
        #self.rate = rat
        self.datetimecreated = datetimecreated

class Costs(db.Model):
    __tablename__ = 'costs'

    costid = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.SmallInteger, nullable=False)

    showid = db.Column(db.Integer, db.ForeignKey('shows.showid'))
    areaid = db.Column(db.Integer, db.ForeignKey('areas.areaid'))

    db.UniqueConstraint('showid', 'areaid')

    def __int__(self, showid, areaid, cost):
        self.showid = showid
        self.hallid = areaid
        self.cost = cost

