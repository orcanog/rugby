
# Import des bibliothèques standard
import locale
from datetime import *
import json
import os

# Import des bibliothèques tierces
from PIL import Image, ImageDraw, ImageFont
import qrcode

# Ce code sert à indiquer à Python que l'on voudra afficher des dates
# en français lors de l'utilisation de datetime.strptime()
locale.setlocale(locale.LC_TIME, "fr_FR")

events = {}
stadiums = {}
tickets = []

# Préparation des polices
color_white = (255, 255, 255)
color_black = (0, 0, 0)

path_font_bold = os.path.join("fonts", "Akshar-Bold.ttf")
path_fond_medium = os.path.join("fonts", "Akshar-Medium.ttf")

police_equipe = ImageFont.truetype(path_font_bold, 42)
police_reste = ImageFont.truetype(path_fond_medium, 30)

# Lecture des documents JSON
path_events = os.path.join("events.json")
path_stadiums = os.path.join("stadiums.json")
path_tickets = os.path.join("tickets.json")


with open(path_events, "r", encoding="utf-8") as f:
    events = json.load(f)

with open(path_stadiums, "r", encoding="utf-8") as g:
    stadiums = json.load(g)

with open(path_tickets, "r", encoding="utf-8") as h:
    tickets = json.load(h)

# Boucle sur chaque billet...
count = 1  # Compteur pour avoir des noms d'image uniques
for ticket in tickets:

    # Préparation des textes à écrire
    if ticket['seat'] == "free":
        siege = "Libre"
    else:
        siege = ticket['seat']

    if ticket['currency'] == "EUR":
        devise = "€"
    elif ticket['currency'] == "JPY":
        devise = "¥"
    elif ticket['currency'] == "NZD":
        devise = "$"

    for event in events:
        if event['id'] == ticket['event_id']:
            start = event['start']
            team_home = event['team_home']
            team_away = event['team_away']
    converted_start = datetime.fromisoformat(start)

    for stadium in stadiums:
        if stadium['id'] == ticket['event_id']:
            terrain = stadium['name']
            lieu = stadium['location']

    # Ouverture de l'image de fond
    with Image.open("billet.png") as im:
        draw = ImageDraw.Draw(im)

        # Écriture des informations du match
        draw.text((877, 115), team_home,
                  font=police_equipe, fill=color_black)
        draw.text((877, 242), team_away,
                  font=police_equipe, fill=color_black)
        draw.text((705, 375), terrain,
                  font=police_reste, fill=color_white)
        draw.text((1155, 375), lieu,
                  font=police_reste, fill=color_white)
        draw.text((705, 485), f"{converted_start.day}/{converted_start.month}/{converted_start.year}",
                  font=police_reste, fill=color_white)
        draw.text((1155, 485), f"{converted_start.hour}:{converted_start.minute}",
                  font=police_reste, fill=color_white)
        draw.text((650, 605), ticket['category'],
                  font=police_reste, fill=color_white)
        draw.text((845, 605), siege,
                  font=police_reste, fill=color_white)
        draw.text((995, 605), ("%s" % ticket['price'] + devise),
                  font=police_reste, fill=color_white)

        # Génération et écriture du QR Code
        qr = qrcode.QRCode(box_size=4)
        qr.add_data(ticket['id'])
        qr.make
        qr_image = qr.make_image()
        im.paste(qr_image, (111, 340))

        # Sauvegarde du billet
        filename, ext = os.path.splitext("billet.png")
        destination = f"{filename}_thumbnail{count}{ext}"
        count += 1
        im.save(destination, "PNG")
