# Laboratorio SportApp

## Requerimientos
    - Se debe tener instalado python 3.9
    - Se debe tener instalado pipenv
    - Se debe tener instalado Docker, se recomienda docker desktop si no estas familiarizado ver(https://docs.docker.com/compose/install/#scenario-one-install-docker-desktop)

## Ejecutar el proyecto
    - Validar que cuentas con docker instalado `docker -v`
    - Validar que cuentas con docker-compose instalado `docker-compose -v`
    - Ejecutar el comando `docker-compose up -d`

## Recomendaciones
    - Si hacen cambios para verlos reflejados, reinicien las imagenes de sus proyectos con el comando `docker compose down --rmi all` y luego `docker-compose up -d`
    - Si es muy dificil trabajar con python descarguen y usen pycharm community edition (https://www.jetbrains.com/es-es/pycharm/download/?section=mac)
