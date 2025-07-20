CREATE TABLE test_db (
    id SERIAL PRIMARY KEY,
    station_name VARCHAR(100),
    line_name VARCHAR(100),
    destination VARCHAR(100),
    departure_time TIMESTAMP,
    platform VARCHAR(10),
    status VARCHAR(50)
);

INSERT INTO test_db (station_name, line_name, destination, departure_time, platform, status)
VALUES
('London Waterloo', 'South Western Railway', 'Woking', '2025-07-20 09:30:00', '4', 'On time'),
('London Waterloo', 'South Western Railway', 'Guildford', '2025-07-20 09:45:00', '5', 'Delayed'),
('London Victoria', 'Southern', 'Brighton', '2025-07-20 10:00:00', '8', 'On time'),
('Paddington', 'Great Western Railway', 'Reading', '2025-07-20 10:15:00', '2', 'Cancelled'),
('Euston', 'Avanti West Coast', 'Manchester', '2025-07-20 10:30:00', '7', 'On time'),
('King\'s Cross', 'LNER', 'Leeds', '2025-07-20 10:45:00', '1', 'On time'),
('Liverpool Street', 'Greater Anglia', 'Norwich', '2025-07-20 11:00:00', '9', 'On time'),
('St Pancras', 'East Midlands Railway', 'Nottingham', '2025-07-20 11:15:00', '6', 'Delayed'),
('Charing Cross', 'Southeastern', 'Dartford', '2025-07-20 11:30:00', '3', 'On time'),
('London Bridge', 'Thameslink', 'Brighton', '2025-07-20 11:45:00', '10', 'On time');
