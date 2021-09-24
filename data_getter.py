# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 17:53:15 2021

@author: ronal
"""

import pandas as pd
import requests

def get_auto_data(pages, mark, link):
    df_auto = pd.DataFrame()
    
    a = 1 #Переменная для перехода по страницам
    while a <= pages: #Всего 99 страниц на сайте
        #Объявление переменных как глобальные
        global License_plate, Availability, Category, Color_hex, Description, Custom_cleared, Owners_number, PTS, VIN, Vin_resolution
        global Year, Price_rub, Price_eur, Price_usd, Salon, Seller, Region, Timezone, Mileage, Tip_auto, Count_doors, Class_auto
        global Name_auto, trunk_volume_min, Marka_info, Model_info, Ik_summary
        URL = '{}'.format(link) #URL на который будет отправлен запрос
        #'https://auto.ru/-/ajax/desktop/listing/'
    
        #Параметры запроса
        PARAMS = {
             'catalog_filter' : [{"mark": ['{}'.format(mark)]}],
             'section': "all",
             'location': 'Санкт-Петербург',
             'GeoSelect' : [{'GeoSelect__title-shrinker': 'Любой регион'}],
             'category': "cars",
             #'sort': "fresh_relevance_1-asc",
             'page': a
            }
        #Заголовки страницы
        HEADERS = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length': '137',
            'content-type': 'application/json',
            'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
            'Host': 'auto.ru',
            'origin': 'https://auto.ru',
            'Referer': 'https://auto.ru/ryazan/cars/mercedes/all/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'x-client-app-version': '202002.03.092255',
            'x-client-date': '1580933207763',
            'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
            'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
            'x-requested-with': 'fetch'
        }
        
        response = requests.post(URL, json=PARAMS, headers=HEADERS) #Делаем post запрос на url
        try:
            data = response.json()['offers'] #Переменная data хранит полученные объявления
        except:
            continue
        df_one_auto = pd.DataFrame()
        img_url = [] #Словарь в котором будут все картинки
    
        i = 0 #Переменная для перехода по объявлениям
        while i <= len(data) - 1: #len(data)-1 это количество пришедших объявлений
    
            #Доступность объявления
            try:
                Availability = 'Доступность: ' + str(data[i]['availability'])
                df_one_auto.loc[i, 'Доступность'] = data[i]['availability']
            except:
                License_plate = 'Not availability'
                df_one_auto.loc[i, 'License_plate'] = License_plate 
            
    
            #Категория автомобиля
            try:
                Category = 'Категория: ' + str(data[i]['category'])
                df_one_auto.loc[i, 'Категория'] = data[i]['category']
            except:
                Category = 'Not category'
                df_one_auto.loc[i, 'Категория'] = Category
    
            #Цвет автомобиля (возвращается в формате hex)
            try:
                Color_hex = 'Цвет: #' + str(data[i]['color_hex'])
                df_one_auto.loc[i, 'Цвет'] = data[i]['color_hex']
            except:
                Color_hex = 'Not color'
                df_one_auto.loc[i, 'Цвет'] = Color_hex
    
            #Описание автомобиля
            try:
                Description = 'Описание: ' + str(data[i]['description'])
                df_one_auto.loc[i, 'Описание'] = str(data[i]['description'])
            except:
                Description = 'Not description'
                df_one_auto.loc[i, 'Описание'] = Description
            
    
            #Растаможен ли автомобиль (возвращает True или False)
            try:
                Custom_cleared = 'Таможня: ' + str(data[i]['documents']['custom_cleared'])
                df_one_auto.loc[i, 'Таможня'] = data[i]['documents']['custom_cleared']
            except:
                Custom_cleared = 'Not custom cleared'
                df_one_auto.loc[i, 'Таможня'] = Custom_cleared
    
            #Лицензия на автомобиль
            try:
                License_plate = 'Лицензия: ' + str(data[i]['documents']['license_plate'])
                df_one_auto.loc[i, 'Лицензия'] = str(data[i]['documents']['license_plate'])
            except:
                License_plate = 'Not license plate'
                df_one_auto.loc[i, 'Лицензия'] = License_plate
                
            #Колличество владельцев автомобиля
            try:
                Owners_number = 'Количество владельцев: ' + str(data[i]['documents']['owners_number'])
                df_one_auto.loc[i, 'Количество владельцев'] = data[i]['documents']['owners_number']
            except:
                Owners_number = 'The number of owners is not specified'
                df_one_auto.loc[i, 'Количество владельцев'] = Owners_number
    
            #PTS автомобиля
            try:
                PTS = 'PTS: ' + str(data[i]['documents']['pts'])
                df_one_auto.loc[i, 'PTS'] = data[i]['documents']['pts']
            except:
                PTS = 'Not PTS'
                df_one_auto.loc[i, 'PTS'] = PTS
    
            #VIN автомобиля
            try: 
                VIN = 'VIN: ' + str(data[i]['documents']['vin'])
                df_one_auto.loc[i, 'VIN'] = data[i]['documents']['vin']
            except: 
                VIN = 'Not VIN'
                df_one_auto.loc[i, 'VIN'] = VIN
    
            try: 
                Vin_resolution = 'Vin разрешение: ' + str(data[i]['documents']['vin_resolution'])
                df_one_auto.loc[i, 'Vin разрешение'] = data[i]['documents']['vin_resolution']
            except:
                Vin_resolution = 'Not vin resolution '
                df_one_auto.loc[i, 'Vin разрешение'] = Vin_resolution
    
            #Год выпуска автомобиля
            try:
                Year = 'Год: ' + str(data[i]['documents']['year'])
                df_one_auto.loc[i, 'Год'] = data[i]['documents']['year']
            except:
                Year = 'Not year'
                df_one_auto.loc[i, 'Год'] = Year
    
            #Цена в рублях, евро и долларах
            try:
                Price_rub = 'Рубли: ' + str(data[i]['price_info']['RUR']) + '₽'
                df_one_auto.loc[i, 'Цена (рубли)'] = data[i]['price_info']['RUR']
            except:
                Price_rub = 'Not price rub'
                df_one_auto.loc[i, 'Цена (рубли)'] = Price_rub
    
            try:
                Price_eur = 'Евро: ' + str(data[i]['price_info']['EUR']) + '€'
                df_one_auto.loc[i, 'Цена (евро)'] = data[i]['price_info']['EUR']
            except:
                Price_eur = 'Not price eur'
                df_one_auto.loc[i, 'Цена (евро)'] = Price_eur
    
            try:
                Price_usd = 'Доллар: ' + str(data[i]['price_info']['USD']) + '$'
                df_one_auto.loc[i, 'Цена (доллары)'] = data[i]['price_info']['USD']
            except:
                Price_usd = 'Not price usd'
                df_one_auto.loc[i, 'Цена (доллары)'] = Price_usd
    
            #С салона ли машина или нет
            try:
                Salon = 'С салона: ' + str(data[i]['salon']['is_official'])
                df_one_auto.loc[i, 'С салона'] = data[i]['salon']['is_official']
            except:
                Salon = 'Not salon'
                df_one_auto.loc[i, 'С салона'] = Salon
    
            #Координаты места нахождения машины (возвращается долгота и широта)
            try:
                Seller = 'Координаты: ' + str(data[i]['seller']['location']['coord']['latitude']) + ':' + str(data[i]['seller']['location']['coord']['longitude'])
                df_one_auto.loc[i, 'Координаты_ширина'] = data[i]['seller']['location']['coord']['latitude']
                df_one_auto.loc[i, 'Координаты_долгота'] = data[i]['seller']['location']['coord']['longitude']
            except:
                Seller = 'Not seller'
                df_one_auto.loc[i, 'Координаты_ширина'] = Seller
                df_one_auto.loc[i, 'Координаты_долгота'] = Seller
    
            #Регион, в котором находится автомобиль
            try:
                Region = 'Регион: ' + str(data[i]['seller']['location']['region_info']['name'])
                df_one_auto.loc[i, 'Регион'] = data[i]['seller']['location']['region_info']['name']
            except:
                Region = 'Not region'
                df_one_auto.loc[i, 'Регион'] = Region
    
            #Временная зона в которой находится автомобиль
            try:
                Timezone = 'Временная зона: ' + str(data[i]['seller']['location']['timezone_info']['abbr'])
                df_one_auto.loc[i, 'Временная_зона'] = data[i]['seller']['location']['timezone_info']['abbr']
            except:
                Timezone = 'Not timezone'
                df_one_auto.loc[i, 'Временная_зона'] = Timezone
    
            #Пробег автомобиля
            try:
                Mileage = 'Пробег: ' + str(data[i]['state']['mileage'])
                df_one_auto.loc[i, 'Пробег'] = data[i]['state']['mileage']
            except:
                Mileage = 'Not mileage'
                df_one_auto.loc[i, 'Пробег'] = Mileage
    
            #Картинки автомобиля
            #Возвращается несколько фото, мы их добавляем в словарь img_url
            for img in data[i]['state']['image_urls']:
                img_url.append(img['sizes']['1200x900'])
    
            #Тип автомобиля
            try:
                Tip_auto = 'Тип автомобиля: ' + str(data[i]['vehicle_info']['configuration']['body_type'])
                df_one_auto.loc[i, 'Тип_автомобиля'] = data[i]['vehicle_info']['configuration']['body_type']
            except: 
                Tip_auto = 'Not tip auto'
                df_one_auto.loc[i, 'Тип_автомобиля'] = Tip_auto
    
            #Количество дверей у автомобиля
            try:
                Count_doors = 'Колличество дверей: ' + str(data[i]['vehicle_info']['configuration']['doors_count'])
                df_one_auto.loc[i, 'Количество дверей'] = data[i]['vehicle_info']['configuration']['doors_count']
            except:
                Count_doors = 'Not count doors'
                df_one_auto.loc[i, 'Количество дверей'] = Count_doors
                
            #Секция: used - поддержанный, или new
            try: 
                Section = 'Секция: ' + str(data[i]['section'])
                df_one_auto.loc[i, 'Секция'] = data[i]['section']
            except: 
                Section = 'Not section'
                df_one_auto.loc[i, 'Секция'] = Section
            
            '''Доп. информация, содержит: 'review_summary': {'avg_rating': 4.599999904632568, 'counter': 5},
               'price_stats': {},
               'booking': {},
               'days_in_stock': 5,
               'days_on_sale': 5, а также свежесть'''
            try: 
                Additional_Info = 'Доп. информация: ' + str(data[i]['additional_info'])
                df_one_auto.loc[i, 'Доп_информация'] = str(data[i]['additional_info'])
            except: 
                Additional_Info = 'Not add. info'
                df_one_auto.loc[i, 'Доп_информация'] = Additional_Info
             
            #Актуальность
            try: 
                Relevance_Info = 'Актуальность: ' + str(data[i]['relevance'])
                df_one_auto.loc[i, 'Актуальность'] = str(data[i]['relevance'])
            except: 
                Relevance_Info = 'Not relevance'
                df_one_auto.loc[i, 'Актуальность'] = Relevance_Info
            
            #Комплектация
            try: 
                Complectation = 'Комплектация: ' + str(data[i]['vehicle_info']['complectation'])
                df_one_auto.loc[i, 'Комплектация'] = str(data[i]['vehicle_info']['complectation'])
            except: 
                Complectation = 'Not complectation'
                df_one_auto.loc[i, 'Комплектация'] = Complectation
                
            try: 
                Equipment = 'Оборудование: ' + str(data[i]['vehicle_info']['equipment'])
                df_one_auto.loc[i, 'Оборудование'] = str(data[i]['vehicle_info']['equipment'])
            except: 
                Equipment = 'Not equipment'
                df_one_auto.loc[i, 'Оборудование'] = Equipment
                
            try:
                Vendor = 'Производитель: ' + str(data[i]['vehicle_info']['vendor'])
                df_one_auto.loc[i, 'Производитель'] = data[i]['vehicle_info']['vendor']
            except:
                Vendor = 'Not vendor'
                df_one_auto.loc[i, 'Производитель'] = Vendor
            
            #Затраты владельца: налог и тд
            try: 
                Owner_Expenses = 'Затраты владельца: ' + str(data[i]['owner_expenses'])
                df_one_auto.loc[i, 'Затраты_владельца'] = str(data[i]['owner_expenses'])
            except:
                Owner_Expenses = 'Not owner expenses'
                df_one_auto.loc[i, 'Затраты_владельца'] = Owner_Expenses
            
            #Класс автомобиля
            try:
                Class_auto = 'Класс автомобиля: ' + str(data[i]['vehicle_info']['configuration']['auto_class'])
                df_one_auto.loc[i, 'Класс_автомобиля'] = data[i]['vehicle_info']['configuration']['auto_class']
            except: 
                Class_auto = 'Not class auto'
                df_one_auto.loc[i, 'Класс_автомобиля'] = Class_auto
    
            #Название автомобиля
            try: 
                Name_auto = 'Имя автомобиля: ' + str(data[i]['vehicle_info']['configuration']['human_name'])
                df_one_auto.loc[i, 'Имя_автомобиля'] = data[i]['vehicle_info']['configuration']['human_name']
            except:
                Name_auto = 'Not name auto'
                df_one_auto.loc[i, 'Имя_автомобиля'] = Name_auto
    
            #Объем багажника автомобиля
            try:
                trunk_volume_min = 'Объем багажника: ' + str(data[i]['vehicle_info']['configuration']['trunk_volume_min'])
                df_one_auto.loc[i, 'Объем_багажника'] = data[i]['vehicle_info']['configuration']['trunk_volume_min']
            except:
                trunk_volume_min = 'Not trunk volume min'
                df_one_auto.loc[i, 'Объем_багажника'] = trunk_volume_min
    
            #Марка автомобиля
            try:
                Marka_info = 'Марка автомобиля: ' + str(data[i]['vehicle_info']['mark_info']['name'])
                df_one_auto.loc[i, 'Марка_автомобиля'] = data[i]['vehicle_info']['mark_info']['name']
            except:
                Marka_info = 'Not marka info'
                df_one_auto.loc[i, 'Марка_автомобиля'] = Marka_info
    
            #Модель автомобиля
            try:
                Model_info = 'Модель автомобиля: ' + str(data[i]['vehicle_info']['model_info']['name'])
                df_one_auto.loc[i, 'Модель автомобиля'] = data[i]['vehicle_info']['model_info']['name']
            except:
                Model_info = 'Not model info'
                df_one_auto.loc[i, 'Модель автомобиля'] = Model_info
    
            #Информация об автомобиле
            try:
                Ik_summary = 'Информация: ' + str(data[i]['lk_summary'])
                df_one_auto.loc[i, 'Информация'] = data[i]['lk_summary']
            except:
                Ik_summary = 'Not ik summary'
                df_one_auto.loc[i, 'Информация'] = Ik_summary
    
            i += 1 #Увеличиваем переменную перехода по объявлениям на 1
            df_auto = df_auto.append(df_one_auto)
        df_auto = df_auto.drop_duplicates().reset_index(drop=True)
        #print('Page: ' + str(a)) #Выводим сообщение, какая страница записалась
        a += 1 #Увеличиваем переменную страницы сайта на 1
    
    print('Cars of mark {} successfully loaded'.format(mark)) #Выводим информацию об успешном выполнении
    print('-'*90)
    return df_auto