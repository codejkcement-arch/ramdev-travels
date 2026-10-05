INSERT INTO education.courses(code,title,slug,description,status,is_free,price)
VALUES
('REET-12','REET Level 1 & 2','reet-level-1-2','Complete REET preparation course','published',true,0),
('PATWARI','Patwari Complete Course','patwari-complete-course','Rajasthan Patwari preparation','published',true,0),
('GRAM-SEVAK','Gram Sevak','gram-sevak','Rajasthan GK and practice','published',true,0),
('CET','CET','cet','Maths and Reasoning preparation','published',true,0)
ON CONFLICT (code) DO NOTHING;

INSERT INTO education.tests(title,slug,description,status,duration_minutes,total_marks,total_questions)
VALUES
('Rajasthan Patwari Mock Test','rajasthan-patwari-mock-1','100 question mock test','published',120,200,100),
('REET Level 1 Test','reet-level-1-test-1','REET practice test','published',120,150,100)
ON CONFLICT (slug) DO NOTHING;
