<h1>Easy Table</h1>
<p>Hi, this is the first project that I built from scratch. After learning SQL and Flask, I really wanted to test more about getting, adding, updating, and dropping data records to and from the database. Therefore, I decided to develop a web application where you can manipulate data records from the database like SQL but much simpler and easier with graphical user interfaces.</p>
<p>Website Link: https://easy-table-never.herokuapp.com</p>

<h2>Features Supported</h2>
<ul>
	<li>hi</li>
	<li>hello</li>
</ul>


<div> I used bootstrap 5.1.3 for easy manipulation of CSS and some Javascript. Since, I am good with Python, I chose Flask to write the whole web application. As database language, I wanted to edit and delete my columns, SQLite does not support that. Hence, I had to learn MySQL and used it for the project.For queries, I used mysql.connector library. I also used Font Awesome to get cool icons.</div>
	After choosing the languages and frameworks, I planned my project step by step in Notion app. My first task was to make a register, login and logout for users' accounts. So created easy table database in MySQL and hosted as "localhost". I created users table with id, username, hash columns. id is Primary key and auto increment. Since Professor David Malan taught us to never store passwords in plain text, I used werkzeug.security library for check_password_hash and generate_password_hash functions. And store passwords as hashs. Then, I used flask_session library to Login and Logout the users.
	For second task, I created items table with Name as a base column. With user_id as Foreign key, and item_id as Primary key. To show items only related to the user, I reference user_id to id from users table. I show all the data of the items table on index.html page.
	As a third task, I try to manipulate columns of the items table. I excluded Name as a base column. I put +Add new column button in the right most header. By clicking it, new input text box will appear. I can enter the name of the new column. When I submit that, I will alter the table and add new column with name as user entered and type as TEXT NOT NULL. If I click the delete button beside column name, it will delete the whole column. If I click the edit button beside column name, I would be able to rename the column. I won't let the user to create column with other data types because of some difficulties I was facing when writing query codes for other data types.
	As a forth task, I try to manipulate items of the items table. I can add new items, edit items and delete items same as columns. The most difficult about this is I had to try and think many methods to manipulate items correctly, since the columns are dynamic. Because column names and amount of columns are changing, I had to loop those data and add as string to variable name "query", and data as list "data". I couldn't hard code them like I did with columns.
	After finishing manipulating data of the table, I added search and sort features as final task. To make it more advanced I let users search and sort by each columns. And also choose ascending or descending order to sort. I was facing some difficulties while creating dropdown selection for search columns, so I chose input type "radio".
	For future improvements, I still need to handle all errors. And also fix that when one user delete the column, it delete the whole column of the items table. I think I should create a table for each users.
