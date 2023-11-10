-- CREATE THE DATABASE 
CREATE DATABASE github;

USE github;

-- CREATING GITHUB USER DETAILS TABLE
 
CREATE TABLE IF NOT EXISTS userdetails(
User_Name VARCHAR(250),
Login VARCHAR(250) PRIMARY KEY,
Bio TEXT,
Joined_At DATE,
Email VARCHAR(250),
Location VARCHAR(250),
Company VARCHAR(250), 
Following_Count INT,
Followers_Count INT,
Public_Repos INT,
Avatar_url VARCHAR(250),
Profile_url VARCHAR(250),
Languages_Used TEXT,
Starred_Repo LONGTEXT);

-- INSERT QUERY FOR USER DETAILS TABLE 
INSERT INTO userdetails
(User_Name, Login, Bio, Joined_At, Email, Location, Company, Following_Count, Followers_Count, Public_Repos, Avatar_url, Profile_url, Languages_Used, Starred_Repo) 
VALUES ('nethaji nirmal',
  'nethajinirmal13',
  'always an aspirant\r\n',
  '2023-12-23',
  'nethajinirmal13@gmail.com',
  'chennai',
  'thinkspert',
  1,
  78,
  60,
  'https://avatars.githubusercontent.com/u/15277998?v=4',
  'https://github.com/nethajinirmal13',
  'Procfile CSS Python Shell Batchfile HTML Hack C# Makefile Java TypeScript PHP Dockerfile Solidity JavaScript Jupyter Notebook C++',
  'Avaiga/taipy JagadeeshwaranM/Data_Engineering_Simplified')
ON DUPLICATE KEY UPDATE
User_Name = VALUES(User_Name), 
Login = VALUES(Login), 
Bio = VALUES(Bio), 
Joined_At = VALUES(Joined_At),
Email = VALUES(Email),
Location = VALUES(Location),
Company = VALUES(Company),
Following_Count = VALUES(Following_Count),
 Followers_Count = VALUES(Followers_Count),
 Public_Repos = VALUES(Public_Repos),
 Avatar_url = VALUES(Avatar_url),
 Profile_url = VALUES(Profile_url),
 Languages_used = VALUES(Languages_Used),
 Starred_Repo = VALUES(Starred_Repo);

