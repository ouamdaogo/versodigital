from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from slugify import slugify
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Asegurar que existe el directorio de uploads
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Extensiones permitidas para imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    featured_image = db.Column(db.String(200))
    meta_description = db.Column(db.String(160))
    meta_keywords = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categories = db.relationship('Category', secondary='post_categories', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        if 'title' in kwargs:
            kwargs['slug'] = slugify(kwargs['title'])
        super(Post, self).__init__(*args, **kwargs)

    def get_meta_tags(self):
        return {
            'description': self.meta_description or self.summary,
            'keywords': self.meta_keywords,
            'author': self.author.username,
            'og:title': self.title,
            'og:description': self.meta_description or self.summary,
            'og:type': 'article',
            'article:published_time': self.created_at.isoformat(),
            'article:modified_time': self.updated_at.isoformat(),
        }

# Tabla de relación muchos a muchos entre Post y Category
post_categories = db.Table('post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['slug'] = slugify(kwargs['name'])
        super(Category, self).__init__(*args, **kwargs)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def utility_processor():
    return {
        'now': datetime.now()
    }

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    return render_template('index.html', posts=posts.items, categories=categories)

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    
    query = Post.query.filter_by(published=True)
    
    if category:
        query = query.join(Post.categories).filter(Category.slug == category)
    
    posts = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    categories = Category.query.all()
    
    return render_template('blog.html', posts=posts, categories=categories)

@app.route('/categoria/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(Post.categories).filter(
        Category.id == category.id,
        Post.published == True
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('category.html', category=category, posts=posts)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Obtener posts relacionados de las mismas categorías
    if post.categories:
        related_posts = Post.query.join(Post.categories).filter(
            Category.id.in_([c.id for c in post.categories]),
            Post.id != post.id,
            Post.published == True
        ).distinct().order_by(Post.created_at.desc()).limit(3).all()
    else:
        related_posts = []
    
    return render_template('post.html', post=post, related_posts=related_posts)

@app.route('/admin/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        summary = request.form.get('summary')
        meta_description = request.form.get('meta_description')
        meta_keywords = request.form.get('meta_keywords')
        action = request.form.get('action', 'draft')
        
        # Manejo de la imagen destacada
        featured_image = None
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                featured_image = filename

        # Crear nuevo post
        post = Post(
            title=title,
            content=content,
            summary=summary or title[:100],
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            featured_image=featured_image,
            user_id=current_user.id,
            published=(action == 'publish')
        )
        
        db.session.add(post)
        
        # Manejar categorías
        if 'categories[]' in request.form:
            category_ids = request.form.getlist('categories[]')
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            post.categories.extend(categories)
        
        try:
            db.session.commit()
            flash('Post creado exitosamente!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el post. Por favor, intenta de nuevo.', 'error')
            print(str(e))  # Para debugging
    
    categories = Category.query.all()
    return render_template('admin/new_post.html', categories=categories)

@app.route('/admin/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.summary = request.form.get('summary')
        post.meta_description = request.form.get('meta_description')
        post.meta_keywords = request.form.get('meta_keywords')
        post.published = request.form.get('action') == 'publish'
        
        # Manejo de la imagen destacada
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file and allowed_file(file.filename):
                # Si hay una imagen anterior, la eliminamos
                if post.featured_image:
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.featured_image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                post.featured_image = filename
        
        # Actualizar categorías
        post.categories = []
        if 'categories[]' in request.form:
            category_ids = request.form.getlist('categories[]')
            categories = Category.query.filter(Category.id.in_(category_ids)).all()
            post.categories.extend(categories)
        
        try:
            db.session.commit()
            flash('Post actualizado exitosamente!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el post. Por favor, intenta de nuevo.', 'error')
            print(str(e))
    
    categories = Category.query.all()
    return render_template('admin/edit_post.html', post=post, categories=categories)

@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml"""
    pages = []
    ten_days_ago = datetime.now() - timedelta(days=10)
    
    # Páginas estáticas
    pages.append([url_for('index', _external=True), ten_days_ago, 'weekly', '1.0'])
    pages.append([url_for('blog', _external=True), ten_days_ago, 'daily', '0.9'])
    
    # Posts dinámicos
    posts = Post.query.filter_by(published=True).all()
    for post in posts:
        url = url_for('post', slug=post.slug, _external=True)
        modified_time = post.updated_at or post.created_at
        pages.append([url, modified_time, 'weekly', '0.8'])
    
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    
    return response

@app.route('/admin/setup', methods=['GET', 'POST'])
def setup():
    # Verificar si ya existe un usuario administrador
    if User.query.first() is not None:
        flash('La configuración inicial ya se ha realizado', 'warning')
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # Crear usuario administrador
            admin = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(admin)
            
            # Crear categorías predeterminadas
            categories = [
                {'name': 'Desarrollo Web', 'slug': 'desarrollo-web'},
                {'name': 'Diseño UI/UX', 'slug': 'diseno-ui-ux'},
                {'name': 'Programación', 'slug': 'programacion'},
                {'name': 'Tecnología', 'slug': 'tecnologia'},
                {'name': 'Tutoriales', 'slug': 'tutoriales'}
            ]
            
            for cat_data in categories:
                category = Category(
                    name=cat_data['name'],
                    slug=cat_data['slug']
                )
                db.session.add(category)
            
            try:
                db.session.commit()
                flash('Configuración inicial completada con éxito', 'success')
                login_user(admin)
                return redirect(url_for('admin_dashboard'))
            except Exception as e:
                db.session.rollback()
                flash('Error durante la configuración: ' + str(e), 'error')
                
    return render_template('admin/setup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('admin/dashboard.html', posts=posts, categories=categories)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
