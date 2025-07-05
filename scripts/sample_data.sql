USE university_portal;

DELETE FROM notifications;
DELETE FROM professor_contacts;
DELETE FROM enrollments;
DELETE FROM schedule;
DELETE FROM courses;
DELETE FROM users;

INSERT INTO users (username, email, password, role, full_name) VALUES
('armando.ruggeri', 'armando.ruggeri@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Armando Ruggeri'),
('dino.costa', 'dino.costa@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Dino Costa'),
('giancarlo.consolo', 'giancarlo.consolo@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Giancarlo Consolo'),
('antonio.celesti', 'antonio.celesti@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Antonio Celesti'),
('giacomo.fiumara', 'giacomo.fiumara@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Giacomo Fiumara'),
('salvatore.distefano', 'sdistefano@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Salvatore Distefano'),
('lorenzo.carnevale', 'lcarnevale@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Lorenzo Carnevale'),
('giancarlo.rinaldo', 'giancarlo.rinaldo@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Giancarlo Rinaldo'),
('maria.fazio', 'mfazio@unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'professor', 'Maria Fazio');

INSERT INTO users (username, email, password, role, full_name) VALUES
('student1', 'student1@studenti.unime.it', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'student', 'Mario Rossi');

-- Insert courses
INSERT INTO courses (course_code, course_name, professor_id, description, credits) VALUES
('WEB101', 'Web Programming', (SELECT id FROM users WHERE username = 'armando.ruggeri'), 'Introduction to web development technologies and frameworks', 6),
('PHYS101', 'Physics', (SELECT id FROM users WHERE username = 'dino.costa'), 'Fundamental principles of physics and their applications', 9),
('CALC101', 'Calculus', (SELECT id FROM users WHERE username = 'giancarlo.consolo'), 'Differential and integral calculus with applications', 9),
('DB101', 'Database', (SELECT id FROM users WHERE username = 'armando.ruggeri'), 'Database design, implementation, and management', 6),
('DB102', 'Database (Advanced)', (SELECT id FROM users WHERE username = 'antonio.celesti'), 'Advanced database concepts and distributed systems', 6),
('ML101', 'Machine Learning', (SELECT id FROM users WHERE username = 'giacomo.fiumara'), 'Introduction to machine learning algorithms and applications', 6),
('ADS101', 'Algorithms and Data Structures', (SELECT id FROM users WHERE username = 'giacomo.fiumara'), 'Fundamental algorithms and data structure implementations', 9),
('SE101', 'Software Engineering', (SELECT id FROM users WHERE username = 'salvatore.distefano'), 'Software development methodologies and project management', 6),
('SEC101', 'System Security', (SELECT id FROM users WHERE username = 'lorenzo.carnevale'), 'Computer and network security principles and practices', 6),
('DMATH101', 'Discrete Mathematics', (SELECT id FROM users WHERE username = 'giancarlo.rinaldo'), 'Mathematical foundations for computer science', 6),
('PROG101', 'Programming', (SELECT id FROM users WHERE username = 'maria.fazio'), 'Fundamentals of programming and problem solving', 9);

INSERT INTO schedule (course_id, day_of_week, start_time, end_time, room) VALUES
((SELECT id FROM courses WHERE course_code = 'WEB101'), 'Monday', '09:00:00', '11:00:00', 'Lab A1'),
((SELECT id FROM courses WHERE course_code = 'WEB101'), 'Wednesday', '09:00:00', '11:00:00', 'Lab A1'),

((SELECT id FROM courses WHERE course_code = 'PHYS101'), 'Tuesday', '11:00:00', '13:00:00', 'Aula Magna'),
((SELECT id FROM courses WHERE course_code = 'PHYS101'), 'Thursday', '11:00:00', '13:00:00', 'Aula Magna'),

((SELECT id FROM courses WHERE course_code = 'CALC101'), 'Monday', '14:00:00', '16:00:00', 'Aula 1'),
((SELECT id FROM courses WHERE course_code = 'CALC101'), 'Wednesday', '14:00:00', '16:00:00', 'Aula 1'),
((SELECT id FROM courses WHERE course_code = 'CALC101'), 'Friday', '14:00:00', '16:00:00', 'Aula 1'),

((SELECT id FROM courses WHERE course_code = 'DB101'), 'Tuesday', '09:00:00', '11:00:00', 'Lab B1'),
((SELECT id FROM courses WHERE course_code = 'DB101'), 'Thursday', '09:00:00', '11:00:00', 'Lab B1'),

((SELECT id FROM courses WHERE course_code = 'DB102'), 'Monday', '16:00:00', '18:00:00', 'Lab B2'),
((SELECT id FROM courses WHERE course_code = 'DB102'), 'Wednesday', '16:00:00', '18:00:00', 'Lab B2'),

((SELECT id FROM courses WHERE course_code = 'ML101'), 'Tuesday', '14:00:00', '16:00:00', 'Lab C1'),
((SELECT id FROM courses WHERE course_code = 'ML101'), 'Friday', '09:00:00', '11:00:00', 'Lab C1'),

((SELECT id FROM courses WHERE course_code = 'ADS101'), 'Monday', '11:00:00', '13:00:00', 'Aula 2'),
((SELECT id FROM courses WHERE course_code = 'ADS101'), 'Wednesday', '11:00:00', '13:00:00', 'Aula 2'),
((SELECT id FROM courses WHERE course_code = 'ADS101'), 'Friday', '11:00:00', '13:00:00', 'Aula 2'),

((SELECT id FROM courses WHERE course_code = 'SE101'), 'Tuesday', '16:00:00', '18:00:00', 'Aula 3'),
((SELECT id FROM courses WHERE course_code = 'SE101'), 'Thursday', '16:00:00', '18:00:00', 'Aula 3'),

((SELECT id FROM courses WHERE course_code = 'SEC101'), 'Wednesday', '16:00:00', '18:00:00', 'Lab D1'),
((SELECT id FROM courses WHERE course_code = 'SEC101'), 'Friday', '16:00:00', '18:00:00', 'Lab D1'),

((SELECT id FROM courses WHERE course_code = 'DMATH101'), 'Monday', '16:00:00', '18:00:00', 'Aula 4'),
((SELECT id FROM courses WHERE course_code = 'DMATH101'), 'Thursday', '14:00:00', '16:00:00', 'Aula 4'),

((SELECT id FROM courses WHERE course_code = 'PROG101'), 'Tuesday', '09:00:00', '11:00:00', 'Lab E1'),
((SELECT id FROM courses WHERE course_code = 'PROG101'), 'Thursday', '09:00:00', '11:00:00', 'Lab E1'),
((SELECT id FROM courses WHERE course_code = 'PROG101'), 'Friday', '09:00:00', '11:00:00', 'Lab E1');

INSERT INTO professor_contacts (professor_id, office_location, office_hours) VALUES
((SELECT id FROM users WHERE username = 'armando.ruggeri'), 'Department of Engineering, Room 201', 'Monday 15:00-17:00, Wednesday 15:00-17:00'),
((SELECT id FROM users WHERE username = 'dino.costa'), 'Department of Physics, Room 105', 'Tuesday 14:00-16:00, Thursday 14:00-16:00'),
((SELECT id FROM users WHERE username = 'giancarlo.consolo'), 'Department of Mathematics, Room 301', 'Monday 10:00-12:00, Friday 10:00-12:00'),
((SELECT id FROM users WHERE username = 'antonio.celesti'), 'Department of Engineering, Room 205', 'Tuesday 15:00-17:00, Thursday 15:00-17:00'),
((SELECT id FROM users WHERE username = 'giacomo.fiumara'), 'Department of Computer Science, Room 401', 'Wednesday 10:00-12:00, Friday 15:00-17:00'),
((SELECT id FROM users WHERE username = 'salvatore.distefano'), 'Department of Engineering, Room 301', 'Monday 14:00-16:00, Wednesday 14:00-16:00'),
((SELECT id FROM users WHERE username = 'lorenzo.carnevale'), 'Department of Computer Science, Room 501', 'Tuesday 10:00-12:00, Friday 10:00-12:00'),
((SELECT id FROM users WHERE username = 'giancarlo.rinaldo'), 'Department of Mathematics, Room 201', 'Monday 09:00-11:00, Thursday 09:00-11:00'),
((SELECT id FROM users WHERE username = 'maria.fazio'), 'Department of Computer Science, Room 301', 'Tuesday 14:00-16:00, Thursday 14:00-16:00');

INSERT INTO notifications (course_id, professor_id, title, message) VALUES
((SELECT id FROM courses WHERE course_code = 'WEB101'), (SELECT id FROM users WHERE username = 'armando.ruggeri'), 'Project Assignment Released', 'The final web development project has been posted. Please check the course materials for requirements and deadline.'),
((SELECT id FROM courses WHERE course_code = 'PHYS101'), (SELECT id FROM users WHERE username = 'dino.costa'), 'Lab Session Schedule', 'Physics lab sessions will start next week. Please bring your lab manual and safety equipment.'),
((SELECT id FROM courses WHERE course_code = 'ML101'), (SELECT id FROM users WHERE username = 'giacomo.fiumara'), 'Guest Lecture Announcement', 'We will have a guest lecturer from industry next Friday discussing real-world ML applications.'),
((SELECT id FROM courses WHERE course_code = 'SE101'), (SELECT id FROM users WHERE username = 'salvatore.distefano'), 'Team Formation Deadline', 'Please form your project teams by the end of this week. Teams should have 3-4 members.'),
((SELECT id FROM courses WHERE course_code = 'SEC101'), (SELECT id FROM users WHERE username = 'lorenzo.carnevale'), 'Security Workshop', 'Optional cybersecurity workshop this Saturday from 10:00-16:00 in Lab D1. Registration required.');

INSERT INTO enrollments (student_id, course_id) VALUES
((SELECT id FROM users WHERE username = 'student1'), (SELECT id FROM courses WHERE course_code = 'WEB101')),
((SELECT id FROM users WHERE username = 'student1'), (SELECT id FROM courses WHERE course_code = 'PROG101')),
((SELECT id FROM users WHERE username = 'student1'), (SELECT id FROM courses WHERE course_code = 'DB101')),
((SELECT id FROM users WHERE username = 'student1'), (SELECT id FROM courses WHERE course_code = 'ADS101'));
