High Level Description:
   The Book Collection Manager is a web-based application designed to help users organize and manage their personal book collections efficiently. By integrating with the Google Books API, the application allows users to search for books, retrieve detailed information, and add selected titles to their collection. It also features secure user authentication, ensuring a personalized and safe user experience. The application leverages modern web development practices, enabling seamless API interaction, secure data storage, and deployment scalability through Docker.


# Routes:


# Route: /health
    Request Type: GET
    Purpose: Health check route to confirm the application is running.
    Request Body:
        None

    Response Format: JSON
        Success Response Example:
            Code: 200
            Content: {"status": "healthy"}
    
    Example Request:
        GET /health HTTP/1.1
        Host: localhost:5000
    
    Example Response:
        {
            "status": "healthy"
        }



# Route: /create-account
    Request Type: POST
    Purpose: Creates a new user account with a username and password.
    Request Body:
        username (String): User's chosen username.
        password (String): User's chosen password.

    Response Format: JSON
        Success Response Example:
            Code: 201
            Content: {"message": "Account created successfully", "user_id": 1}
    
    Example Request:
        {
            "username": "newuser123",
            "password": "securepassword"
        }
    
    Example Response:
        {
            "message": "Account created successfully"
            "user_id": 1
        }


# Route: /login
    Request Type: POST
    Purpose: Logs in a user by verifying their username and password.
    Request Body:
        username (String): The username of the user.
        password (String): The password of the user.
    Response Format: JSON
        Success Response Example:
            Code: 200
            Content: {"message": "Login successful"}
    
    Error Response Example:
        Code: 401
        Content: {"error": "Invalid username or password"}
    
    Example Request:
        {
            "username": "newuser123",
            "password": "securepassword"
        }
    
    Example Response:
        {
            "message": "Login successful"
        }



# Route: /update-password
    Request Type: PUT
    Purpose: Updates the password for an existing user.
    Request Body:
        username (String): The username of the user.
        new_password (String): The new password to set for the user.
    
    Response Format: JSON
        Success Response Example:
            Code: 200
            Content: {"message": "Password updated successfully"}
    
    Error Response Example:
        Code: 404
        Content: {"error": "User not found"}
    
    Example Request:
        {
            "username": "newuser123",
            new_password": "newsecurepassword"
        }
    
    Example Response:
        {
            "message": "Password updated successfully"
        }

    

# Route: /books
    Request Type: POST
    Purpose: Adds a new book to the database for a specific user.
    Request Body:
        title (String): The title of the book (required).
        author (String): The author of the book (required).
        year (String): The publication year of the book (optional).
        user_id (Integer): The ID of the user who owns the book (optional, defaults to 1).

    Response Format: JSON
        Success Response Example:
            Code: 201
            Content: {"message": "Book added successfully", "book_id": 1}
    
    Error Response Example:
        Code: 400
        Content:{"error": "Title and Author are required"}
    
    Example Request:
        {
            "title": "Learn Python",
            "author": "John Doe",
            "year": "2020",
            "user_id": 1
        }
    
    Example Response:
        {
            "message": "Book added successfully",
            "book_id": 1
        }



# Route: /books/<book-id>
    Request Type: GET
    Purpose: Retrieves a book by its ID.
    Request Parameters:
        book_id (Integer): The ID of the book to retrieve (required).
    
    Response Format: JSON
        Success Response Example:
            Code: 200
            Content:
                {
                    "id": 1,
                    "title": "Learn Python",
                    "author": "John Doe",
                    "year": "2020",
                    "status": "unread",
                    "cover_image": null,
                    "summary": null
                }

    Error Response Example:
        Code: 404
        Content: {"error": "Book not found"}

    Example Request:
        GET /books/1 HTTP/1.1
        Host: localhost:5000

    Example Response:
        {
            "id": 1,
            "title": "Learn Python",
            "author": "John Doe",
            "year": "2020",
            "status": "unread",
            "cover_image": null,
            "summary": null
        }



