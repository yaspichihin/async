CREATE_BRAND_TABLE = """
CREATE TABLE IF NOT EXISTS brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL
);
"""

CREATE_PRODUCT_TABLE = """
CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    brand_id INT NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
);
"""

CREATE_PRODUCT_COLOR_TABLE = """
CREATE TABLE IF NOT EXISTS product_color (
    product_color_id SERIAL PRIMARY KEY,
    product_color_name VARCHAR(255) NOT NULL
);
"""

CREATE_PRODUCT_SIZE_TABLE = """
CREATE TABLE IF NOT EXISTS product_size (
    product_size_id SERIAL PRIMARY KEY,
    product_size_name VARCHAR(255) NOT NULL
);
"""

CREATE_SKU_TABLE = """
CREATE TABLE IF NOT EXISTS sku (
    sku_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    product_size_id INT NOT NULL,
    product_color_id INT NOT NULL,
    FOREIGN KEY (product_id)
        REFERENCES product(product_id),
    FOREIGN KEY (product_size_id)
        REFERENCES product_size(product_size_id),
    FOREIGN KEY (product_color_id)
        REFERENCES product_color(product_color_id)
);
"""

PRODUCT_COLOR_INSERT = """
INSERT INTO product_color VALUES (1, 'Blue');
INSERT INTO product_color VALUES (2, 'Black');
"""

PRODUCT_SIZE_INSERT = """
INSERT INTO product_size VALUES (1, 'Small');
INSERT INTO product_size VALUES (2, 'Medium');
INSERT INTO product_size VALUES (3, 'Large');
"""
