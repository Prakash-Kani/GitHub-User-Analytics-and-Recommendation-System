-- CREATE THE DATABASE 
CREATE DATABASE github;

USE github;

-- CREATING GITHUB REPOSITORIES DETAILS TABLE
 
CREATE TABLE IF NOT EXISTS repositories_details(
Owner VARCHAR(250),
Repo_Name VARCHAR(250),
Repo_Link VARCHAR(250),
Created_At DATE,
Description TEXT,
Forks_Count INT,
Repo_Fullname VARCHAR(250) PRIMARY KEY,
Repo_ID INT, 
Language_Used VARCHAR(250),
Last_Modified INT,
Pushed_At DATE,
Size INT,
Subscriber INT,
Stargazers INT,
Updated_At DATE,
Watchers_Counts INT, 
Commits INT);


-- INSERT QUERY FOR REPOSITORIES DETAILS TABLE 
INSERT INTO repositories_details
(Owner, Repo_Name, Repo_Link, Created_At, Description, Forks_Count, Repo_Fullname, Repo_ID, Language_Used, Last_Modified, Pushed_At, Size, Subscriber, Stargazers, Updated_At, Watchers_Counts, Commits)
VALUES ('nethajinirmal13',
 'allanasta',
 'https://github.com/nethajinirmal13/allanasta.git',
 '2022/08/05',
 Null,
 0,
 'nethajinirmal13/allanasta',
 521578606,
 'Shell',
 Null,
'2022/08/05',
 7,
 1,
 1,
'2022/08/05',
 1,
 1)
ON DUPLICATE KEY UPDATE
Owner = VALUES(Owner),
Repo_Name = VALUES(Repo_Name), 
Repo_Link = VALUES(Repo_Link), 
Created_At = VALUES(Created_At), 
Description = VALUES(Description), 
Forks_Count = VALUES(Forks_Count), 
Repo_Fullname = VALUES(Repo_Fullname), 
Repo_ID = VALUES(Repo_ID), 
Language_Used = VALUES(Language_Used), 
Last_Modified = VALUES(Last_Modified), 
Pushed_At = VALUES(Pushed_At), 
Size = VALUES(Size), 
Subscriber = VALUES(Subscriber), 
Stargazers = VALUES(Sargazers), 
Updated_At = VALUES(Updated_At), 
Watchers_Counts = VALUES(Watchers_Counts), 
Commits = VALUES(Commits);

select * from repositories_details;

-- To Retrieve the Repos Per Languages data.
SELECT Language_Used as Language, COUNT(*) as Count FROM repositories_details
                        WHERE Owner = 'Prakash-Kani' AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;
-- To Retrieve the Commits Per Languages data.
SELECT Language_Used as Language, sum(Commits) AS Commits FROM repositories_details
                        WHERE Owner = 'Prakash-Kani' AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;
                       
-- To Retrieve the Stargazers count Per Languages data.
SELECT Language_Used as Language, sum(Stargazers) AS Stars FROM repositories_details
                        WHERE Owner = 'Prakash-Kani' AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;

