# Hackathon Ambev

Backend desenvolvido em Django / Django REST Framework.
API(s) utilizada(s): OpenWeather <sup>(TM)</sup>

<b>endpoints:</b>\
`/weather`:\
método: `GET`\
lista os objetos de dados de tempo

`/weather/current`:\
método: `GET`\
parâmetros:
 - city: nome da cidade (padrão: "Berlin")
 - country: código do país (padrão: "DE")

retorna dados de tempo atuais, obtidos há menos de 1 minuto


Para fazer deploy:\
`pip install -r requirements.txt`\
`python manage.py makemigrations`\
`python manage.py migrate`\
`python manage.py runserver 0.0.0.0:8000`
