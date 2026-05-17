DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS registration_counters;

CREATE TABLE registration_counters (
    course TEXT PRIMARY KEY,
    counter INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL,
    registration INTEGER NOT NULL
);
