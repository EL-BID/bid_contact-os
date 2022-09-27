# BID Contact-Os
BID Contact-Os, Progressive Web App.
<p align="center"><img src="static/images/manifest/icon-512x512.png" width="512"/></p>
Es una plataforma de comunicación web en tiempo real, que permite comunicar diferentes personas de manera segura por medio de diferentes canales de comunicación como lo son: Audio, Video y Chat. Además, permite la creación de citas, reportería estadística, módulos administrativos, SEO, login SSO y muchas otras funcionalidades que permiten que Contact-Os sea una plataforma versátil y liviana para adoptar y personalizar.

# Requerimientos

BID Contact-Os se encuentra desarrollada con las siguientes herramientas y librerías:
- Python 3.8 (en modo de ambiente virtual)
- Python pip 21.2.4
- Flask 2.0.1
- Nginx 1.14.0 y Gunicorn 20.1.0
- SocketIO 3.1.0, Flask-SocketIO 5.1.1 y SimplePeer 9.7
- NodeJS 14.17.6
- Elasticsearch 7.15.2
- MySQL 8.0 o PostgreSQL 14.1
- npm 6.14.15
- npm (librerías):
    - webpack@5
    - css-loader
    - sass-loader
    - node-sass
    - extract-loader
    - file-loader
    - babel-core 
    - babel-loader
    - material-components-web
    - lots more!...


# Pasos de instalación

Para instalar BID Contact-Os hay que seguir los siguientes pasos (para Ubuntu 20.04):

1 - Crear un directorio para clonar BID Contact-Os. (ej: /var/www/)

2 - Instalar git:

    ~: sudo add-apt-repository ppa:git-core/ppa

    ~: sudo apt update

    ~: sudo apt-get install git

3 - Clonar BID Contact-Os del repositorio oficial:

    ~: git clone git@github.com:renegng/bid_contact-os.git

4 - Dentro del folder anterior, instalar Python 3.8 bajo un ambiente virtual y los pre-requisitos de las bases de datos (MySQL/PostgreSQL, ElasticSearch):

    ~: [python | python3 | python3.8 | python3.x] -m venv venv
    ~: sudo apt-get install build-essential python3-dev libmysqlclient-dev
    ~: sudo apt-get install elasticsearch

5 - Dentro del folder anterior, activar el ambiente virtual de Python:

    ~: source ./venv/bin/activate

6 - Dentro del ambiente virtual activo, instalar Flask y todas las aplicaciones de PiP:

    ~: pip install --upgrade pip

    Se puede instalar todos los paquetes en un solo paso ejecutando el siguiente comando:

    ~: pip install -r requirements.txt

    O, se pueden instalar de manera independiente:

    ~: pip install wheel
    ~: pip install flask
    ~: pip install flask-login
    ~: pip install flask-sqlalchemy
    ~: pip install flask-migrate
    ~: pip install flask-wtf
    ~: pip install flask-socketio
    ~: pip install flask-babel
    ~: pip install gunicorn[eventlet]
    ~: pip install gevent
    ~: pip install psycopg2-binary
    ~: pip install firebase-admin
    ~: pip install mysqlclient
    ~: pip install elasticsearch
    ~: pip install cryptography
    ~: pip install sqlalchemy-utils

    (OPCIONAL) Para los componentes del ChatBot, se deben instalar los siguientes componentes:
    ~: pip install pyspellchecker
    ~: pip install chatterbot
    ~: pip install pyyaml
    ~: pip install spacy
    ~: spacy download es

    ~: deactivate

7 - Instalar el plugin apropiado de Flask dependiendo del Web Server sobre el cual se ejecutará:

    ~: sudo apt-get install [libapache2-mod-wsgi-py3 | nginx]

8 - Instalar NodeJS:

    ~: curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -

    ~: sudo apt-get install -y nodejs

9 - Ejecutar NodeJS npm para instalar las librerías requisito de la plataforma:

    ~: npm install
    ~: npm run build-prd-wp

** - AOS puede generar inconvenientes ocasionalmente. Para prevenir esto, es necesario eliminar el archivo .babelrc dentro del folder node_modules/aos.

10 - Copiar y editar los archivos dentro de la carpeta instance con las credenciales y rutas adecuadas:
    
    + firebase-admin-key
    + firebase-api-init
    + firebase-key
    + config_app
    + config_firebase
    + config_models

11 - Ejecutar models/ddl.py para generar la base de datos mínima necesaria.

12 - Poner el Web Server en producción:

    + Apache HTTPD - swing_cms.apache2.conf
    O
    + Nginx/Gunicorn - swing_cms-socketio.*.conf


# Créditos

Se extienden los créditos a los siguientes equipos:
- Apache HTTPD, Nginx y Gunicorn web server que nunca falla.
- Google Material Design, Workbox y Firebase, por hacer el internet genial!
- Polymer Project,por una estructura genial inicial de base para PWA.
- Python, Flask, NodeJS, SQLAlchemy(-Utils), Migrate, Alembic, WTForms, Login, Cryptography GitHub y todos los frameworks espectaculares.
- MySQL, PostgreSQL, Firebase, ElasticSearch por bases de datos geniales.
- SocketIO y simple-peer por sus frameworks espectáculares de WebRTC.
- dr5hn's Countries States Cities Database por proveer una excelente base de datos de localización.
- Localforage por su increíble wrapper de localStorage.
- jsCalendar y LitePicker por su increíble y moderna librería de calendario.
- Chart.js por sus gráficos de data livianos y modernos.
- Traversy Media, por excelentes cursos libres sobre frameworks modernos.
- Visual Studio Code, por ser el mejor IDE actual.
- Twitter Twemoji por sus emojis tan fabulosos.
- El equipo de Ubuntu, por brindar el mejor y más amigable OS de productividad.
- Animate.css from <a href="https://animate.style/" title="Animate CSS">animate.style/</a> for their amazing css animations!
- Icons made by <a href="http://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
- Icons made by <a href="https://www.flaticon.com/authors/vitaly-gorbachev" title="Vitaly Gorbachev">Vitaly Gorbachev</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
- Icons made by <a href="https://www.flaticon.com/authors/fjstudio" title="fjstudio">fjstudio</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
- Icons made by <a href="https://www.flaticon.com/authors/dinosoftlabs" title="DinosoftLabs">DinosoftLabs</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
- Anchorme por su detección y reemplazo automático de URLs.
- Sounds from <a href="https://www.zapsplat.com/" title="Zapsplat">zapsplat.com</a> y <a href="https://mixkit.co/" title="Mixkit">mixkit.com</a>
- dev-console.macro, date-fns & crypto-js por librerías esenciales y robustas de Javascript.
