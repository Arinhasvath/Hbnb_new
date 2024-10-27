#!/bin/bash

echo "=== Testing Review API ==="

# Fonction pour afficher les réponses de manière claire
show_response() {
    local title="$1"
    local response="$2"
    echo -e "\n=== $title ==="
    echo "$response"
    echo "===================="
}

# 1. Créer les données nécessaires
echo -e "\n1. Creating prerequisite data..."

# 1.1 Create User
echo "1.1 Creating test user..."
USER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test'$(date +%s)'@example.com"
  }')
show_response "User Creation" "$USER_RESPONSE"
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "User ID: $USER_ID"

# 1.2 Create Place
echo "1.2 Creating test place..."
PLACE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "description": "A test place",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "'$USER_ID'"
  }')
show_response "Place Creation" "$PLACE_RESPONSE"
PLACE_ID=$(echo "$PLACE_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Place ID: $PLACE_ID"

# 2. Test Review Creation
echo -e "\n2. Testing Review Creation..."

# 2.1 Valid Review
echo "2.1 Creating valid review..."
REVIEW_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "'$USER_ID'",
    "place_id": "'$PLACE_ID'"
  }')
show_response "Valid Review Creation" "$REVIEW_RESPONSE"
REVIEW_ID=$(echo "$REVIEW_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

# 2.2 Invalid Review (Rating > 5)
echo "2.2 Testing invalid rating (>5)..."
curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Invalid rating",
    "rating": 6,
    "user_id": "'$USER_ID'",
    "place_id": "'$PLACE_ID'"
  }'

# 2.3 Invalid Review (Rating < 1)
echo "2.3 Testing invalid rating (<1)..."
curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Invalid rating",
    "rating": 0,
    "user_id": "'$USER_ID'",
    "place_id": "'$PLACE_ID'"
  }'

# 2.4 Invalid Review (Empty text)
echo "2.4 Testing empty text..."
curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "",
    "rating": 4,
    "user_id": "'$USER_ID'",
    "place_id": "'$PLACE_ID'"
  }'

# 3. Test Review Retrieval
echo -e "\n3. Testing Review Retrieval..."

# 3.1 Get All Reviews
echo "3.1 Getting all reviews..."
curl -s -X GET http://localhost:5000/api/v1/reviews/

# 3.2 Get Specific Review
echo "3.2 Getting specific review..."
curl -s -X GET "http://localhost:5000/api/v1/reviews/$REVIEW_ID"

# 3.3 Get Reviews by Place
echo "3.3 Getting reviews for place..."
curl -s -X GET "http://localhost:5000/api/v1/reviews/places/$PLACE_ID/reviews"

# 4. Test Review Update
echo -e "\n4. Testing Review Update..."

# 4.1 Valid Update
echo "4.1 Updating review..."
curl -s -X PUT "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated review text",
    "rating": 4
  }'

# 4.2 Invalid Update (Bad Rating)
echo "4.2 Testing invalid update..."
curl -s -X PUT "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 6
  }'

# 5. Test Review Deletion
echo -e "\n5. Testing Review Deletion..."

# 5.1 Delete Review
echo "5.1 Deleting review..."
curl -s -X DELETE "http://localhost:5000/api/v1/reviews/$REVIEW_ID"

# 5.2 Verify Deletion
echo "5.2 Verifying deletion..."
curl -s -X GET "http://localhost:5000/api/v1/reviews/$REVIEW_ID"

echo -e "\nTests completed."