# Guia de pasos para subir el proyecto de Flask a Amazon

## Requisitos

- Se recomienda que el proyecto sea creado utilizando la plantilla subida en la clase del 02/03/2023
- Crear una instancia
- Tener acceso a la llave (.pem en el caso de MacOS/Linux y .ppk en el caso de Windows)
- Tener el proyecto listo y funcionando

Como crear una instancia - > [aqui](https://login.codingdojo.com/m/351/11275/77316)

## Pasos pre subida del proyecto a Github

Una vez de que tengan su proyecto listo y probado para subirlo al servidor, deberan hacer los siguientes pasos:

- Dentro de el shell de pipenv, es decir luego de ejecutar pipenv shell
- Correr el siguiente comando ```pip freeze > requirements.txt```
- Crear repositorio en modo público
- Subir el código

## Conectarse a la máquina de EC2 - Amazon

 Guia:
 - [Windows](https://www.youtube.com/watch?v=051Jdka8piY) seguir hasta el minuto 2:20 aprox
 - [MacOS/Linux](https://www.youtube.com/watch?v=8UqtMcX_kg0) desde el minuto 2 aprox.

 ## Conectados en la máquina

 ```
 	sudo apt-get update
	sudo apt-get install python3-pip nginx git python3-venv mysql-server -y
	sudo apt-get update
	sudo mysql
 ```

 Aquí entraremos a la shell de mysql y necesitamos ejecutar en esta

```
	ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'P4ssW0rD';
	FLUSH PRIVILEGES;
	quit
```

con quit o control + d salimos de la shell de mysql.

Luego seguimos aplicando ```sudo mysql_secure_installation``` Aqui se haran varias preguntas dentro de la terminal y contestaremos:

	- Primera pre. "Enter password for user root:" -> {{password_config_mysql}}
	- Segunda pregt. "Would you like to setup VALIDATE PASSWORD component?" -> n 
	- Tercera preg. "Change password for root" -> n
	- Cuarta preg. "Remove anonymous users" -> y
	- QUinta preg. "Disallow root loggin remotely?" -> y
	- Sexta preg.  "Remove test database" -> y
	- Septima preg. "Reload privilege tables now?" -> y

Ahora vamos a cargar eldump de nuestra base de datos, para esto necesitamos seguir los pasos de la sección que dice "1. Exporta el esquema" en la [página](https://login.codingdojo.com/m/351/11275/77318)

Ahora descargaremos nuestro proyecto a la maquina de la siguiente manera:

```
	cd
	git clone {{ url copiada del proyecto de gthub }}
	cd {{ project }}
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
	pip3 install gunicorn
	deactivate
	source venv/bin/activate
	gunicorn --bind 0.0.0.0:5000 app:app
```

Aqui se cargara gunicorn y quedará corriendo en la terminal, se deberá ver algo así.

```
[2016-12-27 05:45:56 +0000] [8695] [INFO] Starting gunicorn 19.6.0
[2016-12-27 05:45:56 +0000] [8695] [INFO] Listening at: http://0.0.0.0:5000 (8695)
[2016-12-27 05:45:56 +0000] [8695] [INFO] Using worker: sync
[2016-12-27 05:45:56 +0000] [8700] [INFO] Booting worker with pid: 8700
```

Si es que este último comando falla contacte a ayuda.


Si todo sale bien matamos el proceso apretando control + c y continuamos aplicando

```
	deactivate
	sudo vim /etc/systemd/system/gunicorn.service
```

Aqui apretamos i y luego pegamos el siguiente texto con los remplazos correspondientes

```
[Unit]
Description=Gunicorn instance
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/{{repo name}}
Environment="PATH=/home/ubuntu/{{repo name}}/venv/bin"
ExecStart=/home/ubuntu/{{repo name}}/venv/bin/gunicorn --workers 3 --bind unix:{{project}}.sock -m 007 wsgi:application
[Install]
WantedBy=multi-user.target
```

ahora pare cerrar VIM/editor apretamos ESC luego : y luego w y q y finalmente enter.

Continuamos ejecutando

```
	sudo systemctl start gunicorn
	sudo systemctl enable gunicorn
	sudo vim /etc/nginx/sites-available/{{project}}
```

Aqui apretamos i y luego pegamos el siguiente texto con los remplazos correspondientes

```
server {
    listen 80;
    server_name {{yout_public_ip}};
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/{{repo name}}/{{project}}.sock;
    }
}
```

ahora pare cerrar VIM/editor apretamos ESC luego : y luego w y q y finalmente enter.


Continuamos ejecutando

```
	sudo ln -s /etc/nginx/sites-available/project_flask /etc/nginx/sites-enabled
	sudo rm /etc/nginx/sites-enabled/default
	sudo vim /etc/nginx/nginx.conf
```

Aqui deben editar la primera linea que dice ```user www-data;``` por  ```user ubuntu;```
ahora pare cerrar VIM/editor apretamos ESC luego : y luego w y q y finalmente enter.

```	
	sudo nginx -t
	sudo service nginx restart
```
Y con eso deberian tenerlo funcionando
HINT: Usar {{repo name}} y {{project}} con el mismo nombre de la carpeta que se descarga desde git