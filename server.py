import asyncio

import websockets

import requests

import datetime as dt

import json

# URL


def get_info(CITY):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "0459c9c55aba2880813f22ecd9867c4d"
    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()
    return response


def change_celsius_weather(data):
    do_c = data - 273.15
    do_f = do_c * (9/5) + 32
    return do_c, do_f
# create handler for each connection


async def handler(websocket, path):
    print("client connescted")

    try:
        async for message in websocket:
            print(f"received data :{message}")
            result = get_info(message)
            temp_kevin = result['main']['temp']
            temp_do_c, temp_do_f = change_celsius_weather(temp_kevin)
            print(temp_do_f)
            temp_max = result['main']['temp_max']
            temp_maxc, temp_max_f = change_celsius_weather(temp_max)
            temp_min = result['main']['temp_min']
            temp_min_c, temp_min_f = change_celsius_weather(temp_min)
            sunSineTime = dt.datetime.utcfromtimestamp(
                result['sys']['sunrise'] + result['timezone'])
            sun_sine_time_str = sunSineTime.isoformat()
            sunSetTime = dt.datetime.utcfromtimestamp(
                result['sys']['sunset'] + result['timezone'])
            sun_set_time_str = sunSetTime.isoformat()
            wind_speed = result['wind']['speed']
            do_am = result['main']['humidity']
            mo_ta = result['weather'][0]['description']
            city = result['name']
            icon = result['weather'][0]['icon']
            print(do_am)
            data_to_save = {
                "do_am": do_am,
                "mo_ta": mo_ta,
                "thanh_pho": city,
                "nhiệt độ lớn nhất ": f"{temp_maxc:.2f}",
                "Nhiệt độ nhỏ nhất ": f"{temp_min_c:.2f}",
                "Độ C": temp_do_c,
                "Nhiệt độ F ": f"{temp_do_f:.2f}",
                "Thời gian mặt trời mọc": sun_sine_time_str,
                "Thời gian mặt trời lặng": sun_set_time_str,
                "Tốc độ gió": wind_speed,
                "icon1": icon,
                "few clouds": "./icon/cloud_few.mp4",
                "Beautifull_weather_video": "./icon/186405 (720p).mp4",
                "overcast clouds":"./icon/overcast clouds.mp4",
                "light rain":"./icon/light rain.mp4",
                "scattered clouds":"./icon/scattered clouds.mp4",
                "clear sky":"./icon/clear sky.mp4",
                "moderate rain":"./icon/moderate rain.mp4",
            }
            file_path = "D:/python/python/app_weather/data.json"
            with open(file_path, 'w') as json_file:
                json.dump(data_to_save, json_file)
            print(f"Dữ liệu đã được lưu vào file JSON tại: {file_path}")
            print(f"result :{result}")
    except websocket.exceptions.ConnectionError:
        print("client disconnected")

    # data = await websocket.recv()ư

    # reply = f"Data recieved as:  {data}!"

    # await websocket.send(reply)


start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
