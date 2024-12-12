# Guía de Contribución

¡Gracias por tu interés en contribuir a VersoDigital! Esta guía te ayudará a configurar el proyecto y hacer contribuciones.

## Configuración del Entorno de Desarrollo

1. Clonar el repositorio:
```bash
git clone https://github.com/ouamdaogo/versodigital.git
cd versodigital
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Unix o MacOS:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Inicializar la base de datos:
```bash
flask db upgrade
```

## Flujo de Trabajo

1. Crear una nueva rama para tu feature:
```bash
git checkout -b feature/nombre-de-tu-feature
```

2. Hacer commits con mensajes descriptivos:
```bash
git add .
git commit -m "Descripción clara del cambio"
```

3. Mantener tu rama actualizada:
```bash
git fetch origin
git rebase origin/main
```

4. Subir tus cambios:
```bash
git push origin feature/nombre-de-tu-feature
```

5. Crear un Pull Request en GitHub

## Convenciones de Código

- Seguir PEP 8 para código Python
- Usar nombres descriptivos para variables y funciones
- Documentar funciones y clases con docstrings
- Mantener el código modular y DRY (Don't Repeat Yourself)

## Pruebas

- Agregar pruebas para nuevas funcionalidades
- Asegurar que todas las pruebas pasen antes de hacer commit
- Documentar casos de prueba

## Pull Requests

1. Usar un título descriptivo
2. Incluir una descripción detallada de los cambios
3. Referenciar issues relacionados
4. Incluir capturas de pantalla si hay cambios visuales
5. Asegurar que los checks de CI pasen

## Reportar Bugs

Al reportar bugs, incluir:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Capturas de pantalla si aplica
- Información del entorno (OS, navegador, etc.)

## Preguntas

Si tienes dudas:
1. Revisa los issues existentes
2. Consulta la documentación
3. Abre un nuevo issue con la etiqueta "question"

¡Gracias por contribuir!
