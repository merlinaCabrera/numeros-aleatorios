-- Crear DB y tabla
CREATE DATABASE random_numbers;

CREATE TABLE random_numbers.generated_numbers (
	id INT NOT NULL AUTO_INCREMENT,
    figure_count INT,
    square_count INT,
    unique_position_value FLOAT,
    temperature DECIMAL(4, 2),
    seed VARCHAR(255),
    generated_number VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Popular la DB para realizar pruebas
INSERT INTO random_numbers.generated_numbers 
    (figure_count, square_count, unique_position_value, temperature, seed, generated_number) 
VALUES 
    (10, 4, 12345, 22.5, '67890', '987654321');
    
INSERT INTO random_numbers.generated_numbers 
    (figure_count, square_count, unique_position_value, temperature, seed, generated_number) 
VALUES 
    (8, 3, 54321, 20.0, '12345', '123456789');
    
INSERT INTO random_numbers.generated_numbers 
    (figure_count, square_count, unique_position_value, temperature, seed, generated_number) 
VALUES 
    (15, 5, 67890, 25.7, '24680', '112233445');

INSERT INTO random_numbers.generated_numbers 
    (figure_count, square_count, unique_position_value, temperature, seed, generated_number) 
VALUES 
    (12, 2, 98765, 18.9, '13579', '998877665');

