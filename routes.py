from collections import namedtuple
from flask import Flask, render_template, request

import babel
import babel.dates
import babel.languages

import datetime
import calendar

from app import app, db
from models import Theatres, Perfomances, Types, Shows, Genres, Subgenres, Halls, Actors, Directors, Comments, Areas, Costs, SeatsForShow, Ticket

@app.template_filter('datetime')
def format_datetime(value, format='medium'):
    if format == 'full':
        format="d MMMM y HH:mm"
    elif format == 'medium':
        format="dd.MM.y HH:mm"
    elif format == 'short':
        format ="d MMMM H:mm"
    return babel.dates.format_datetime(value, format, locale='ru')

@app.template_filter('date')
def format_datetime(value, format='medium'):
    if format == 'full':
        format="d MMMM y"
    elif format == 'medium':
        format="dd.MM.y"
    elif format == 'short':
        format ="d MMMM"
    return babel.dates.format_datetime(value, format, locale='ru')

@app.template_filter('month')
def format_datetime(value):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return months[value-1]

@app.template_filter('time')
def format_datetime(value):
    return babel.dates.format_datetime(value, "H:mm", locale='ru')

@app.route("/")
def index():
    try:
        perfomances=Perfomances.query.limit(3).all()
        pair = namedtuple('pair', 'perfomance theatre')
        dict = {}
        i=0
        for perfomance in perfomances:
            dict[i] = pair(perfomance, Theatres.query.get(perfomance.theatreid))
            i+=1

        theatres = Theatres.query.limit(3).all()
        return  render_template('index.html', perfomances=dict, theatres = theatres)

    except Exception as e:
	    return(str(e))

@app.route("/theatres")
def theatres():
    try:
        if request.method == "GET":
            type = request.args.get('type', '')
            if type == 'all':
                theatres = Theatres.query.all()
            else:
                theatres = Types.query.get(int(type)).theatres
            dict = {}
            pair = namedtuple('pair', 'theatre types')
            i=0
            for theatre in theatres:
                types = theatre.types
                dict[i] = pair(theatre, types)
                i+=1

            types = Types.query.all()
            return render_template('theatres.html', theatres=dict, types = types)

    except Exception as e:
        return (str(e))

def get_dict_by_type(type, subgenre):
    if subgenre == 'all':
        perfomances = Perfomances.query.filter_by(genreid = type).all()
    else:
        perfomances = Subgenres.query.get(int(subgenre)).perfomances
    dict = {}
    i = 0
    pair = namedtuple('pair', 'perfomance theatre closestshow')
    for perfomance in perfomances:
        shows = perfomance.shows.order_by(Shows.datetime)
        try:
            temp = list(filter(lambda x: x.date >= datetime.datetime.now().date(), shows))[0]
        except:
            temp = None
        dict[i] = pair(perfomance, Theatres.query.get(perfomance.theatreid), temp)
        i+=1

    return dict

def get_dict_by_theatre(theatreid):
    perfomances = Perfomances.query.filter_by(theatreid = theatreid).all()
    dict = {}
    i = 0
    pair = namedtuple('pair', 'perfomance theatre closestshow')
    for perfomance in perfomances:
        shows = perfomance.shows.order_by(Shows.datetime)
        try:
            temp = list(filter(lambda x: x.date >= datetime.datetime.now().date(), shows))[0]
        except:
            None
        dict[i] = pair(perfomance, Theatres.query.get(theatreid), temp)
        i+=1

    return dict

@app.route('/perfomances')
def perfomances():
    try:
        if request.method == "GET":
            subgenre = request.args.get('subgenre', '')
            dict = get_dict_by_type(1, subgenre)
            subgenres = Subgenres.query.filter_by(parentid = 1).all()
            return render_template('perfomances.html', dict=dict, typename = 'Спектакли', subgenres=subgenres)
    except Exception as e:
        return (str(e))

@app.route('/musics')
def musics():
    try:
        if request.method == "GET":
            subgenre = request.args.get('subgenre', '')
            dict = get_dict_by_type(9, subgenre)
            subgenres = Subgenres.query.filter_by(parentid = 9).all()
            return render_template('perfomances.html', dict=dict, typename='Мюзиклы', subgenres=subgenres)
    except Exception as e:
        return (str(e))

@app.route('/operas')
def operas():
    try:
        if request.method == "GET":
            subgenre = request.args.get('subgenre', '')
            dict = get_dict_by_type(8, subgenre)
            subgenres = Subgenres.query.filter_by(parentid = 8).all()
            return render_template('perfomances.html', dict=dict, typename="Оперы", subgenres=subgenres)
    except Exception as e:
        return (str(e))

@app.route('/shows')
def shows():
    try:
        if request.method == "GET":
            subgenre = request.args.get('subgenre', '')
            dict = get_dict_by_type(11, subgenre)
            subgenres = Subgenres.query.filter_by(parentid = 11).all()
            return render_template('perfomances.html', dict=dict, typename="Шоу", subgenres=subgenres)
    except Exception as e:
        return (str(e))


def get_theatre(theatreid):
    return Theatres.query.get_or_404(theatreid)

def get_perfomance(perfomanceid):
    return Perfomances.query.get_or_404(perfomanceid)

