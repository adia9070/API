# API
A small CRUD API in flask with unittesting

HOW TO RUN CODE:
INSTALL ALL LIBRARY FROM REQUIREMENTS.TXT

Execute **run.py**

**All API End Points:**

FOR GET (SINGLE RECORD OF TYPE) : - /get/TYPE/ID

FOR GET (ALL RECORD OF TYPE) : - /get/TYPE

**For fetching use GET requet ** 
  
FOR CRAETE : /create/TYPE

**For creation use post request**
 
 
FOR UPDATE : /update/TYPE/ID

**for udpate use PUT request**
  

Database - Sqlite3 is used with this API and the location run.py will be executed, the database will be created in the same directory

**ORM is used for database mapping so in case database file is deleted, use the following code to create tables**

from curd_api_package import engine, Base

Base.metadata.create_all(engine)

3 Tables is created inside database - 

1). Song - **id, name, duration, uploaded_time**

2). podcast - **id, name, duration, uploaded_time , participant1, participant2, participant3 ............ participant6, participant7, participant10** 

3). AudioBook - **id, title, author, narrator, duration, uploaded_time**

All the column name in the above table info will be used as key while sending JSON data to server (please use same name shown above)

**Example of API:**

GET : /get/song/1  or /get/song  or /get/podcast  or /get/podcast/1

CREATE : /create/podcast  , JSON = {"id":1, "name":"life", "duration":120, "uploaded_time":"2021-02-20 22:50:00", "host":"Aditya", "participants":["Aman","Ankur"]}

UPDATE : /update/podcast/1 , JSON = {"id":1, "name":"life", "duration":120, "uploaded_time":"2021-02-20 22:50:00", "host":"Aditya", "participants":["Aman","Ankur"]}

DELETE: /delete/podcast/1 
