INSERT INTO users(name, instructions, rating, date_joined, rider, credit_card_num, driver, car_make, car_model, license_num)
	VALUES ('Mike Easter', DEFAULT, 4.3, NULL, TRUE, 0123456789012345, FALSE, NULL, NULL, NULL),
			('Tom Magliozzi', 'Don''t drive like my brother', 3.2, DEFAULT, FALSE, NULL, TRUE, 'Toyota', 'Prius', '123456789'),
			('Ray Magliozzi', 'Don''t drive like my brother', 3.4, DEFAULT, TRUE, 1234567890123456, TRUE, 'Ford', 'Fusion', '012345678')
;

INSERT INTO passenger(user_id)
	VALUES (1),
			(1),
			(3)
;

INSERT INTO rides(driver, passenger_id)
	VALUES (2, 1),
			(3, 2),
			(2, 3)