@app.route('/theatres/<int:theatreid>')
def theatre(theatreid):
    try:
        theatre = get_theatre(theatreid)
        dict = get_dict_by_theatre(theatreid)

        base = datetime.datetime.today()
        date_list = [base + datetime.timedelta(days=x) for x in range (
            calendar.monthrange(base.year, base.month)[1] - base.day + 1
            )]

        pair = namedtuple('pair', 'show perfomance hall genre')
        dateshowdict = dict.fromkeys(list(map (lambda x: x.date(), date_list)))
        for date in date_list:
            templist = list(map(lambda x: Shows.query.filter(Shows.perfomanceid == x.perfomanceid, Shows.date == date.date()).all(),
                         Perfomances.query.filter_by(theatreid = theatreid).all()))
            mylist = []
            for el in templist:
               mylist.extend(el)
            try:
                dateshowdict[date.date()].extend(list(map(lambda x: pair(x, Perfomances.query.get(x.perfomanceid), Halls.query.get(Perfomances.query.get(x.perfomanceid).hallid), Genres.query.get(Perfomances.query.get(x.perfomanceid).genreid)), mylist)))
            except Exception:
                dateshowdict[date.date()] = list(map(lambda x: pair(x, Perfomances.query.get(x.perfomanceid),
                                                                         Halls.query.get(Perfomances.query.get(
                                                                             x.perfomanceid).hallid), Genres.query.get(
                        Perfomances.query.get(x.perfomanceid).genreid)), mylist))

        #кусок кода который надо переписать да
        templist = list(
            map(lambda x: Shows.query.filter(Shows.perfomanceid == x.perfomanceid).all(),
                Perfomances.query.filter_by(theatreid=theatreid).all()))
        mylist = []
        for el in templist:
            mylist.extend(el)
        mylist.sort(key=lambda x: x.datetime)
        allshows = list(map(lambda x: pair(x, Perfomances.query.get(x.perfomanceid),
                                                                     Halls.query.get(
                                                                         Perfomances.query.get(x.perfomanceid).hallid),
                                                                     Genres.query.get(Perfomances.query.get(
                                                                         x.perfomanceid).genreid)), mylist))
        return render_template('theatre.html', theatre=theatre, dict=dict, date_list=date_list, dictshows = dateshowdict, allshows=allshows)
    except Exception as e:
        return (str(e))

@app.route('/perfomances/<int:perfomanceid>', methods=('POST', 'GET'))
def perfomance(perfomanceid):
    try:
        if request.method == 'POST':
           name = request.form['name']
           text = request.form['content']
           coment = Comments(name, text, perfomanceid, datetime.datetime.now())
           db.session.add(coment)
           db.session.commit()

        perfomance = get_perfomance(perfomanceid)
        subgenres = list(map(lambda x: Subgenres.query.get(x.subgenreid), perfomance.subgenres))
        actors = list(map(lambda x: Actors.query.get(x.actorid), perfomance.actors))

        anotherperfomances = Perfomances.query.filter_by(theatreid=perfomance.theatreid).limit(3)
        dict={}
        i=0
        pair = namedtuple('pair', 'perfomance closestshow')
        for el in anotherperfomances:
            shows = el.shows.order_by(Shows.datetime)
            try:
                temp - list(filter(lambda x: x.date >= datetime.datetime.now().date(), shows))[0]
            except:
                temp = None
            dict[i] = pair(el, temp)
            i += 1

        comments = Comments.query.with_parent(perfomance).all()

        shows1 = Shows.query.filter(Shows.perfomanceid == perfomance.perfomanceid).all()
        shows2 = list(filter(lambda x: x.date >= datetime.datetime.now().date(), shows1))
        shows2.sort(key=lambda x: x.datetime)

        hall = Halls.query.get(perfomance.hallid)

        areas = Areas.query.filter_by(hallid = perfomance.hallid).all()

        showareacost = {}
        areacost = namedtuple('areacost', 'area seats cost')
        for showw in shows2:
            for area in areas:
                try:
                    showareacost[showw.showid]
                except:
                    showareacost[showw.showid] = list()

                seatsforshowl = []
                for i in range(area.rows):
                    for j in range(area.seats):
                        seatsforshowl.append(SeatsForShow.query.filter_by(row=i+1, place=j+1, areaid=area.areaid, showid=showw.showid).first().close)
                showareacost[showw.showid].append(areacost(area, seatsforshowl,
                                                           Costs.query.filter(Costs.areaid == area.areaid,
                                                                                   Costs.showid == showw.showid).first()))



        return render_template('perfomance.html', perfomance=perfomance, theatre = Theatres.query.get(perfomance.theatreid),
                               genre=Genres.query.get(perfomance.genreid), director=Directors.query.get(perfomance.directorid),
                               subgenres = subgenres, actors=actors, dict=dict, comments=comments, shows=shows2, type=type,
                               hall = hall, areas=areas, showareacost=showareacost)
    except Exception as e:
        return (str(e))

@app.route('/ticket', methods=["POST"])
def ticket():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']

            row = request.form['row']
            place = request.form['place']

            showid = request.form['showid']
            areaid = request.form['areaid']
            show = Shows.query.get(showid)
            area = Areas.query.get(areaid)
            perfomance = Perfomances.query.get(show.perfomanceid)
            theatre = Theatres.query.get(perfomance.theatreid)
            ticket = Ticket(name, email, areaid, showid)
            db.session.add(ticket)
            db.session.commit()

            seat = db.session.query(SeatsForShow).filter(SeatsForShow.row==row, SeatsForShow.place==place, SeatsForShow.showid==showid, SeatsForShow.areaid==areaid).first()
            seat.close = True
            seat.ticketid = ticket.ticketid
            db.session.commit()

            return render_template('ticket.html', name=name, email=email, area=area, show=show, perfomance=perfomance,
                                   theatre=theatre, row=row, place=place)

            #if request.method == 'GET':
            #    abort(404)

    except Exception as e:
        return (str(e))

#index_service = IndexService(config=app.config)
#index_service.register_class(Theatres)

@app.route('/search', methods=["POST"])
def search():
    try:
        if request.method == 'POST':
            results = Theatres.search_query('Театр')
            return render_template('search.html')
    except Exception as e:
        return (str(e))

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена")