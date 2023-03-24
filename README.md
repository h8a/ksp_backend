# KSP Backend

## Requerimientos
- python 3.10 o cualquier version compatible con la mensionada
- conexión disponible a una base de datos postgresql 13.4 o cualquier version compatible con la mensionada

### Archivo de configuracion settings.yml dentro del directorio ksp_backend/src
```yaml
---
  api:
    version: v1.0.0
  service:
    host: localhost
    port: 5000
    log_level: debug
    debug: true
  db:
    connection: postgresql+asyncpg://test_user:test_password@localhost:5411/test1
```

### Variables de entorno necesarias, de lo contrario proveer la configuración en el archivo settings.yml

|Nombre|Ejemplo|Descripción|
|---|---|---|
|API_VERSION|v1.0.0|Esta versión es usada en la base de la url|
|SERVICE_HOST|0.0.0.0 ó localhost|Host en el que respondera el servicio|
|SERVICE_PORT|5000|Puerto en el cual estara escuchando el servicio|
|SERVICE_LOG_LEVEL|Opciones critical,error,warning,info,debug,trace|Posibles niveles de debug|
|SERVICE_DEBUG|True|Reload recursivo|
|DB|postgresql+asyncpg://test_user:test_password@localhost:5411/test1|Conexión en formato string para base de datos postgresql|



## Instrucciones
Pasos

Crear un entorno virtual:
```bash
python -m venv .env
```

Activar entorno virtual
```bash
source .env/bin/activate
```

Instalar librerias necesarias en el entorno virtual
```bash
pip install -r requirements.txt
```
Correr el servicio
```bash
python src/main.py
