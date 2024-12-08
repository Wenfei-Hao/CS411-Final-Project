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
# Health Check
#
###############################################

check_health() {
  echo "Checking API health status..."
  response=$(curl -s -X GET "$BASE_URL/api/health")
  if echo "$response" | grep -q '"status": "healthy"'; then
    echo "API health check passed."
  else
    echo "API health check failed."
    echo "Response: $response"
    exit 1
  fi
}

###############################################
#
# User Management Tests
#
###############################################

create_user() {
  echo "Creating a test user..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "password123"
  }' "$BASE_URL/create-account")

  if echo "$response" | grep -q '"message": "Account created successfully"'; then
    echo "User creation passed."
  else
    echo "User creation failed."
    echo "Response: $response"
    exit 1
  fi
}

login_user() {
  echo "Logging in the test user..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "password123"
  }' "$BASE_URL/login")

  if echo "$response" | grep -q '"message": "Login successful"'; then
    echo "User login passed."
  else
    echo "User login failed."
    echo "Response: $response"
    exit 1
  fi
}

###############################################
#
# Book Management Tests
#
###############################################

search_books() {
  echo "Searching for books (Google Books API)..."
  response=$(curl -s -X GET "$BASE_URL/books/details?title=python")
  
  if echo "$response" | grep -q '"title"'; then
    echo "Book search passed."
  else
    echo "Book search failed."
    echo "Response: $response"
    exit 1
  fi
}

add_book() {
  echo "Adding a book to the collection..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "title": "Learn Python",
    "author": "John Doe",
    "year": 2021
  }' "$BASE_URL/books")

  if echo "$response" | grep -q '"message": "Book added successfully"'; then
    echo "Add book passed."
  else
    echo "Add book failed."
    echo "Response: $response"
    exit 1
  fi
}

get_collection() {
  echo "Retrieving the user's book collection..."
  response=$(curl -s -X GET "$BASE_URL/books/collection?user_id=1")

  if echo "$response" | grep -q '"collection"'; then
    echo "Retrieve collection passed."
  else
    echo "Retrieve collection failed."
    echo "Response: $response"
    exit 1
  fi
}

###############################################
#
# Run All Tests
#
###############################################

echo "Running Smoke Tests for CS411 Final Project..."
check_health
create_user
login_user
search_books
add_book
get_collection
echo "All smoke tests passed successfully!"