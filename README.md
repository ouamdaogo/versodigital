# VersoDigital Blog

Un blog profesional y moderno desarrollado con Flask, enfocado en SEO y experiencia de usuario.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Características

- Gestión completa de posts y categorías
- Sistema de autenticación de usuarios
- Panel de administración intuitivo
- Soporte para imágenes destacadas
- Optimización SEO integrada
- Diseño responsive
- Sistema de etiquetas y categorías
- URLs amigables con slugs
- Análisis de tráfico básico

## Requisitos

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- Werkzeug
- Python-dotenv

## Tecnologías

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: SQLite
- **Autenticación**: Flask-Login
- **Formularios**: Flask-WTF
- **Imágenes**: Pillow
- **SEO**: Meta tags dinámicos

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ouamdaogo/versodigital.git
cd versodigital
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
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

6. Ejecutar la aplicación:
```bash
flask run
```

## Configuración

### Variables de Entorno

- `FLASK_APP`: Nombre del archivo principal
- `FLASK_ENV`: Entorno (development/production)
- `SECRET_KEY`: Clave secreta para sesiones
- `DATABASE_URL`: URL de la base de datos
- `UPLOAD_FOLDER`: Directorio para uploads

## Uso

1. Acceder a `/admin/setup` para crear el primer usuario administrador
2. Iniciar sesión en `/admin/login`
3. Usar el panel de administración para gestionar el contenido

## Estructura del Proyecto

```
web_ibra/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── static/            # Archivos estáticos
│   ├── css/          # Estilos
│   └── uploads/      # Imágenes subidas
└── templates/        # Plantillas
    ├── admin/       # Plantillas del admin
    └── partials/    # Componentes reutilizables
```

## Contribución

¡Las contribuciones son bienvenidas! Por favor, lee nuestra [guía de contribución](CONTRIBUTING.md).

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

- Website: [versodigital.com](https://versodigital.com)
- Email: [contacto@versodigital.com](mailto:contacto@versodigital.com)
- Twitter: [@VersoDigital](https://twitter.com/VersoDigital)

## Agradecimientos

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
