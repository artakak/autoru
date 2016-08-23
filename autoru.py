# -*- coding: utf-8 -*-
import urllib2
import BeautifulSoup
import datetime
from sqlalchemy_wrapper import SQLAlchemy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db = SQLAlchemy('sqlite:///auto.db')

class Cars(db.Model):
    auto_id = db.Column(db.String(100), primary_key=True)
    auto_name = db.Column(db.String(100), unique=False)
    auto_description = db.Column(db.String(200), unique=False)
    auto_year = db.Column(db.String(20), unique=False)
    auto_probeg = db.Column(db.String(20), unique=False)
    auto_cost = db.Column(db.String(20), unique=False)

    def __init__(self, auto_id, auto_name, auto_description, auto_year, auto_probeg, auto_cost):
        self.auto_id = auto_id
        self.auto_name = auto_name
        self.auto_description = auto_description
        self.auto_year = auto_year
        self.auto_probeg = auto_probeg
        self.auto_cost = auto_cost

    def __repr__(self):
        return '<Cars %r, %r>' % (self.auto_id, self.auto_name)

fromm = 2010
to = 2012
req = urllib2.Request("https://moscow.auto.ru/cars/suzuki/sx4/used/?listing=listing&sort_offers=price-ASC&top_days=off&currency=RUR&output_type=list&image=true&is_clear=false&autoru_body_type%5B%5D=HATCHBACK&autoru_body_type%5B%5D=HATCHBACK_3_DOORS&autoru_body_type%5B%5D=HATCHBACK_5_DOORS&autoru_body_type%5B%5D=HATCHBACK_LIFTBACK&transmission_full%5B%5D=AUTO&transmission_full%5B%5D=AUTO_AUTOMATIC&transmission_full%5B%5D=AUTO_ROBOT&transmission_full%5B%5D=AUTO_VARIATOR&year_from="+str(fromm)+"&year_to="+str(to)+"&beaten=1&customs_state=1&price_from=350+000+%D1%80%D1%83%D0%B1.&price_to=700+000&dealer_org_type=4&page_num_offers=1")
req.add_header("Cookie", "counter_ga_all7=0; _ym_uid=1467713728461341335; geo_location=a%3A1%3A%7Bs%3A9%3A%22region_id%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A87%3B%7D%7D; gids=213; all7_user_region_confirmed=1; ___suid=f299f84215281adb4829f86dfae2c759.5539e823a26cb072847264a3f7c68272; suid=d95a7e58b5443ec36cdb2b022130e7ad.3b79f557e287d5f049e051b4636d39fe; gauto=3; autoru_sid=ce9eef0c4935430d_4989670596882e392817adf41ec383a1; autoruuid=2fb24c07d8b978b85aa859033843845d.0f431debbbef922fc26859c5acb9bce3; af_lpdid=19:163201659; _ym_isad=2; fuid01=5624f26e7e584bbc.3zS_hwoJqRLo5trf1KPZW4ULjWptv7OA9puPwTrnn9mK_rEszOOb_FEtgpnhdoAb2ikJ_osvZB_WZVYW5ndtURiozuSItpgvLykTOxA9vRAWE2I2xsEIcScbWkOVMlPt; yandexuid=8017545731445261934; dynamic_listing_tooltip=1; listing_view=%7B%22sort_offers%22%3A%22price-ASC%22%2C%22currency%22%3A%22RUR%22%2C%22output_type%22%3A%22list%22%2C%22image%22%3A%22true%22%7D; listing_view_session=%7B%22is_clear%22%3A%22false%22%2C%22top_days%22%3A%22off%22%7D; _ym_visorc_21407305=b; _ym_visorc_22753222=b; _ym_visorc_25353038=b; los=no; from_lifetime=1470902896205; from=direct")
page = urllib2.urlopen(req)
soup = BeautifulSoup.BeautifulSoup(page.read(), fromEncoding="utf-8")

cars = []
a = 0
b = 0
c = 0
d = 0
e = 0
aver = 0
db.create_all()
for t in soup.findAll("tr", {"class": "listing__row"}):
    for k in t.findAll("a",{"class": "link link_theme_auto listing-item__link link__control i-bem"}):
        cars.append(dict())
        cars[a]['name'] = k.next.next
        cars[a]['link'] = k['href']
        a+=1
    for k in t.findAll("div", {"class": "listing-item__description"}):
        cars[b]['description'] = u''.join(k.string)
        b +=1
    for k in t.findAll("div", {"class": "listing-item__year"}):
        cars[c]['year'] = k.string
        c += 1
    for k in t.findAll("div", {"class": "listing-item__km"}):
        cars[d]['probeg'] = k.string
        d += 1
    for k in t.findAll("div", {"class": "listing-item__price"}):
        cars[e]['cost'] = k.next
        e += 1
print len(cars)

msgs = ''
for k in cars:
    s = str(k['cost']).replace('&nbsp;','')
    s = s.replace(' ', '')
    aver += int(s)
    print('\n'+k['name']+'; '+k['year']+'; '+k['probeg']+'; '+str(k['cost']).replace('&nbsp;','')+'; '+u''.join(k['description']).replace('&nbsp;','')+'; '+k['link'])
    if k['link'] not in [s.auto_id for s in db.query(Cars).order_by(Cars.auto_id)]:
        db.add(Cars(k['link'], k['name'], u''.join(k['description']).replace('&nbsp;',''), k['year'], k['probeg'], str(k['cost']).replace('&nbsp;','')))
        msgs += ('\n'+k['name']+'; '+k['year']+'; '+k['probeg']+'; '+str(k['cost']).replace('&nbsp;','')+'; '+u''.join(k['description']).replace('&nbsp;','')+'; '+k['link'])
    else:
        db.query(Cars).filter(Cars.auto_id == k['link']).update({'auto_cost': str(k['cost']).replace('&nbsp;','')+' upd '+str(datetime.date.today())})

db.commit()
print('\nAver cost: '+str(aver/len(cars)))
if msgs != '':
    fromaddr = "a260641139@ya.ru"
    toaddr = "a260641139@ya.ru"
    mypass = "aqua345SOFT"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "New Cars"

    msg.attach(MIMEText(msgs.encode('utf-8'), 'plain'))

    server = smtplib.SMTP('smtp.yandex.ru')
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
