#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

###############################################
#
# User Management Tests
#
###############################################

# Function to create a user
create_user() {
  echo "Creating a new user..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "password123"
  }' "$BASE_URL/create-account")
  
  if echo "$response" | grep -q '"message": "Account created successfully"'; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to log in a user
login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "password123"
  }' "$BASE_URL/login")
  
  if echo "$response" | grep -q '"message": "Login successful"'; then
    echo "User logged in successfully."
  else
    echo "Failed to log in user."
    exit 1
  fi
}

###############################################
#
# Book Management Tests
#
###############################################

# Function to search for books
search_books() {
  echo "Searching for books..."
  response=$(curl -s -X GET "$BASE_URL/books/search?q=python")
  
  if echo "$response" | grep -q '"books"'; then
    echo "Book search successful."
  else
    echo "Failed to search for books."
    exit 1
  fi
}

# Function to add a book to the user's collection
add_book() {
  echo "Adding a book to the user's collection..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "title": "Learn Python",
    "author": "John Doe",
    "year": 2021
  }' "$BASE_URL/books/add")
  
  if echo "$response" | grep -q '"message": "Book added successfully"'; then
    echo "Book added successfully."
  else
    echo "Failed to add book."
    exit 1
  fi
}

# Function to retrieve the user's collection
get_collection() {
  echo "Retrieving the user's collection..."
  response=$(curl -s -X GET "$BASE_URL/books/collection?user_id=1")
  
  if echo "$response" | grep -q '"collection"'; then
    echo "Book collection retrieved successfully."
  else
    echo "Failed to retrieve book collection."
    exit 1
  fi
}

##########################################
# Execute Tests
##########################################

# Health check
check_health

# User management tests
create_user
login_user

# Book management tests
search_books
add_book
get_collection

echo "All smoke tests passed successfully!"