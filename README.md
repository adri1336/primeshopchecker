# PrimeShopChecker
Aplicación de escritorio para comprobar de forma automática stock en las tiendas más conocidas de España.
![image](https://github.com/user-attachments/assets/eecf31bb-615d-484e-87be-4c5a6a80de1b)

## Descarga
https://github.com/adri1336/primeshopchecker/releases

## Tiendas soportadas
- Amazon.es (añadir enlace sin parámetros, por ejemplo: https://www.amazon.es/dp/B09NMWD2BJ)
- Carrefour.es
- Elcorteingles.es
- Fnac.es
- Game.es
- Mediamarkt.es
- Direct.playstation.com

## Características
- Posibilidad de Proxy para evitar baneos (recomiendo https://dataimpulse.com/es/ con rotación de IPs españolas)
- Resuelve automáticamente captchas de Amazon
- Configurable desde ajustes
- Notificaciones al móvil (requiere instalar https://pushover.net/ en el teléfono y un token, se configura en ajustes): ![image](https://github.com/user-attachments/assets/3022fad3-79b9-4710-8f57-e0bd523c6c81)

## Donaciones para contribuir al tiempo de desarrollo
[![Donate with PayPal](https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Z5DFHA5C2RAFJ)

## Para desarrolladores:
### Requisitos
- Python 3 (https://www.python.org/downloads/)

### Configurar entorno
```
git clone https://github.com/adri1336/primeshopchecker.git
cd primeshopchecker/
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Probar
```
.\venv\Scripts\activate
python main.py
```


### Empaquetar
```
.\venv\Scripts\activate
flet pack main.py
```

