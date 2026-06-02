-- Tabella Champions per League of Legends
CREATE TABLE IF NOT EXISTS champions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL,
    lore TEXT,
    difficulty VARCHAR(20),
    image_vertical VARCHAR(500),
    image_horizontal VARCHAR(500),
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indice per cerche veloci per ruolo
CREATE INDEX IF NOT EXISTS idx_role ON champions(role);
