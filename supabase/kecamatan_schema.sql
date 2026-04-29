-- Kecamatan Database Schema for TaniBot
-- Stores all ~8,000 kecamatan in Indonesia with coordinates

CREATE TABLE IF NOT EXISTS kecamatan (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL, -- BPS code
    name VARCHAR(255) NOT NULL, -- Kecamatan name
    city_code VARCHAR(10) NOT NULL, -- City/Regency code
    city_name VARCHAR(255) NOT NULL, -- City/Regency name
    province_code VARCHAR(10) NOT NULL, -- Province code
    province_name VARCHAR(255) NOT NULL, -- Province name
    latitude DECIMAL(10, 7), -- Latitude
    longitude DECIMAL(10, 7), -- Longitude
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster searches
CREATE INDEX idx_kecamatan_name ON kecamatan USING gin(to_tsvector('indonesian', name));
CREATE INDEX idx_kecamatan_province ON kecamatan(province_name);
CREATE INDEX idx_kecamatan_city ON kecamatan(city_name);
CREATE INDEX idx_kecamatan_coords ON kecamatan(latitude, longitude);

-- Full-text search function
CREATE OR REPLACE FUNCTION search_kecamatan(search_text TEXT, limit_count INT DEFAULT 50)
RETURNS TABLE (
    id INT,
    code VARCHAR(10),
    name VARCHAR(255),
    city_name VARCHAR(255),
    province_name VARCHAR(255),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    rank FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        k.id,
        k.code,
        k.name,
        k.city_name,
        k.province_name,
        k.latitude,
        k.longitude,
        ts_rank(to_tsvector('indonesian', k.name), to_tsquery('indonesian', search_text)) as rank
    FROM kecamatan k
    WHERE to_tsvector('indonesian', k.name) @@ to_tsquery('indonesian', search_text)
       OR k.name ILIKE '%' || search_text || '%'
       OR k.city_name ILIKE '%' || search_text || '%'
       OR k.province_name ILIKE '%' || search_text || '%'
    ORDER BY rank DESC, k.name ASC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Function to get coordinates by name
CREATE OR REPLACE FUNCTION get_kecamatan_coords(kecamatan_name TEXT)
RETURNS TABLE (
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7)
) AS $$
BEGIN
    RETURN QUERY
    SELECT k.latitude, k.longitude
    FROM kecamatan k
    WHERE k.name ILIKE '%' || kecamatan_name || '%'
    ORDER BY k.name
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Insert sample data (add more as needed)
-- This is a template - populate with actual 7k+ kecamatan data
INSERT INTO kecamatan (code, name, city_code, city_name, province_code, province_name, latitude, longitude) VALUES
('350101', 'Pacet', '3501', 'Mojokerto', '35', 'Jawa Timur', -7.5333, 112.4333),
('350102', 'Ngoro', '3501', 'Mojokerto', '35', 'Jawa Timur', -7.4167, 112.7333),
('350103', 'Trawas', '3501', 'Mojokerto', '35', 'Jawa Timur', -7.5167, 112.5167),
('357101', 'Pabelan', '3571', 'Semarang', '35', 'Jawa Tengah', -6.9167, 110.2000),
('357102', 'Candisari', '3571', 'Semarang', '35', 'Jawa Tengah', -6.9833, 110.4000),
('360101', 'Cibinong', '3601', 'Bogor', '36', 'Jawa Barat', -6.5833, 106.8000),
('360102', 'Tanah Sareal', '3601', 'Bogor', '36', 'Jawa Barat', -6.4500, 106.8333),
('317101', 'Gambir', '3171', 'Jakarta Pusat', '31', 'DKI Jakarta', -6.1862, 106.8341),
('317102', 'Menteng', '3171', 'Jakarta Pusat', '31', 'DKI Jakarta', -6.1950, 106.8250),
('317201', 'Kebayoran Baru', '3172', 'Jakarta Selatan', '31', 'DKI Jakarta', -6.2267, 106.7833),
('510101', 'Denpasar Barat', '5101', 'Denpasar', '51', 'Bali', -8.6705, 115.2126),
('510102', 'Denpasar Timur', '5101', 'Denpasar', '51', 'Bali', -8.6500, 115.2333),
('510201', 'Ubud', '5102', 'Gianyar', '51', 'Bali', -8.5167, 115.2667),
('140101', 'Medan Kota', '1401', 'Medan', '12', 'Sumatera Utara', 3.5952, 98.6722),
('727101', 'Makassar', '7271', 'Makassar', '73', 'Sulawesi Selatan', -5.1477, 119.4327);

-- Grant permissions
GRANT SELECT ON kecamatan TO anon;
GRANT SELECT ON kecamatan TO authenticated;
