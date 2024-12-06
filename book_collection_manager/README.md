High Level Description:
   The Book Collection Manager is a web-based application designed to help users organize and manage their personal book collections efficiently. By integrating with the Google Books API, the application allows users to search for books, retrieve detailed information, and add selected titles to their collection. It also features secure user authentication, ensuring a personalized and safe user experience. The application leverages modern web development practices, enabling seamless API interaction, secure data storage, and deployment scalability through Docker.


API Routes:
   Route: /book/add
       Request Type: POST
       Purpose: Users can add books to their collection by providing details such as title, author, and publication year.
       Request Body:
           title (String): The title of the book.
           author (String): The author of the book.
           year (Integer): The publication year of the book.
       Response Format:
           Sucess Response Example:
               Code: 200
               Content:
                   {
                       "message": "Book added successfully"
                   }
               Example Request:
                   {
                       "title": "Learn Python",
                       "author": "John Doe",
                       "year": 2020
                   }
               Example Response:
                   {
                       "message": "Book added successfully"
                   }
   Route: /books/<book_id>
       Request Type: GET
       Purpose: Retrieve information about a specific book in the user's collection using its ID.
       Request Parameters:
           book_id (Integer): The ID of the book to retrieve.
       Response Format:
           Success Response Example:
               Code: 200
               Content:
                   {
                       "id": 1,
                       "title": "Learn Python",
                       "author": "John Doe",
                       "year": 2020,
                       "status": "unread"
                   }
               Example Request:
                   GET /books/1 HTTP/1.1
                   Host: localhost:5000
               Example Response:
                   {
                       "id": 1,
                       "title": "Learn Python",
                       "author": "John Doe",
                       "year": 2020,
                       "status": "unread"
                   }
  
   Route: /books/update-status
       Request Type: PUT
       Purpose: Allows users to update the reading status of a book, marking it as "read" or "unread."
       Request Body:
           book_id (Integer): The ID of the book.
           status (String): The new reading status ("read" or "unread").
       Response Format:
           Success Response Example:
               Code: 200
               Content:
                   {
                       "message": "Book status updated successfully"
                   }
               Example Request:
                   {
                       "book_id": 1,
                       "status": "read"
                   }
               Example Response:
                   {
                       "message": "Book status updated successfully"
                   }
   Route: /books/delete
       Request Type: DELETE
       Purpose: Enables users to remove books from their collection.
       Request Body:
           book_id (Integer): The ID of the book to delete.
       Response Format:
           Success Response Example:
               Code: 200
               Content:
                   {
                       "message": "Book deleted successfully"
                   }
               Example Request:
                   {
                       "book_id": 1
                   }
               Example Response:    
                   {
                       "message": "Book deleted successfully"
                   }
   Route: /books/details
       Request Type: GET
       Purpose: Retrieves detailed information about a book by title using the Google Books API. Details include a summary, publication date, and cover image.
       Request Parameters:
           title (String): The title of the book to query.
       Response Format:
           Success Response Example:
               Code: 200
               Content:
                   {
                       "title": "Learn Python",
                       "author": "John Doe",
                       "description": "A comprehensive guide to learning Python programming.",
                       "published_date": "2020-01-01",
                       "cover_image": "https://example.com/cover.jpg"
                   }
               Example Request:
                   GET /books/details?title=Learn%20Python HTTP/1.1
                   Host: localhost:5000
