#!/usr/bin/env python3

from urllib.request import urlopen
from utils.t_convert import C_to_F, C_to_K
import re
import time
import os

data = [
    "http://www.gismeteo.com", # url
    "http://www.gismeteo.com/city/daily/<b>1234</b>", # example
    "<b>1234</b>", #code
    { 
        'com': 'English',
        'ru': 'Русский',
        'ua/ua': 'Український',
        'lv': 'Latvijas',
        'lt': 'Lietuviškai',
        'md/ro': 'Română'
    }, # dict_weather_lang
    ('com', 'ru', 'ua/ua', 'lv', 'lt', 'md/ro') # weather_lang_list
]
max_days = 12
# weather variables
city_name = []
t_now = []
wind_speed_now = []
wind_direct_now = []
icon_now = []
icon_wind_now = []
time_update = []
text_now = []
press_now = []
hum_now = []
t_water_now = []

t_night = []
t_night_feel = []
day = []
date = []
t_day = []
t_day_feel = []
icon = []
icon_wind = []
wind_speed = []
wind_direct = []
text = []

t_tomorrow = []
t_tomorrow_feel = []
icon_tomorrow = []
wind_speed_tom = []
wind_direct_tom = []

t_today = []
t_today_feel = []
icon_today = []
wind_speed_tod = []
wind_direct_tod = []
chance_of_rain = []
t_today_low=[]
t_tomorrow_low=[]

