# -*- coding: utf-8 -*-
import urllib2
import BeautifulSoup
import datetime
import webapp2
import logging
from google.appengine.ext import ndb
from google.appengine.api import mail


class Cars(ndb.Model):
    link = ndb.TextProperty()
    name = ndb.TextProperty()
    year = ndb.IntegerProperty()
    probeg = ndb.TextProperty()
    cost = ndb.TextProperty()
    description = ndb.TextProperty()
    update = ndb.DateProperty(auto_now_add=False)
    startdate = ndb.DateProperty(auto_now_add=False)

class MainPage(webapp2.RequestHandler):
    def get(self):
        carsold = ndb.gql('SELECT * FROM Cars')
        pars = Parser()
        fromm = self.request.get('from')
        to = self.request.get('to')
        self.response.out.write("""<html><body><form action="/" method="get">
            <div><textarea name="from" rows="1" cols="10"></textarea></div>
            <div><textarea name="to" rows="1" cols="10"></textarea></div>
            <div><input type="submit" value="YearChoose"></div>
            </form>
            <form action="/db" method="get">
            <div><input type="submit" value="DB"></div>
            </form>
            <table border='2' width ='100%'><tr><td>№</td><td>Модель</td><td>Год</td><td>Пробег</td><td>Цена</td><td>Описание</td><td>Ссылка на объявление</td></tr>""")
        body = ''
        n = 1
        for k in pars.gopars(fromm, to):
            if k['link'] not in [s.link for s in carsold]:
                car = Cars(id=k['link'])
                car.link = k['link']
                car.name = k['name']
                car.description = u''.join(k['description']).replace('&nbsp;', '')
                car.year = int(k['year'])
                car.probeg = k['probeg']
                car.cost = str(k['cost']).replace('&nbsp;', '')
                car.update = datetime.date.today()
                car.startdate = datetime.date.today()
                car.put()
                body += ('\n' + k['name'] + '; ' + k['year'] + '; ' + k['probeg'] + '; ' + str(k['cost']).replace('&nbsp;','') + '; ' + u''.join(k['description']).replace('&nbsp;', '') + '; ' + k['link'])
            else:
                car = Cars.get_by_id(k['link'])
                car.cost = str(k['cost']).replace('&nbsp;', '')
                car.update = datetime.date.today()
                car.put()
            self.response.out.write('<tr><td>'+str(n)+'</td><td>' + k['name'] + '</td><td>' + k['year'] + '</td><td>' + k['probeg'] + '</td><td>' + str(k['cost']).replace('&nbsp;', '') + '</td><td>' + u''.join(k['description']).replace('&nbsp;', '') + '</td><td><a href="' + k['link'] + '">LINK</a></td></tr>')
            n += 1
        self.response.out.write('</table></body></html>')
        if body != '':
            mail.send_mail(sender="a260641139@gmail.com", to="a260641139@ya.ru", subject="New Cars List", body=body)

class DataBase(webapp2.RequestHandler):
    def get(self):
        cars = ndb.gql('SELECT * FROM Cars ORDER BY update DESC, year DESC')
        self.response.out.write("""<html><body>
                                   <table border='2' width ='100%'><tr><td>№</td><td>Модель</td><td>Год</td><td>Пробег</td><td>Цена</td><td>Описание</td><td>Ссылка на объявление</td><td>Последнее обновление</td><td>Количество дней</td></tr>""")
        n = 1
        for k in cars:
            if k.update != datetime.date.today():
                self.response.out.write('<tr style="color: red"><td>'+str(n)+'</td><td>' + k.name + '</td><td>' + str(k.year) + '</td><td>' + k.probeg + '</td><td>' + str(k.cost).replace('&nbsp;', '') + '</td><td>' + u''.join(k.description).replace('&nbsp;', '') + '</td><td><a href="' + k.link + '">LINK</a></td><td>' + str(k.update) + '</td><td>' + str(k.update - k.startdate) + '</td></tr>')
            else:
                self.response.out.write('<tr style="color: green"><td>'+str(n)+'</td><td>' + k.name + '</td><td>' + str(k.year) + '</td><td>' + k.probeg + '</td><td>' + str(k.cost).replace('&nbsp;', '') + '</td><td>' + u''.join(k.description).replace('&nbsp;', '') + '</td><td><a href="' + k.link + '">LINK</a></td><td>' + str(k.update) + '</td><td>' + str(k.update - k.startdate) + '</td></tr>')
            n += 1
        self.response.out.write('</body></html>')


