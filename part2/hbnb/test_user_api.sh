#!/bin/bash

echo "=== Testing User API ==="
echo "1. Creating first user..."
RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}')
echo "Response: $RESPONSE"
USER_ID=$(echo $RESPONSE | jq -r '.id')
echo "User ID: $USER_ID"

echo -e "\n2. Testing duplicate email..."
curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "john@example.com"
}'

echo -e "\n3. Testing invalid data..."
curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "",
    "last_name": "Doe",
    "email": "invalid-email"
}'

echo -e "\n4. Getting specific user..."
curl -s -X GET "http://localhost:5000/api/v1/users/$USER_ID"

echo -e "\n5. Updating user..."
curl -s -X PUT "http://localhost:5000/api/v1/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Doe",
    "email": "johnny.doe@example.com"
}'

echo -e "\n6. Getting all users..."
curl -s -X GET http://localhost:5000/api/v1/users/