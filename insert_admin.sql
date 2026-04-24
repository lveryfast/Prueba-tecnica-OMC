-- Alterar tabla para agregar default UUID
ALTER TABLE users ALTER COLUMN id SET DEFAULT uuid_generate_v4();

-- Insertar admin con UUID explícito
INSERT INTO users (id, email, password_hash, nombre, rol) 
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'admin@leads.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LhY5Ai0VKkQ3hYQoO', 
    'Administrador', 
    'admin'
) ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash;