CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    rol VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(50),
    fuente VARCHAR(50) NOT NULL,
    producto_interes VARCHAR(255),
    presupuesto DECIMAL(12, 2),
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

INSERT INTO users (email, password_hash, nombre, rol) VALUES
('admin@leads.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LhY5Ai0VKkQ3hYQoO', 'Admin', 'admin');

INSERT INTO leads (nombre, email, telefono, fuente, producto_interes, presupuesto) VALUES
('Juan Perez', 'juan@email.com', '+573012345678', 'instagram', 'Curso', 299.99),
('Maria Lopez', 'maria@email.com', '+573023456789', 'facebook', 'Mentoria', 499.50),
('Carlos R', 'carlos@email.com', '+573034567890', 'landing_page', 'E-book', 49.99),
('Ana M', 'ana@email.com', '+573045678901', 'referido', 'Analytics', 199.00),
('Luis S', 'luis@email.com', '+573056789012', 'instagram', 'Pack', 599.00),
('Sofia H', 'sofia@email.com', '+573067890123', 'facebook', 'Premium', 799.99),
('Miguel T', 'miguel@email.com', '+573078901234', 'landing_page', 'SEO', 249.99),
('Isabella D', 'isabella@email.com', '+573089012345', 'instagram', 'Growth', 349.00),
('Roberto J', 'roberto@email.com', '+573090123456', 'referido', 'Emprendedor', 899.00),
('Valentina R', 'valentina@email.com', '+573001234567', 'facebook', 'Startup', 599.99);