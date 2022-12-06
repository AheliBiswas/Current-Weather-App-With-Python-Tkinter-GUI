import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import geopy as geopy
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import datetime as dt
import pytz as pytz


# WIDTH = 800
# HEIGHT = 500


def get_icon(icon):
    size = 65
    pic = ImageTk.PhotoImage(Image.open('./img/' + icon + '.png').resize((size, size)))
    icon_canvas.delete("all")
    icon_canvas.create_image(0, 0, anchor='nw', image=pic)
    icon_canvas.image = pic


def show_update(update):
    temp.config(text=str(round(update['main']['temp'])) + "°c")
    icon = update['weather'][0]['icon']
    get_icon(icon)
    try:
        # ---------------------- Values of Left Label bg="#1C1E23", -----------------------------
        main.config(text=update['weather'][0]['main'])
        description.config(text=update['weather'][0]['description'])
        feel.config(text=str(update['main']['feels_like']) + " °c")
        humid.config(text=str(update['main']['humidity']) + " %")
        wind.config(text=str(update['wind']['speed']) + " m/s")

        # ---------------------- Values of right Label bg="#1C1E23", -----------------------------
        visibility.config(text=str(update['visibility'] / 1000) + " KM")
        pressure.config(text=str(update['main']['pressure']) + " hPa")
        clouds.config(text=str(update['clouds']['all']) + " %")
        rain.config(text=str(update['rain']['1h']) + " mm")
        gust.config(text=str(update['wind']['gust']) + " m/s")
    except:
        print("Took Care Of Everything")


def get_weather(lon, lat):
    # ---------------------- API call-----------------------------
    key = '394c86b11f90d8efe6dd98eaf24dc5c6'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'appid': key, 'lat': lat, 'lon': lon, 'exclude': 'current', 'units': 'metric'}
    response = requests.get(url, params=params)
    update = response.json()
    show_update(update)


def get_location(city):
    # ---------------------- Locating Searched City-----------------------------
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)  # finding mentioned city's lat and lng
        tf = TimezoneFinder()
        result = tf.timezone_at(lng=location.longitude, lat=location.latitude)  # using lat and lng of geolocation to
        # find Continent & it's city
        country.config(text=result)
        lat_lon.config(text=f"{round(location.longitude, 4)}°N,{round(location.latitude, 4)}°E")

        # ---------------------- Finding out City and Country -----------------------------
        location = geolocator.reverse(str(location.latitude) + "," + str(location.longitude))
        address = location.raw['address']
        code = address.get('country_code')
        place.config(text=f"{city.capitalize()},{code.upper()}")

    except:
        print("Took care of AttributeError")
        messagebox.showerror("name error", "Incorrect Name Entered")

    # ---------------------- Finding out Date & Day -----------------------------
    zone = pytz.timezone(result)
    zone_date = dt.datetime.now(zone)
    date.config(text=zone_date.strftime("%d-%m-%y"))
    day.config(text=zone_date.strftime('%A'))

    # ---------------------- Finding out Time -----------------------------
    time.config(text=zone_date.strftime("%I:%M %p"))
    # ---------------------- get weather call -----------------------------
    get_weather(location.longitude, location.latitude)


root = tk.Tk()
root.resizable(False, False)
root.iconbitmap("sun_icon.ico")
root.title('Weather App')
root.geometry('800x500+350+150')

# canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
# canvas.pack()
# ---------------------- Background Image -----------------------------
img = tk.PhotoImage(file="bg.png")
background_label = tk.Label(root, image=img)
background_label.place(relheight=1, relwidth=1)

# ---------------------- Search Bar -----------------------------
frame = tk.Frame(root, bg="#F5DE65", bd=5)
frame.place(x=399, y=39, width=367, height=44)

entry = tk.Entry(root, font=40)
entry.place(x=408, y=46, width=299, height=31)

