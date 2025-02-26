[Ejemplo Completo: Proyecto NodeJS](#ejemplo-con-nodejs)
[Subir imagen a Docker Hub](#subir-imagen-a-docker-hub)
[Despliegue en Heroku](#despliegue-en-heroku)
[Ejemplo Completo: Proyecto Python](#ejemplo-con-python)
[Extra: Despliegue en producción](#despliegue-en-producción)



## Ejemplo con NodeJS

En este apartado vamos a transformar un proyecto nodejs full-stack en una única imagen de Docker para poder almacenarla, compartirla, ejecutarla y desplegarla en un entorno de producción.

### Getting started

<details>
  <summary>Guía paso a paso de instalación</summary>

Puedes `clonar los repositorios` para el ejercicio desde los siguientes enlaces:

- [animal-api](https://github.com/amargopastor-codealong/animal-api)
- [animal-front](https://github.com/amargopastor-codealong/animal-front)

1. Ejecuta el comando `npm install` para ambos proyectos
2. Recuerda que `animal-api` necesita un fichero `.env para la variable PORT`
3. Familiarizate con ambos proyectos
4. Genera una build del proyecto `animal-front` con `npm run build` y copia la nueva `carpeta dist` en la raíz del proyecto `animal-api`
5. Ejecuta el proyecto `animal-api` con `npm run start`

Si todo ha ido bien deberías tener disponible el proyecto `animal-api` corriendo en el puerto `http://localhost:3001` sirviendo los archivos estáticos de la carpeta `dist` en su raíz. Observa commo la información que recibidos de los endpoints de la API aparecen en la consola de tu navegador:

<p>
  <img src="./img/npm_run_start.png" style="width: 100%">
</p>

> [!WARNING]  
> Asegúrate de tener [instalado docker](https://docs.docker.com/engine/install/) en tu ordenador junto con el interfad docker-desktop:

<p>
  <img src="./img/docker_version.png" style="width: 100%">
</p>

</details>

### Crear un archivo Dockerfile

El primer paso será `crear un archivo Dockerfile` que defina el como será la imagen de la aplicación:

```dockerfile
# 1. Usamos una imagen base de Node.js versión LTS (Long Term Support)
FROM node:18

# 2. Establece un directorio de trabajo en el contenedor: todo el código se copiará aquí.
WORKDIR /app

# 3. Copia el package.json y package-lock.json al contenedor para instalar las dependencias antes de copiar todo el código.
COPY package*.json ./

# 4. Instala solo las dependencias necesarias para producción. Si también quieres instalar las dependencias de desarrollo, omite --production.
RUN npm install --production

# 5. Copiar el resto del código fuente de la aplicación al contenedor
COPY . .

# 6. Exponer el puerto en el que tu aplicación estará escuchando
EXPOSE 3001

# 7. Este comando ejecuta tu aplicación, asumiendo que tienes un script start en el package.json como: "start": "node index.js".
CMD ["npm", "start"]

```

### Crear un archivo .dockerignore

El archivo `.dockerignore` es útil para evitar que ciertos archivos sean copiados al contenedor. De manera similar al fichero .gitignore, el objetivo es evitar compartir ficheros y recursos que por su propia naturaleza se auto-generan durante el proceso de ejecución. El objetivo es hacer `una imagen lo más liviana y eficiente posible`:

```.dockerignore
node_modules
npm-debug.log
.DS_Store
.git
.gitignore
.env

```

Este archivo excluye directorios y archivos innecesarios como `node_modules`, archivos de configuración de Git, y archivos de entorno sensibles como `.env`.

### Construir la imagen de Docker

Para construir la imagen de Docker, debemos ejecutar el siguiente comando `en la raíz de nuestro proyecto`:

```bash
docker build -t my-node-app .
```

> [!TIP]
> Recuerda que puedes usar el comando `docker images` para visualizar todas las imágenes en tu máquina (o usar el interfaz de docker desktop):

<p>
  <img src="./img/docker_images.png" style="width: 100%">
</p>

> [!NOTE]
> Las imágenes de Docker se almacenan en el sistema de archivos que Docker usa internamente, llamado **overlayFS** (en la mayoría de los sistemas modernos), que almacena la información de las capas de las imágenes. Docker no almacena las imágenes como archivos únicos, sino que las divide en capas que se comparten entre diferentes imágenes para ahorrar espacio.

### Ejecutar un contenedor

Vamos a ejecutar un contenedor (a.k.a instanciar nuestra imagen) en el puerto 3001 con el siguiente comando:

```bash
docker run -p 3001:3001 my-node-app
```

> [!WARNING]
> Si tienes un archivo `.env` para variables de entorno, asegúrate de pasarlo al contenedor definiendo `--env-file`:

```bash
docker run --env-file .env -p 3001:3001 my-node-app
```

> [!TIP]
> Recuerda que puedes usar el comando `docker ps -a` para visualizar todas las instancias en tu máquina (o usar el interfaz de docker desktop):

<p>
  <img src="./img/docker_container.png" style="width: 100%">
</p>

### Ejecutar otro contenedor

_easy peasy_

```bash
docker run -p 3001:3001 -e PORT=3000 my-node-app
```

### Crear un volumen para node_modules (opcional)

Si estás desarrollando localmente y no quieres reinstalar las dependencias cada vez que construyas la imagen, puedes usar volúmenes para mantener los módulos fuera de la imagen. Esto lo puedes hacer al correr el contenedor:

```bash
docker run -p 3001:3001 -v $(pwd):/app -v /app/node_modules my-node-app
```

Esto asegura que los cambios en el código fuente sean reflejados sin necesidad de reconstruir la imagen cada vez.

## Subir imagen a Docker Hub

Una vez que has construido una imagen localmente usando Docker Desktop, podemos subir (empujar) esa imagen a Docker Hub para compartirla o almacenarla en la nube:

1. Primero debemos autenticarnos en Docker Hub:

```bash
docker login
```

2. Ponerle una etiqueta de referencia a nuestra imagen:

```bash
docker tag my-node-app your-dockerhub-username/my-node-app
```

3. _Pushear_ la imagen a Docker Hub:

```bash
docker push your-dockerhub-username/my-node-app
```

En resumen, Docker Desktop te permite trabajar en tu máquina local, mientras que Docker Hub actúa como un repositorio centralizado donde puedes almacenar y compartir tus imágenes Docker.

## Despliegue en Heroku

Llegados a este punto, vamos a intentar lanzar nuestro proyecto a un entorno real de producción utilizando la imagen que ya tenemos generada. Para ello vamos a utilizar Heroku por su simplicidad y fácil configuración a través de su [CLI](https://devcenter.heroku.com/articles/heroku-cli).

<details>
  <summary>Otras plataformas de Cloud Computing (PaaS) con Soporte Docker</summary>

- AWS Elastic Beanstalk (con Docker)
- Google Cloud Run
- Microsoft Azure App Service (con Docker)

</details>

### Instalar Heroku CLI

Lo primero que debemos hacer es descargar el [CLI de Heroku](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli) y comprobar su instalación:

```bash
heroku --version
```

### Iniciar sesión en Heroku

Este comando abrirá una ventana del navegador para que ingreses tus credenciales de Heroku. Una vez que inicies sesión, la CLI estará autenticada:

```bash
heroku login
```

### Crear una aplicación en Heroku

```bash
heroku create my-node-app
```

<p>
  <img src="./img/heroku_create.png" style="width: 100%">
</p>

### Configurar Heroku para usar Docker

Aunque existen diversar formar de configurar Heroku para que emplee Docker, lo más sencillo es utilizar el propio Dockerfile en la raíz de nuestro proyecto iniciando sesión en Docker:

```bash
heroku container:login
```

> [!NOTE]
> Este comando autentica tu sesión de Docker para que puedas interactuar con Heroku Container Registry.

### Construir y enviar la imagen Docker a Heroku

El siguiente paso es construir y enviar la imagen Docker a Heroku. Heroku llamará al proceso web por defecto, así que vamos a mantener la etiqueta web al subir tu imagen.

```bash
heroku container:push web -a my-node-app
```

> [!WARNING]
> Debido a las configuraciones por defecto, es posible que la app generada no esté prepara para docker. En este caso debemos introducir el siguiente comando:

```bash
heroku stack:set container
```

<p>
  <img src="./img/heroku_container.png" style="width: 100%">
</p>

### Liberar la imagen Docker en Heroku

Una vez que la imagen haya sido subida a Heroku, debes lanzar tu contenedor para que Heroku lo ejecute en su plataforma. Este comando libera la imagen y despliega tu aplicación en Heroku:

```bash
heroku container:release web -a my-node-app
```

### Verificar que la aplicación esté en funcionamiento

Una vez que tu contenedor ha sido liberado, puedes verificar que tu aplicación esté corriendo en Heroku. Heroku te proporcionará un dominio para tu aplicación.

```bash
heroku open -a my-node-app
```

### Resumen de comandos:

- **`heroku login`**: Instalar Heroku CLI y autenticarse
- **`heroku create my-node-app`**: Crear una nueva aplicación en Heroku
- **`heroku container:login`**: Iniciar sesión en Docker
- **`heroku container:push web -a my-node-app`**: Construir y subir la imagen Docker a Heroku
- **`heroku container:release web -a my-node-app`**: Liberar la imagen para producción
- **`heroku open -a my-node-app`**: Abrir la aplicación
- **`heroku logs --tail -a my-node-app`**: Ver logs de la aplicación

