# Hackathon Ambev

Backend desenvolvido em Django / Django REST Framework

<b>endpoints:</b>\
`/weather`:\
método: `GET`\
lista os objetos de dados de tempo

`/weather/current`:\
método: `GET`\
parâmetros:
 - city: nome da cidade (default: "Berlin")
 - country: código do país (default: "DE")

retorna dados de tempo atuais, obtidos há menos de 1 minuto


Para fazer deploy:\
`pip install -r requirements.txt`\
`python manage.py makemigrations`\
`python manage.py migrate`\
`python manage.py runserver 0.0.0.0:8000`
