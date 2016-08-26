# -*- coding: utf-8 -*-
import urllib2
import BeautifulSoup
import datetime
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Cars(ndb.Model):
    link = ndb.TextProperty()
    name = ndb.TextProperty()
    year = ndb.IntegerProperty()
    probeg = ndb.TextProperty()
    cost = ndb.TextProperty()
    description = ndb.TextProperty()
    update = ndb.DateProperty(auto_now_add=True)

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
          </form>""")
        body = ''
        for k in pars.gopars(fromm, to):
            if k['link'] not in [s.link for s in carsold]:
                body += ('\n' + k['name'] + '; ' + k['year'] + '; ' + k['probeg'] + '; ' + str(k['cost']).replace('&nbsp;','') + '; ' + u''.join(k['description']).replace('&nbsp;', '') + '; ' + k['link'])
            cars = Cars(id=k['link'])
            self.response.out.write('<div>'+k['name']+'; '+k['year']+'; <b>'+k['probeg']+'</b>; <b>'+str(k['cost']).replace('&nbsp;','')+'</b>; '+u''.join(k['description']).replace('&nbsp;','')+'; <a href="'+k['link']+'">LINK</a></div>')
            cars.link = k['link']
            cars.name = k['name']
            cars.description = u''.join(k['description']).replace('&nbsp;', '')
            cars.year = int(k['year'])
            cars.probeg = k['probeg']
            cars.cost = str(k['cost']).replace('&nbsp;', '')
            cars.put()
        self.response.out.write('</body></html>')
        if body != '':
            mail.send_mail(sender="a260641139@gmail.com", to="a260641139@ya.ru", subject="New Cars List", body=body)

class DataBase(webapp2.RequestHandler):
    def get(self):
        cars = ndb.gql('SELECT * FROM Cars ORDER BY update DESC, year DESC')
        self.response.out.write("""<html><body>""")
        for k in cars:
            self.response.out.write('<div>'+k.name+'; '+str(k.year)+'; <b>'+k.probeg+'</b>; <b>'+str(k.cost).replace('&nbsp;','')+'</b>; '+u''.join(k.description).replace('&nbsp;','')+'; <a href="'+k.link+'">LINK</a> '+str(k.update)+'</div>')
        self.response.out.write('</body></html>')


class Parser():
    def __init__(self):
        self.cars = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.aver = 0

    def gopars(self, fromm, to):
        self.fromm = fromm
        self.to = to
        self.req = urllib2.Request(
            "https://moscow.auto.ru/cars/suzuki/sx4/used/?listing=listing&sort_offers=price-ASC&top_days=off&currency=RUR&output_type=list&image=true&is_clear=false&autoru_body_type%5B%5D=HATCHBACK&autoru_body_type%5B%5D=HATCHBACK_3_DOORS&autoru_body_type%5B%5D=HATCHBACK_5_DOORS&autoru_body_type%5B%5D=HATCHBACK_LIFTBACK&transmission_full%5B%5D=AUTO&transmission_full%5B%5D=AUTO_AUTOMATIC&transmission_full%5B%5D=AUTO_ROBOT&transmission_full%5B%5D=AUTO_VARIATOR&year_from=" + str(
                self.fromm) + "&year_to=" + str(
                self.to) + "&beaten=1&customs_state=1&price_from=350+000+%D1%80%D1%83%D0%B1.&price_to=700+000&dealer_org_type=4&page_num_offers=1")
        self.req.add_header("Cookie",
                            "counter_ga_all7=0; _ym_uid=1467713728461341335; geo_location=a%3A1%3A%7Bs%3A9%3A%22region_id%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A87%3B%7D%7D; gids=213; all7_user_region_confirmed=1; ___suid=f299f84215281adb4829f86dfae2c759.5539e823a26cb072847264a3f7c68272; suid=d95a7e58b5443ec36cdb2b022130e7ad.3b79f557e287d5f049e051b4636d39fe; gauto=3; autoru_sid=ce9eef0c4935430d_4989670596882e392817adf41ec383a1; autoruuid=2fb24c07d8b978b85aa859033843845d.0f431debbbef922fc26859c5acb9bce3; af_lpdid=19:163201659; _ym_isad=2; fuid01=5624f26e7e584bbc.3zS_hwoJqRLo5trf1KPZW4ULjWptv7OA9puPwTrnn9mK_rEszOOb_FEtgpnhdoAb2ikJ_osvZB_WZVYW5ndtURiozuSItpgvLykTOxA9vRAWE2I2xsEIcScbWkOVMlPt; yandexuid=8017545731445261934; dynamic_listing_tooltip=1; listing_view=%7B%22sort_offers%22%3A%22price-ASC%22%2C%22currency%22%3A%22RUR%22%2C%22output_type%22%3A%22list%22%2C%22image%22%3A%22true%22%7D; listing_view_session=%7B%22is_clear%22%3A%22false%22%2C%22top_days%22%3A%22off%22%7D; _ym_visorc_21407305=b; _ym_visorc_22753222=b; _ym_visorc_25353038=b; los=no; from_lifetime=1470902896205; from=direct")
        self.page = urllib2.urlopen(self.req)
        self.soup = BeautifulSoup.BeautifulSoup(self.page.read(), fromEncoding="utf-8")
        for t in self.soup.findAll("tr", {"class": "listing__row"}):
            for k in t.findAll("a",{"class": "link link_theme_auto listing-item__link link__control i-bem"}):
                self.cars.append(dict())
                self.cars[self.a]['name'] = k.next.next
                self.cars[self.a]['link'] = k['href']
                self.a+=1
            for k in t.findAll("div", {"class": "listing-item__description"}):
                self.cars[self.b]['description'] = u''.join(k.string)
                self.b +=1
            for k in t.findAll("div", {"class": "listing-item__year"}):
                self.cars[self.c]['year'] = k.string
                self.c += 1
            for k in t.findAll("div", {"class": "listing-item__km"}):
                self.cars[self.d]['probeg'] = k.string
                self.d += 1
            for k in t.findAll("div", {"class": "listing-item__price"}):
                self.cars[self.e]['cost'] = k.next
                self.e += 1
        print len(self.cars)

        self.msgs = ''
        for k in self.cars:
            s = str(k['cost']).replace('&nbsp;','')
            s = s.replace(' ', '')
            self.aver += int(s)
            self.msgs += ('\n'+k['name']+'; '+k['year']+'; '+k['probeg']+'; '+str(k['cost']).replace('&nbsp;','')+'; '+u''.join(k['description']).replace('&nbsp;','')+'; '+k['link'])
        print('\nAver cost: ' + str(self.aver / len(self.cars)))
        return self.cars

app = webapp2.WSGIApplication([
  ('/', MainPage),
    ('/db', DataBase)
], debug=True)