dict_icons = {
    "d.sun.png": "32.png",

    "d.sun.c1.png": "34.png",
    "d.sun.c2.png": "30.png",
    "d.sun.c3.png": "28.png",
    "d.sun.c4.png": "26.png",

    "d.sun.c1.s1.png": "41.png",
    "d.sun.c1.s2.png": "41.png",
    "d.sun.c1.s3.png": "41.png",
    "d.sun.c1.s4.png": "41.png",
    "d.sun.c2.s1.png": "41.png",
    "d.sun.c2.s2.png": "41.png",
    "d.sun.c2.s3.png": "41.png",
    "d.sun.c2.s4.png": "41.png",
    "d.sun.c3.s1.png": "41.png",
    "d.sun.c3.s2.png": "41.png",
    "d.sun.c3.s3.png": "41.png",
    "d.sun.c3.s4.png": "41.png",
    "d.sun.c4.s1.png": "13.png",
    "d.sun.c4.s2.png": "14.png",
    "d.sun.c4.s3.png": "16.png",
    "d.sun.c4.s4.png": "16.png",

    "d.sun.c1.r1.png": "39.png",
    "d.sun.c1.r2.png": "39.png",
    "d.sun.c1.r3.png": "39.png",
    "d.sun.c1.r4.png": "40.png",
    "d.sun.c2.r1.png": "39.png",
    "d.sun.c2.r2.png": "39.png",
    "d.sun.c2.r3.png": "39.png",
    "d.sun.c2.r4.png": "40.png",
    "d.sun.c3.r1.png": "39.png",
    "d.sun.c3.r2.png": "39.png",
    "d.sun.c3.r3.png": "39.png",
    "d.sun.c3.r4.png": "40.png",
    "d.sun.c4.r1.png": "11.png",
    "d.sun.c4.r2.png": "40.png",
    "d.sun.c4.r3.png": "40.png",
    "d.sun.c4.r4.png": "40.png",

    "d.sun.c1.r1.st.png": "37.png",
    "d.sun.c1.r2.st.png": "37.png",
    "d.sun.c1.r3.st.png": "37.png",
    "d.sun.c1.r4.st.png": "37.png",
    "d.sun.c2.r1.st.png": "37.png",
    "d.sun.c2.r2.st.png": "37.png",
    "d.sun.c2.r3.st.png": "37.png",
    "d.sun.c2.r4.st.png": "37.png",
    "d.sun.c3.r1.st.png": "37.png",
    "d.sun.c3.r2.st.png": "37.png",
    "d.sun.c3.r3.st.png": "37.png",
    "d.sun.c3.r4.st.png": "37.png",
    "d.sun.c4.r1.st.png": "35.png",
    "d.sun.c4.r2.st.png": "35.png",
    "d.sun.c4.r3.st.png": "35.png",
    "d.sun.c4.r4.st.png": "35.png",

    "d.sun.c1.s1.st.png": "35.png",
    "d.sun.c1.s2.st.png": "35.png",
    "d.sun.c1.s3.st.png": "35.png",
    "d.sun.c1.s4.st.png": "35.png",
    "d.sun.c2.s1.st.png": "35.png",
    "d.sun.c2.s2.st.png": "35.png",
    "d.sun.c2.s3.st.png": "35.png",
    "d.sun.c2.s4.st.png": "35.png",
    "d.sun.c3.s1.st.png": "35.png",
    "d.sun.c3.s2.st.png": "35.png",
    "d.sun.c3.s3.st.png": "35.png",
    "d.sun.c3.s4.st.png": "35.png",
    "d.sun.c4.s1.st.png": "35.png",
    "d.sun.c4.s2.st.png": "35.png",
    "d.sun.c4.s3.st.png": "35.png",
    "d.sun.c4.s4.st.png": "35.png",

    "n.moon.png": "31.png",
    "n.moon.c1.png": "33.png",
    "n.moon.c2.png": "29.png",
    "n.moon.c3.png": "27.png",
    "n.moon.c4.png": "26.png",

    "n.moon.c1.s1.png": "46.png",
    "n.moon.c1.s2.png": "46.png",
    "n.moon.c1.s3.png": "46.png",
    "n.moon.c1.s4.png": "46.png",
    "n.moon.c2.s1.png": "46.png",
    "n.moon.c2.s2.png": "46.png",
    "n.moon.c2.s3.png": "46.png",
    "n.moon.c2.s4.png": "46.png",
    "n.moon.c3.s1.png": "46.png",
    "n.moon.c3.s2.png": "46.png",
    "n.moon.c3.s3.png": "46.png",
    "n.moon.c3.s4.png": "46.png",
    "n.moon.c4.s1.png": "13.png",
    "n.moon.c4.s2.png": "15.png",
    "n.moon.c4.s3.png": "16.png",
    "n.moon.c4.s4.png": "16.png",

    "n.moon.c1.r1.png": "45.png",
    "n.moon.c1.r2.png": "45.png",
    "n.moon.c1.r3.png": "45.png",
    "n.moon.c1.r4.png": "40.png",
    "n.moon.c2.r1.png": "45.png",
    "n.moon.c2.r2.png": "45.png",
    "n.moon.c2.r3.png": "45.png",
    "n.moon.c2.r4.png": "40.png",
    "n.moon.c3.r1.png": "45.png",
    "n.moon.c3.r2.png": "45.png",
    "n.moon.c3.r3.png": "45.png",
    "n.moon.c3.r4.png": "40.png",
    "n.moon.c4.r1.png": "11.png",
    "n.moon.c4.r2.png": "40.png",
    "n.moon.c4.r3.png": "40.png",
    "n.moon.c4.r4.png": "40.png",

    "n.moon.c1.r1.st.png": "47.png",
    "n.moon.c1.r2.st.png": "47.png",
    "n.moon.c1.r3.st.png": "47.png",
    "n.moon.c1.r4.st.png": "47.png",
    "n.moon.c2.r1.st.png": "47.png",
    "n.moon.c2.r2.st.png": "47.png",
    "n.moon.c2.r3.st.png": "47.png",
    "n.moon.c2.r4.st.png": "47.png",
    "n.moon.c3.r1.st.png": "47.png",
    "n.moon.c3.r2.st.png": "47.png",
    "n.moon.c3.r3.st.png": "47.png",
    "n.moon.c3.r4.st.png": "47.png",
    "n.moon.c4.r1.st.png": "35.png",
    "n.moon.c4.r2.st.png": "35.png",
    "n.moon.c4.r3.st.png": "35.png",
    "n.moon.c4.r4.st.png": "35.png",

    "n.moon.c1.s1.st.png": "47.png",
    "n.moon.c1.s2.st.png": "47.png",
    "n.moon.c1.s3.st.png": "47.png",
    "n.moon.c1.s4.st.png": "47.png",
    "n.moon.c2.s1.st.png": "47.png",
    "n.moon.c2.s2.st.png": "47.png",
    "n.moon.c2.s3.st.png": "47.png",
    "n.moon.c2.s4.st.png": "47.png",
    "n.moon.c3.s1.st.png": "47.png",
    "n.moon.c3.s2.st.png": "47.png",
    "n.moon.c3.s3.st.png": "47.png",
    "n.moon.c3.s4.st.png": "47.png",
    "n.moon.c4.s1.st.png": "35.png",
    "n.moon.c4.s2.st.png": "35.png",
    "n.moon.c4.s3.st.png": "35.png",
    "n.moon.c4.s4.st.png": "35.png",
    
    "d.sun.c1.st.png": "38.png",
    "d.sun.c2.st.png": "38.png",
    "d.sun.c3.st.png": "38.png",
    "d.sun.c4.st.png": "35.png",
    "n.moon.c1.st.png": "47.png",
    "n.moon.c2.st.png": "47.png",
    "n.moon.c3.st.png": "47.png",
    "n.moon.c4.st.png": "35.png",
    "d.mist.png": "22.png",
    "d.mist.r1.png": "22.png",
    "d.mist.r2.png": "22.png",
    "d.mist.r3.png": "22.png",
    "d.mist.r4.png": "22.png",
    "n.mist.png": "21.png",
    "n.mist.r1.png": "21.png",
    "n.mist.r2.png": "21.png",
    "n.mist.r3.png": "21.png",
    "n.mist.r4.png": "21.png"
}

