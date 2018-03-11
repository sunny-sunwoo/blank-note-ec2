# Social Network UI

URL http://18.221.3.211/
Pyton 3.6.4<br>

I will build an increasingly sophisticated nano-blogging site. This site will eventually be a featureful, interactive web application photo upload, and quasi-real-time updates.

	+ The empty URL (i.e. http://localhost:8000/) will route to the first page(global stream) of my application.

	+ Using default Django database configuration based on a SQLite database file (named db.sqlite3) 
	  for storing user information

***

### Part #1. Social Network UI and Login

Implemented the **HTML pages** for my site and implement a **basic login function** using Django’s authentication package.

	+ Demonstrated the high­-level architecture of an MVC application, including basic features of the Django framework.

	+ Demonstrated a basic understanding objects to represent forms, hierarchical templates,
	  and user authentication using the Django framework.

	+ Gained experience using iterative development, similar to what I would encounter
	  using a modern agile software development process.

***

### Part #2. Social Network Models

Gained experience with sophisticated data management, including data models with complex relationships and the use of an ORM to execute queries using those relationships.

Achieved integration of data models with:

	+ modular, reusable views with inheritance

	+ form classes to encapsulate input validation
	
	+ image (or, in general, file) upload

***

### Part #3. AJAX

Increased familiarity with client-side web programming, including the use of JavaScript (and optionally—but hopefully—JavaScript libraries) for DOM manipulation and Ajax.

	+ The global and follower streams update with new posts and comments, without refreshing the HTML page, every 5 seconds, using Ajax.

	+ Logged-in users are able to add comments to posts anywhere posts are shown.

***

### Part #4. Deployment

Added email validation of user accounts and you will deploy your application to the cloud.

	1. When registering a new account:
		+ require that an email address to be provided,
		+ send, via email, a link that can be clicked on to validate the email address.

	2. Installed and configured MySQL.

	3. Deployed the social network application on AWS EC2.