class Parser():
    def __init__(self):
        self.cars = []
        self.cars.append(dict())
        self.a = 0
        self.aver = 0

    def gopars(self, fromm, to):
        self.fromm = fromm
        self.to = to
        self.req = urllib2.Request("https://moscow.auto.ru/cars/suzuki/sx4/used/?listing=listing&sort_offers=price-ASC&top_days=off&currency=RUR&output_type=list&image=true&is_clear=false&autoru_body_type%5B%5D=HATCHBACK&autoru_body_type%5B%5D=HATCHBACK_3_DOORS&autoru_body_type%5B%5D=HATCHBACK_5_DOORS&autoru_body_type%5B%5D=HATCHBACK_LIFTBACK&transmission_full%5B%5D=AUTO&transmission_full%5B%5D=AUTO_AUTOMATIC&transmission_full%5B%5D=AUTO_ROBOT&transmission_full%5B%5D=AUTO_VARIATOR&year_from=" + str(self.fromm) + "&year_to=" + str(self.to) + "&beaten=1&customs_state=1&price_from=350+000+%D1%80%D1%83%D0%B1.&price_to=700+000&dealer_org_type=4&page_num_offers=1")
        #self.req.add_header("Cookie", "counter_ga_all7=0; _ym_uid=1467713728461341335; gauto=3; fuid01=5624f26e7e584bbc.3zS_hwoJqRLo5trf1KPZW4ULjWptv7OA9puPwTrnn9mK_rEszOOb_FEtgpnhdoAb2ikJ_osvZB_WZVYW5ndtURiozuSItpgvLykTOxA9vRAWE2I2xsEIcScbWkOVMlPt; dynamic_listing_tooltip=1; af_lpdid=19:163201659; listing_view=%7B%22sort_offers%22%3A%22price-ASC%22%2C%22currency%22%3A%22RUR%22%2C%22output_type%22%3A%22list%22%2C%22image%22%3A%22true%22%7D; listing_view_session=%7B%22is_clear%22%3A%22false%22%2C%22top_days%22%3A%22off%22%7D; geo_location=a%3A1%3A%7Bs%3A9%3A%22region_id%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A87%3B%7D%7D; all7_user_region_confirmed=1; nf--1524240667-w=1; nf--1524240667=1; spravka=dD0xNDcxMjYzNjE0O2k9ODIuMTQyLjE1OS44Mjt1PTE0NzEyNjM2MTQxNTQ2OTU2NDM7aD04MGEzMzkwYzBiMDRmYWYxYTUwYTM2NzRiMmY5YmFiMw==; ___suid=2ef8f223654316c9a1deb1db7e674856.5eeff7e21a2c7f22adb60ff01657f187; autoruuid=2fb24c07d8b978b85aa859033843845d.0f431debbbef922fc26859c5acb9bce3; suid=d95a7e58b5443ec36cdb2b022130e7ad.3b79f557e287d5f049e051b4636d39fe; search-save-flying-promo=1; autoru_sid=343a53d04b807345_63152d8733499190367db7833dd06a9f; _ym_isad=2; yandexuid=8017545731445261934; _ym_visorc_22753222=b; _ym_visorc_21407305=b; _ym_visorc_25353038=b; los=no; gids=213; from_lifetime=1472731726766; from=direct")
        self.page = urllib2.urlopen(self.req)
        self.soup = BeautifulSoup.BeautifulSoup(self.page.read(), fromEncoding="utf-8")
        logging.info(self.soup)
        for t in self.soup.findAll("tr", {"class": "listing__row"}):
            try:
                result = t.find("a", {"class": "link link_theme_auto listing-item__link link__control i-bem"})
                self.cars[self.a]['name'] = result.next.next
                self.cars[self.a]['link'] = result['href']
                result = t.find("div", {"class": "listing-item__description"})
                self.cars[self.a]['description'] = u''.join(result.string)
                result = t.find("div", {"class": "listing-item__year"})
                self.cars[self.a]['year'] = result.string
                result = t.find("div", {"class": "listing-item__km"})
                self.cars[self.a]['probeg'] = result.string
                result = t.find("div", {"class": "listing-item__price"})
                self.cars[self.a]['cost'] = result.next
                self.cars.append(dict())
                self.a += 1
            except:
                pass
        self.cars.__delitem__(len(self.cars) - 1)
        return self.cars

app = webapp2.WSGIApplication([
  ('/', MainPage),
    ('/db', DataBase)
], debug=True)