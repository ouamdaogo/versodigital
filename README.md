# VersoDigital Blog

Blog profesional desarrollado con Flask para VersoDigital. Una plataforma moderna para compartir contenido digital.

## Características

- Sistema de administración de contenido
- Editor de posts con soporte para imágenes
- Categorías y etiquetas
- SEO optimizado
- Diseño responsivo
- Sistema de autenticación
- Posts relacionados
- Compartir en redes sociales

## Requisitos

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- Werkzeug
- Python-dotenv

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd web_ibra
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
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

6. Ejecutar el servidor:
```bash
python app.py
```

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

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

VersoDigital - [Sitio web](https://versodigital.com)
