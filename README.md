#  **REST APIs with Flask and Python**
This is a Flask project that demonstrates the development of a RESTful API with authentication, database integration, and interactive documentation using Swagger UI.
# Project Overview
This Flask project serves as the foundation for building a robust RESTful API. It incorporates various libraries and frameworks, including Flask, Flask-RESTful, Flask-JWT, Flask swagger ui and SQLAlchemy ans PostgreSQL for database and flask limiter to limit the requests.

# Getting Started

These instructions will let you run project on your local machine for development and testing purposes. 

### **Prerequisites**

Make sure you have installed Python 3 on your device

Run the command to install the requirenemnts
```
pip install -r requirements.txt

```

### **Modules**
* [Flask](https://pypi.org/project/Flask/):\
&emsp;&emsp;Flask is a lightweight web framework for Python, ideal for building web applications and APIs.
* [Flask-RESTful](https://pypi.org/project/Flask-RESTful/):\
&emsp;&emsp;Flask-RESTful is an extension for Flask that simplifies the creation of RESTful APIs, making it easier to define resources and endpoints.
* [Flask-Swagger-UI](https://pypi.org/project/flask-swagger-ui/):\
&emsp;&emsp;Flask-Swagger-UI is used to generate a user-friendly Swagger UI interface for API documentation. It allows developers and users to explore and test API endpoints easily.
* [Flask-JWT](https://pypi.org/project/Flask-JWT/):\
&emsp;&emsp;Flask-JWT is a library for handling JSON Web Tokens (JWT) authentication in Flask applications. It provides secure user authentication and token-based access control.
* [SQLAlchemy](https://pypi.org/project/SQLAlchemy):\
&emsp;&emsp;SQLAlchemy is a popular SQL toolkit and Object-Relational Mapping (ORM) library used for database operations. It enables the application to interact with a relational database.
* [Flask_swagger_ui](https://pypi.org/project/flask-swagger-ui/):\
&emsp;&emsp;This is a Python library that provides integration with Swagger UI for Flask applications.
* [Flask_limiter](https://pypi.org/project/Flask-Limiter/):\
&emsp;&emsp;
Limiter class from the flask_limiter module in a Flask application. The flask_limiter extension is commonly used to implement rate limiting in Flask applications.

<br>

# Project structure
```
  flask_assignment/
  |--- .env/
  |--- modules/
  |    |    |--- __init__.py
  |    |    |--- item.py
  |    |    |--- user.py
 
  |--- app/
  |--- db.py/
  |--- security.py/
  |--- static/openapi.json
  

```
<br>

# Step to start flask rest api

A step by step series of examples that tell you how to get a development env running

1. Install virtual environment
```
pip install virtualenv
```
2. Create virtual environment and activate inside your flask-rest-api directory according the above structure
```
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . env/bin/activate
```
1. set the KEY variable in .config file. Which is the app secrete key.
2. set the database configuration parameters in .config file
   
3. Run  the `app.py` file.
```python
Access the API at http://127.0.0.1:5000
```
* I have used HTTpie for general purpose.
  * HTTPie is an open-source tool that lets you test APIs with a simple and intuitive interface.
    * [HTTpie](https://httpie.io/)
* **For testing** procedure mentioned below in this file. In Testing headline section. 
<br>


# Components
## **API Endpoints**
Here are some of the main API endpoints:

POST&emsp;**/api/auth/signup**: To register new user or signup.\
POST&emsp;**/api/auth/login**: To authenticate user and this will return a JWT

GET&emsp;&emsp;  **/api/notes:** &emsp; get a list of all notes for the authenticated user.\
GET&emsp; **/api/notes/:id:** &emsp; get a note by ID for the authenticated user.\
POST&emsp; **/api/notes:**&emsp; create a new note for the authenticated user.\
PUT&emsp; **/api/notes/:id:** &emsp; update an existing note by ID for the
authenticated user.\
DELETE&emsp; **/api/notes/:id:** &emsp; delete a note by ID for the authenticated user.\
POST&emsp; **/api/notes/:id/share:** &emsp; share a note with another user for the authenticated user.\
GET&emsp; **/api/search?q=:query:** &emsp; search for notes based on keywords for the authenticated user.\
<br>
For detailed information about available endpoints and request/response formats, refer to the Swagger Documentation section.

## **Authentication**
This project uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, follow these steps:

Register a user account or obtain valid credentials.\
&emsp;**/register**: To regiester new user

Authenticate by sending a POST request to **/api/auth/login** with your credentials to receive a JWT token.

Include the JWT token in the Authorization header of your requests to access protected resources.\
We need JWT toke to access all request.

## **Limiter**
Flask-Limiter is a Flask extension that provides rate limiting for your Flask applications. Rate limiting is a technique used to control the number of requests a user or client can make to your application over a specified period.
As this is inbuilt and easy to implement so i choose this.

**In project you can perform 100 per minute each request. You can set the limit of your choice.**
\
e.g.

```
@limiter.limit("100 per minute")
# using this decorater we can limit the number of requests, like 100 request per min 
```

```
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
)
```
* "memory://"
  * **"memory://"**: In-memory storage suitable for development, testing, and scenarios where persistence is not a requirement. 
  * **Redis:** Can use redis also. It hasExternal, persistent storage suitable for production, scalability, and maintaining data across application restarts.

 

## **Database**
The project uses PostgresSQL to interact with the database. Make sure to set up your database connection and models according to your requirements. Refer to the models.py file for database schema.

PostgreSQL is a powerful open-source relational database management system (RDBMS) known for its reliability, extensibility, and adherence to SQL standards.I have intensively worked with SQL and PostgeSQL so i used this database.According to the data we encounter can use other database also like the mongoDB.

The choice of a database system depends on the specific requirements of the application, the nature of the data, and other factors such as scalability, performance, and ease of development. 

* **Database** : assignmentFlask.db
* **Tables**
  * items
    * Schema
      ```python
      | Column Name  | Data Type  |  Description                    |
      |--------------|------------|---------------------------------|
      | id           | Integer    | ID of note                      |
      | user_id      | Integer    | User ID                         |
      | note         | String     | notes data                      |
    
       ```
      ```
      Primary key: id
      Foreign Key: user_id, refer to user table.
      ```

  * users
    * Schema
      ```python
      | Column Name  | Data Type  |  Description              |
      |--------------|-----------|----------------------------|
      | id           | Integer    | Unique identifier         |
      | username     | Text       | Name of the user          |
      | password     | Text       | Password of user to login |
      ```
      ```
      Primary Key: id
      ```

## **Testing**
To test the url i have used PyTest framework
* open the test_api_app.py file
* Run commnad in terminal
  ```
  pytest -s test_api_app.py 
  ``` 
* Used Flask application with a SQLite in-memory database to do operation and data addition. This is a common setup for testing Flask applications without affecting a production database.
  

### **Testing cases**
* **/api/auth/signup**: To register new user or signup.
  * POST request
    * **case**
        * user created without issue , 200
        * user already present , 409

* **/api/auth/login**: To authenticate user and this will return a JWT
  * POST request
    * **case**
        * user logged in, token created, 200
        * Invalid credentials, Unauthorized. (wrong password or user not found), 401


* **/api/notes:** &emsp; get a list of all notes for the authenticated user.
   * GET request - get all notes of th authenticated user
     * **case**
        * The authenticated user have notes, 200
        * if user have no notes, 404
   * POST request - To  aded note to user logged in.
     * **case**
        * Notes were sent and they saved in database, 200
        * No notes were sent, empty note filed, 400
          * empty notes are not be saved in database.

* **/api/notes/:id:** &emsp; get a note by ID for the authenticated user.
  * GET request - To get the note of particular id
    * **case**
      * The authenticated user have notes of id mentioned, 200
       * if user have no notes of id mentioned, 404
  * PUT request - when the user want to update the note of particular ID.
    * **case** 
      * Note of ID updates successfully ,200
      * user have no note present of this id to update, 404 
      * if user try to update notes to null value (user can delete node instead of storing empty notes), 400

  * DELETE request - Delete a note by ID for the authenticated user.
    * **case**
      * Note of ID deleted successfully ,200
      * user have no note present of this id to delete, 404 
  
* **/api/notes/:id/share:** &emsp; share a note with another user for the authenticated user.
  * POST request - To share the note with outher useer by authenticated user.
    * **case**
      * Notes successfully shared with mentioned id, 200
      * You are sharing notes with yourself, which you already have,400
      * User to which you are sending notes does not exist, 400
      * you have no notes present to share,404

* **/api/search?q=:query:** &emsp; search for notes based on keywords for the authenticated user.
  * GET request - To search in users note for notes based on particular keyword. (used case insensitive senario)
    * found the notes having the keyword, 200
    * No notes have the matching word you mentioned", 400


## **Swagger Documentation**
Interactive API documentation is available using Swagger UI. Access it at http://localhost:5000/swagger after running the application. Explore and test the API endpoints directly from the Swagger UI interface



## **Conclusion**
This Flask project showcases the development of a RESTful API with secure user authentication, database integration, and interactive documentation using Swagger UI. It provides a solid foundation for building web applications and services that require API functionality.
