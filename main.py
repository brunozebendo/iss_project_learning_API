"""o objetivo do código é verificar a posição da estação espacial internacional e caso ela esteja
próxima da nossa posição, e se for noite, será passado um e-mail falando para olhar pra cima"""

import requests
from datetime import datetime
import smtplib
import time
"""abaixo estão as variáveis constantes, que deveriam ser preenchidas com as minhas informações"""
MY_EMAIL = "___YOUR_EMAIL_HERE____"
MY_PASSWORD = "___YOUR_PASSWORD_HERE___"
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

"""a função abaixo verifica se a estação espacial está passando na localização acima passada ou próxima
em 5 graus, reparar na sintaxe para pegar os dados, conforme expliquei no código anterior. Depois de
obter a informação e transformá-la em um float, o sistema verifica a posição"""
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

"""já essa função verifica se é noite, para isso, primeiro passa a latitude e longitude depois verifica
em outro site se é dia ou noite, de acordo com a hora do nascer do pôr do sol, nesse caso foram passados
parâmetro obrigatórios. Já nas variáveis sunrise e sunset foi utilizado o split pois o formato de hora 
que vem no json é diferente do time, assim, a string é dividida (split), usando o T como parâmetro de 
divisão, (na string, o t fica entre a data e a hora), depois o : que divide horas e minutos, depois
pega a primeira posição que é a hora e, por fim, transforma tudo isso em um int. Ai ele pega só a hora
da hora atual e faz a comparação"""
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

"""essa parte do código faz com que ele rode a cada sessenta segundos e caso as duas condições acima sejam
atingidas, ele passa um e-mail, conforme sintaxe já explicada anteriormente."""
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("__YOUR_SMTP_ADDRESS_HERE___")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        )