def convert(icon, icons_name):
    try:
        icon_converted = dict_icons[os.path.split(icon)[1]]
    except:
        icon_converted = os.path.split(icon)[1]
    return icon+';'+icon_converted

def get_city_name(c_id, weather_lang):
    try:
        source = urlopen('http://www.gismeteo.%s/city/weekly/'%weather_lang + str(c_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        c_name = re.findall('type[A-Z].*\">(.*)<', source)
    except:
        print ('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]

def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name):
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod
    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))
    print ('\033[34m>\033[0m '+_('Downloading')+' '+'http://www.gismeteo.%s/city/weekly/'%weather_lang + str(city_id))
    try:
        source = urlopen('http://www.gismeteo.%s/city/weekly/'%weather_lang + str(city_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        print ('\033[1;32mOK\033[0m')
    except:
        print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
        if timer_bool:
            print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
        return False
    #### current weather ####
    w_now = re.findall("type[A-Z].*wrap f_link", source, re.DOTALL)
    
    # city
    city_name = re.findall('type[A-Z].*\">(.*)<', w_now[0])

    # temperature
    t_now = re.findall('m_temp c.>([&minus;+]*\d+)<', w_now[0])
    for i in range(len(t_now)):
        if t_now[i][0] == '&':
            t_now[i] = '-' + t_now[i][7:]
    t_now[0] = t_now[0]+'°;'+t_now[0]+'°;'+C_to_F(t_now[0])+'°;'+C_to_F(t_now[0])+'°;'+C_to_K(t_now[0])+';'+C_to_K(t_now[0])

    # wind
    wind_speed_now = re.findall('m_wind ms.*>(\d+)<', w_now[0])
    if wind_speed_now:
        wind_speed_now[0] = wind_speed_now[0]+' m/s;'+str(round(int(wind_speed_now[0])*3.6))+' km/h;'+str(round(int(wind_speed_now[0])*2.237))+' mph'
    wind_direct_now = re.findall('>(.+)</dt', w_now[0])
    wind_direct_now[0] = wind_direct_now[1]

    # icon
    icon_now = re.findall('url\((.*?new\/.+)\)', w_now[0])
    icon_now[0] = convert(icon_now[0], icons_name)
    
    # wind icon
    icon_wind_now = re.findall('wind(\d)', w_now[0])
    if icon_wind_now[0] == '0':
        icon_wind_now[0] = 'None'
    else:
        icon_wind_now[0] = int(icon_wind_now[0])*45+45

    # update time
    time_update = re.findall('data-hr.* (\d?\d:\d\d)\s*</span>', source, re.DOTALL)
    
    # weather text now
    text_now = re.findall('title=\"(.*?)\"', w_now[0])
    
    # pressure now
    press_now = re.findall('m_press torr\'>(\d+)<', w_now[0])
    if press_now:
        press_now[0] = press_now[0]+' mmHg;'+str(round(int(press_now[0])/25.4))+' inHg;'+str(round(int(press_now[0])*1.333))+' hPa'
    
    # humidity now
    hum_now = re.findall('wicon hum".*>(\d+)<span class="unit"', w_now[0])
    
    # water temperature now
    try:
        t_water_now = t_now[1]+';'+str(int(C_to_F(t_now[1])))+';'+C_to_K(t_now[1])
    except:
        pass
    
    #### weather to several days ####
    # all days
    w_all_list = re.findall('tbwdaily1.*?rframe wblock wdata', source, re.DOTALL)
    w_all = '\n'.join(w_all_list)
    t_all = re.findall('m_temp c.>([&minus;+]*\d+)<', w_all)
    for i in range(len(t_all)):
        if t_all[i][0] == '&':
            t_all[i] = '-' + t_all[i][7:]
    # all temperature
    t = t_all[::2]
    # all temperature as feel
    t_feel = t_all[1::2]

    # night temperature
    t_night = t[::4]
    t_night_feel = t_feel[::4]
    for i in range(len(t_night)):
        t_night[i] = t_night[i]+'°;'+t_night_feel[i]+'°;'+C_to_F(t_night[i])+'°;'+C_to_F(t_night_feel[i])+'°;'+C_to_K(t_night[i])+';'+C_to_K(t_night_feel[i])
    
    # day of week, date
    day = re.findall('weekday.>(.*?)<', source)
    date = re.findall('s_date.>(.*?)<', source)

    # day temperature
    t_day = t[2::4]
    t_day_feel = t_feel[2::4]
    for i in range(len(t_day)):
        t_day[i] = t_day[i]+'°;'+t_day_feel[i]+'°;'+C_to_F(t_day[i])+'°;'+C_to_F(t_day_feel[i])+'°;'+C_to_K(t_day[i])+';'+C_to_K(t_day_feel[i])
    
    # weather icon day
    icons_list = re.findall('src=\"(.*?new\/.*?)\"', w_all)
    icon = icons_list[2::4]
    for i in range(len(icon)):
        icon[i] = convert(icon[i], icons_name)
    
    # wind icon
    icon_wind_list = re.findall('wind(\d)', w_all)
    icon_wind = icon_wind_list[2::4]
    
    # wind
    wind_speed_list = re.findall('m_wind ms.>(\d+)', w_all)
    wind_speed = wind_speed_list[2::4]
    if wind_speed:
        for i in range(len(wind_speed)):
            wind_speed[i] = wind_speed[i]+' m/s;'+str(round(int(wind_speed[i])*3.6))+' km/h;'+str(round(int(wind_speed[i])*2.237))+' mph'
    wind_direct_list = re.findall('>(.+)</dt', w_all)
    wind_direct = wind_direct_list[2::4]
    for i in range(len(wind_direct)):
        wind_direct[i] = wind_direct[i].split('>')[-1]


    # weather text
    text_list = re.findall('cltext.>(.*?)<', w_all)
    text = text_list[2::4]

    if show_block_tomorrow:
        #### weather tomorrow ####
        try:
            w_tomorrow = w_all_list[1]
        except:
            if timer_bool:
                print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
            return False
        
        # temperature
        t_tomorrow = t[4:8]
        t_tomorrow_feel = t_feel[4:8]
        for i in range(len(t_tomorrow)):
            t_tomorrow[i] = t_tomorrow[i]+'°;'+t_tomorrow_feel[i]+'°;'+C_to_F(t_tomorrow[i])+'°;'+C_to_F(t_tomorrow_feel[i])+'°;'+C_to_K(t_tomorrow[i])+';'+C_to_K(t_tomorrow_feel[i])
        a = t_tomorrow[0]
        del t_tomorrow[0]
        t_tomorrow.append(a)
        # weather icon
        icon_tomorrow = re.findall('src=\"(.*?new\/.*?)\"', w_tomorrow)
        for i in range(len(icon_tomorrow)):
            icon_tomorrow[i] = convert(icon_tomorrow[i], icons_name)
        a = icon_tomorrow[0]
        del icon_tomorrow[0]
        icon_tomorrow.append(a)
        # wind
        wind_speed_tom = re.findall('m_wind ms.>(\d+)', w_tomorrow)
        if wind_speed_tom:
            for i in range(len(wind_speed_tom)):
                wind_speed_tom[i] = wind_speed_tom[i]+' m/s;'+str(round(int(wind_speed_tom[i])*3.6))+' km/h;'+str(round(int(wind_speed_tom[i])*2.237))+' mph'
        a = wind_speed_tom[0]
        del wind_speed_tom[0]
        wind_speed_tom.append(a)
        wind_direct_tom = re.findall('>(.+)</dt', w_tomorrow)
        for i in range(len(wind_direct_tom)):
            wind_direct_tom[i] = wind_direct_tom[i].split('>')[-1]
        a = wind_direct_tom[0]
        del wind_direct_tom[0]
        wind_direct_tom.append(a)
        
    if show_block_today:
        #### weather today ####
        w_today = w_all_list[0]
        # temperature
        t_today = t[0:4]
        t_today_feel = t_feel[0:4]
        for i in range(len(t_today)):
            t_today[i] = t_today[i]+'°;'+t_today_feel[i]+'°;'+C_to_F(t_today[i])+'°;'+C_to_F(t_today_feel[i])+'°;'+C_to_K(t_today[i])+';'+C_to_K(t_today_feel[i])
        a = t_today[0]
        del t_today[0]
        t_today.append(a)
        # weather icon
        icon_today = re.findall('src=\"(.*?new\/.*?)\"', w_today)
        for i in range(len(icon_today)):
            icon_today[i] = convert(icon_today[i], icons_name)
        a = icon_today[0]
        del icon_today[0]
        icon_today.append(a)
        # wind
        wind_speed_tod = re.findall('m_wind ms.>(\d+)', w_today)
        if wind_speed_tod:
            for i in range(len(wind_speed_tod)):
                wind_speed_tod[i] = wind_speed_tod[i]+' m/s;'+str(round(int(wind_speed_tod[i])*3.6))+' km/h;'+str(round(int(wind_speed_tod[i])*2.237))+' mph'
        a = wind_speed_tod[0]
        del wind_speed_tod[0]
        wind_speed_tod.append(a)
        wind_direct_tod = re.findall('>(.+)</dt', w_today)
        for i in range(len(wind_direct_tod)):
            wind_direct_tod[i] = wind_direct_tod[i].split('>')[-1]
        a = wind_direct_tod[0]
        del wind_direct_tod[0]
        wind_direct_tod.append(a)
    ########
    
    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in weather.keys():
        weather[i] = globals()[i]
    return weather