search_icon = tk.PhotoImage(file="search_icon.png")
button = tk.Button(root, image=search_icon, command=lambda: get_location(entry.get()))
button.place(x=720.92, y=45.7, width=37.68, height=31.57)

# ---------------------- Day & Date -----------------------------
day = tk.Label(root, text="-----", bg="#1C1E23", font=("Microsoft Sans Serif", 16, "bold"), fg="white")
day.place(x=623, y=414)

date = tk.Label(root, text="-----", font=("Microsoft Sans Serif", 16), fg="#9A81FA", bg="#1C1E23", justify='left',
                anchor="nw")
date.place(x=623, y=443)

# ---------------------- Temperature -----------------------------
temp = tk.Label(root, text="-----", font=("Microsoft Sans Serif", 48), bg="#1C1E23", fg="white")
temp.place(x=24, y=354)

# ---------------------- Temperature Icon-----------------------------
icon_canvas = tk.Canvas(root, bd=0, highlightthickness=0, bg="#1C1E23")
icon_canvas.place(height=68, width=68, x=195, y=370)

# ---------------------- Time & Place bg="#1C1E23", -----------------------------
place = tk.Label(root, text="----", bg="#1C1E23", fg="#9A81FA", font=("Verdana", 16))
place.place(x=24, y=436)

time = tk.Label(root, text="-----", bg="#1C1E23", fg="white", font=("Microsoft Sans Serif", 18, "bold"))
time.place(x=181, y=436)

# ---------------------- Continent and lan and lon bg="#1C1E23",#5B74A1 -----------------------------
country = tk.Label(root, text="----", bg="#1C1E23", fg="white", font=("arial", 16, "bold"))
country.place(x=36, y=39)

lat_lon = tk.Label(root, text="----", bg="#1C1E23", fg="#9A81FA", font=("arial", 12), anchor="w")
lat_lon.place(x=36, y=68)

# ---------------------- Weather Details header bg="#1C1E23", -----------------------------
weather_desc = tk.Label(root, text="Weather Description:", bg="#1C1E23", font=("arial", 14, "bold"), fg="#9A81FA")
weather_desc.place(x=160, y=124)

# ---------------------- Left Label bg="#1C1E23", -----------------------------
label1 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Main:", fg="#C366CC")
label1.place(x=181, y=160)

label2 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Description:", fg="#C366CC")
label2.place(x=181, y=190)

label3 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Feels Like:", fg="#C366CC")
label3.place(x=181, y=220)

label4 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Humidity:", fg="#C366CC")
label4.place(x=181, y=250)

label5 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Wind Speed:", fg="#C366CC")
label5.place(x=181, y=280)

# ---------------------- Values of Left Label bg="#1C1E23", -----------------------------
main = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
main.place(x=312, y=160)

description = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
description.place(x=312, y=190)

feel = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
feel.place(x=312, y=220)

humid = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
humid.place(x=312, y=250)

wind = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
wind.place(x=312, y=280)

# ---------------------- Right Label bg="#1C1E23", -----------------------------
label6 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Visibility:", fg="#C366CC")
label6.place(x=448, y=160)

label7 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Pressure:", fg="#C366CC")
label7.place(x=448, y=190)

label8 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Clouds:", fg="#C366CC")
label8.place(x=448, y=220)

label9 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Rain:", fg="#C366CC")
label9.place(x=448, y=250)

label10 = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="Wind Gust:", fg="#C366CC")
label10.place(x=448, y=280)

# ---------------------- Values of Right Label bg="#1C1E23", -----------------------------
visibility = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
visibility.place(x=579, y=160)

pressure = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
pressure.place(x=579, y=190)

clouds = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
clouds.place(x=579, y=220)

rain = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
rain.place(x=579, y=250)

gust = tk.Label(root, bg="#1C1E23", font=("Verdana", 12), text="-----", fg="white")
gust.place(x=579, y=280)

root.mainloop()
