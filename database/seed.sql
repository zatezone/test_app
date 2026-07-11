USE sample;

INSERT INTO users (user_id, name, email, password_hash)
VALUES
    (
        1,
        'Demo User',
        'demo@example.com',
        'pbkdf2:sha256:1000000$M3S1dtPO0WLy6V5d$0ff0c4c060926c00f465f7b6ba631646e320eb993be00bbb399011b9bad0ee51'
    )
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    password_hash = VALUES(password_hash);

INSERT INTO categories (category_id, user_id, category_name, category_type, is_default)
VALUES
    (1, 1, 'Food', 'expense', TRUE),
    (2, 1, 'Transport', 'expense', TRUE),
    (3, 1, 'Home Bills', 'expense', TRUE),
    (4, 1, 'Self-Care', 'expense', TRUE),
    (5, 1, 'Shopping', 'expense', TRUE),
    (6, 1, 'Health', 'expense', TRUE),
    (7, 1, 'Salary', 'income', TRUE),
    (8, 1, 'Freelance', 'income', TRUE),
    (9, 1, 'Investment', 'income', TRUE)
ON DUPLICATE KEY UPDATE
    category_name = VALUES(category_name),
    category_type = VALUES(category_type),
    is_default = VALUES(is_default);

INSERT INTO transactions (user_id, category_id, transaction_type, amount, description, transaction_date)
VALUES
    (1, 1, 'expense', 220.50, 'Lunch and snacks', '2026-07-10'),
    (1, 2, 'expense', 95.00, 'Bus and ride share', '2026-07-10'),
    (1, 3, 'expense', 1400.00, 'Electric bill', '2026-07-09'),
    (1, 4, 'expense', 350.00, 'Haircut', '2026-07-08'),
    (1, 5, 'expense', 780.00, 'Groceries and supplies', '2026-07-07'),
    (1, 6, 'expense', 500.00, 'Medicine', '2026-07-06'),
    (1, 7, 'income', 15000.00, 'Salary payout', '2026-07-10'),
    (1, 8, 'income', 3200.00, 'Freelance logo work', '2026-07-09'),
    (1, 9, 'income', 1200.00, 'Dividend payment', '2026-07-08');
