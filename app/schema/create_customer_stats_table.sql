CREATE TABLE customer_stats (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    contact_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    total_transactions INT DEFAULT 0,
    total_spent DECIMAL(15,2) DEFAULT 0,
    last_transaction_date DATETIME NULL,
    synced_at DATETIME NOT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,

    INDEX (contact_id),
    INDEX (total_transactions),
    INDEX (total_spent)
);

ALTER TABLE customer_stats 
ADD UNIQUE (contact_id);
