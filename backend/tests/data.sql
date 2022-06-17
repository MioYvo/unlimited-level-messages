INSERT INTO user (username, password, email, token, token_expired_at)
VALUES
  ('csdfsdfsss', 'pbkdf2:sha256:260000$QiviCCLPnsuLm43d$2e731ab00b4a52fd4eaaa599d6888c74a3ff2dd88a44b328351a3464c608d1e2', 'a@aa.com', '0fbbf81c-e52e-11ec-ae1c-0242ac150005', '2023-02-11 00:00:00'),
  ('aBCs3', 'pbkdf2:sha256:260000$LXosAy3NO4TtDLIu$c5289e9003f6f276f42723c6e75642f17a31d9165c6312a2a2c12e96e7e8a419', 'a@b.com', '33aaa9d4-e52f-11ec-868c-0242ac150005', '2023-02-11 00:00:00');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
