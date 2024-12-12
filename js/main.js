// Navegación Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Menú móvil
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
});

// Animación de elementos al hacer scroll
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fadeIn');
        }
    });
}, observerOptions);

// Observar todas las secciones
document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// Manejo del formulario de contacto
const contactForm = document.getElementById('contact-form');

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Aquí puedes agregar la lógica para enviar el formulario
    // Por ejemplo, usando fetch para enviar los datos a un servidor
    
    alert('¡Gracias por tu mensaje! Te contactaremos pronto.');
    contactForm.reset();
});

// Cargar proyectos del portfolio (ejemplo)
const portfolioGrid = document.querySelector('.portfolio-grid');
const portfolioProjects = [
    {
        title: 'Proyecto 1',
        image: 'path/to/image1.jpg',
        description: 'Descripción del proyecto 1'
    },
    // Añade más proyectos aquí
];

// Cargar posts del blog (ejemplo)
const blogGrid = document.querySelector('.blog-grid');
const blogPosts = [
    {
        title: 'Post 1',
        excerpt: 'Extracto del post 1',
        date: '2024-01-01'
    },
    // Añade más posts aquí
];

// Función para cargar proyectos del portfolio
function loadPortfolioProjects() {
    portfolioProjects.forEach(project => {
        const projectElement = document.createElement('div');
        projectElement.className = 'portfolio-item';
        projectElement.innerHTML = `
            <h3>${project.title}</h3>
            <p>${project.description}</p>
        `;
        portfolioGrid.appendChild(projectElement);
    });
}

// Función para cargar posts del blog
function loadBlogPosts() {
    blogPosts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'blog-post';
        postElement.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.excerpt}</p>
            <small>${post.date}</small>
        `;
        blogGrid.appendChild(postElement);
    });
}

// Cargar contenido cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    loadPortfolioProjects();
    loadBlogPosts();
});
