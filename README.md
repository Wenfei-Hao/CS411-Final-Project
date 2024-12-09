# Book Collection Manager:
## High Level Description:
The Book Collection Manager is a web-based application designed to help users organize and manage their personal book collections efficiently. By integrating with the Google Books API, the application allows users to search for books, retrieve detailed information, and add selected titles to their collection. It also features secure user authentication, ensuring a personalized and safe user experience. The application leverages modern web development practices, enabling seamless API interaction, secure data storage, and deployment scalability through Docker.

## Features:

- **User Account Management**:
  - Create an account
  - Log in
  - Update password
- **Add Books**: 
  - Users can add books to their collection by providing details such as title, author, and publication year.
- **Get Book by ID**: 
  - Users can retrieve information about a specific book in their collection using its ID.
- **Update Reading Status**: 
  - Allows users to mark books as "read" or "unread," helping them track their reading progress.
- **Delete Books**: 
  - Enables users to remove books from their collection.
- **Get Book Details**: 
  - Users can query detailed information about a book by title using the Google Books API. The details include a summary, publication date, and cover image.
---

## Setup Instructions:
1. **...**
2. **...**
---

## API Routes:
#### Route: /book/add
- **Request Type:** `POST`
- **Purpose:** Users can add books to their collection by providing details such as title, author, and publication year.
- **Request Body:**
    - title (String): The title of the book.
    - author (String): The author of the book.
    - year (Integer): The publication year of the book.
- **Response Format:**
    - Sucess Response Example:
        - Code: 200
        - Content:
            ```json
            {
              "message": "Account created successfully"
            }
            ```
        - Example Request:
            ```json
            {
               "title": "Learn Python",
               "author": "John Doe",
               "year": 2020
            }
            ```
        - Example Response:
            ```json
            {
                "message": "Book added successfully"
            }
            ```

#### Route: /books/<book_id>
- **Request Type:** `GET`
- **Purpose:** Retrieve information about a specific book in the user's collection using its ID.
- **Request Parameters:**
    - book_id (Integer): The ID of the book to retrieve.
- **Response Format:**
    - Sucess Response Example:
        - Code: 200
        - Content:
            ```json
            {
               "id": 1,
               "title": "Learn Python",
               "author": "John Doe",
               "year": 2020,
               "status": "unread"
            }
            ```
        - Example Request:
            ```
                GET /books/1 HTTP/1.1
                Host: localhost:5000
            ```
        - Example Response:
            ```json
            {
               "id": 1,
               "title": "Learn Python",
               "author": "John Doe",
               "year": 2020,
               "status": "unread"
            }
            ```

#### Route: /books/update-status
- **Request Type:** `PUT`
- **Purpose:** Allows users to update the reading status of a book, marking it as "read" or "unread."
- **Request Body:**
    - book_id (Integer): The ID of the book.
    - status (String): The new reading status ("read" or "unread").
- **Response Format:**
    - Sucess Response Example:
        - Code: 200
        - Content:
            ```json
            {
               "message": "Book status updated successfully"
            }
            ```
        - Example Request:
            ```json
            {
                "book_id": 1,
                "status": "read"
            }
            ```
        - Example Response:
            ```json
            {
               "message": "Book status updated successfully"
            }
            ```

#### Route: /books/delete
- **Request Type:** `DELETE`
- **Purpose:** Enables users to remove books from their collection.
- **Request Body:**
    - book_id (Integer): The ID of the book to delete.
- **Response Format:**
    - Sucess Response Example:
        - Code: 200
        - Content:
            ```json
            {
               "message": "Book deleted successfully"
            }
            ```
        - Example Request:
            ```json
            {
                "book_id": 1
            }
            ```
        - Example Response:
            ```json
            {
               "message": "Book deleted successfully"
            }
            ```

#### Route: /books/details
- **Request Type:** `GET`
- **Purpose:** Retrieves detailed information about a book by title using the Google Books API. Details include a summary, publication date, and cover image.
- **Request Parameters:**
    - title (String): The title of the book to query.
- **Response Format:**
    - Sucess Response Example:
        - Code: 200
        - Content:
            ```json
            {
               "title": "Learn Python",
                "author": "John Doe",
               "description": "A comprehensive guide to learning Python programming.",
               "published_date": "2020-01-01",
                "cover_image": "https://example.com/cover.jpg"
            }
            ```
        - Example Request:
            ```json
            GET /books/details?title=Learn%20Python HTTP/1.1
            Host: localhost:5000
            ```
        - Example Response:
            ```json
            {
               "title": "Learn Python",
                "author": "John Doe",
               "description": "A comprehensive guide to learning Python programming.",
               "published_date": "2020-01-01",
                "cover_image": "https://example.com/cover.jpg"
            }
            ```
