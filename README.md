<h1> Python project to Connect MongoDB Atlas Database </h1>

<h2> Description</h2>
This is a simple application to test and learn a raw connection to a NoSQL database. It is a Remote NoSQL database hosted in MongoDB Atlas Database <br>

<h2>Project Details</h2>


1. Access MongoDB Atlas and create a Free Account -> https://www.mongodb.com/atlas/database
2. Create a Free Shared Instance
3. Configure a AWS provision region
4. Create a Cluster and name it
5. Create a login and password to sign in into the cluster
6. Create a python app
7. Create a .env file and add a variable to the password of the cluster
8. Copy Connection String from MongoDB Atlas
    1. Access the cluster
    2. Go to Overview
		3. Click button `CONNECT`
		4. Select `Connect your application` - Select Python Driver and Version (up to 3)
		5. Copy the Connection String Generated
9. Update the connection string and password in the files app.py and .env
10. Activate the virtual environment
11. run the file `python3 app.py run`

>> Cluster is an abstraction on top of a database. A database will be hosted inside the cluster<br>
>> The cluster must have Replica Set - 3 nodes - Meaning that we will have 3 servers running the database. Better scale and redundancy one goes down another replica assume<br>


>> Install
>> 1. Python Driver for MongoDB `install pymongo[srv]` 
>> 2. `python-dotenv`