# Route: /books/<book_id>
    Request Type: PUT
    Purpose: Updates the reading status of a book by its ID.
    Request Body:
        status (String): The new reading status ("read" or "unread") (required).
    
    Response Format: JSON
        Success Response Example:
            Code: 200
            Content: {"message": "Reading status updated"}
    
    Error Response Example:
        Code: 404
        Content: {"error": "Book not found"}
        Code: 400
        Content: {"error": "Invalid status. Use 'read' or 'unread'."}
    
    Example Request:
        {
            "status": "read"
        }
    
    Example Response:
        {
            "message": "Reading status updated"
        }



# Route: /books/<book_id>
    Request Type: DELETE
    Purpose: Deletes a book from the database by its ID.
    Request Parameters:
        book_id (Integer): The ID of the book to delete (required).

    Response Format: JSON
        Success Response Example:
            Code: 200
            Content:
                {
                    "message": "Book deleted successfully"
                }
    
    Error Response Example:
        Code: 404
        Content:
            {
                "error": "Book not found"
            }
    
    Example Request:
        DELETE /books/1 HTTP/1.1
        Host: localhost:5000

    Example Response:
        {
            "message": "Book deleted successfully"
        }



# Route: /books/details
    Request Type: GET
    Purpose: Fetches details about a book by title using the Google Books API.
    Request Parameters:
        title (String): The title of the book to search (required).
        
    Response Format: JSON
        Success Response Example:
            Code: 200
            Content:
                {
                    "title": "Learn Python",
                    "author": "John Doe",
                    "published_date": "2020-01-01",
                    "summary": "A comprehensive guide to Python programming.",
                    "cover_image": "https://example.com/cover.jpg"
                }

    Error Response Example:
        Code: 404
        Content:
            {
                "error": "No book details found"
            }
        Code: 400
        Content:
            {
                "error": "Title is required"
            }

    Example Request:
        GET /books/details?title=Learn%20Python HTTP/1.1
        Host: localhost:5000

    Example Response:
        {
            "title": "Learn Python",
            "author": "John Doe",
            "published_date": "2020-01-01",
            "summary": "A comprehensive guide to Python programming.",
            "cover_image": "https://example.com/cover.jpg"
        }



# Route: /books/collection
    Request Type: GET
    Purpose: Retrieves the collection of books for a specific user by their user ID.
    Request Parameters:
        user_id (Integer): The ID of the user whose collection to retrieve (required).
    
    Response Format: JSON
        Success Response Example:
        Code: 200
        Content:
            {
                "collection": [
                    {
                        "id": 1,
                        "title": "Learn Python",
                        "author": "John Doe",
                        "year": "2020",
                        "status": "read"
                    },
                    {
                        "id": 2,
                        "title": "Master Flask",
                        "author": "Jane Doe",
                        "year": "2021",
                        "status": "unread"
                    }
                ]
            }

    Error Response Example:
        Code: 400
        Content:
            {
                "error": "user_id is required"
            }

    Example Request:
        GET /books/collection?user_id=1 HTTP/1.1
        Host: localhost:5000
    
    Example Response:
        {
            "collection": [
                {
                    "id": 1,
                    "title": "Learn Python",
                    "author": "John Doe",
                    "year": "2020",
                    "status": "read"
                },
                {
                    "id": 2,
                    "title": "Master Flask",
                    "author": "Jane Doe",
                    "year": "2021",
                    "status": "unread"
                }
            ]
        }



# Route: /api/db-check
    Request Type: GET
    Purpose: Verifies the database connection and table setup.
    Request Format: None (No body or parameters needed).

    Response Format:
        Success Example:

        {
            "database_status": "healthy"
        }
    Failure Example:
        {
            "error": "Database connection failed"
        }

    Example Request:
        curl -X GET http://localhost:5000/api/db-check
    
    Example Response:
        {
            "database_status": "healthy"
        }



# Steps to run application

1) Install Docker, Python, and Pip
2) Obtain a Google Books API Key from the Google Cloud Console
3) Add the API key to the .env file
3) Build the docker image:  docker build -t book_collection_manager .
4) Run the docker container:  docker run -d -p 5000:5000 --name book_collection_manager_container book_collection_manager
