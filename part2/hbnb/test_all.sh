#!/bin/bash

# Fonctions utilitaires
show_response() {
    local title="$1"
    local response="$2"
    echo -e "\n=== $title ==="
    echo "$response" | python3 -m json.tool || echo "$response"
    echo "===================="
}

extract_id() {
    local response="$1"
    if [ -z "$response" ]; then
        echo ""
        return
    fi
    ID=$(echo "$response" | python3 -c '
import sys, json
try:
    print(json.loads(sys.stdin.read()).get("id", ""))
except:
    print("")
')
    echo "$ID"
}

# Variables pour stocker les IDs
echo "======================================"
echo "Starting HBnB API Integration Tests..."
echo "======================================"

# 1. USER TESTS
echo -e "\n=== 1. USER TESTS ==="

# 1.1 Créer un utilisateur
echo "1.1 Testing User Creation..."
USER_CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Test", "last_name": "User", "email": "test'$(date +%s)'@example.com"}')

show_response "Create User Response" "$USER_CREATE_RESPONSE"
USER_ID=$(extract_id "$USER_CREATE_RESPONSE")
echo "User ID: $USER_ID"

if [ -z "$USER_ID" ]; then
    echo "Failed to create user. Exiting tests."
    exit 1
fi

# 1.2 Get Users
echo "1.2 Getting all users..."
USERS_RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/users/)
show_response "All Users" "$USERS_RESPONSE"

# 2. PLACE TESTS
echo -e "\n=== 2. PLACE TESTS ==="
echo "2.1 Creating place..."

PLACE_CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "description": "A test place",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "'$USER_ID'"
}')

show_response "Create Place Response" "$PLACE_CREATE_RESPONSE"
PLACE_ID=$(extract_id "$PLACE_CREATE_RESPONSE")
echo "Place ID: $PLACE_ID"

# 3. AMENITY TESTS
echo -e "\n=== 3. AMENITY TESTS ==="
echo "3.1 Creating amenity..."

AMENITY_CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}')

show_response "Create Amenity Response" "$AMENITY_CREATE_RESPONSE"
AMENITY_ID=$(extract_id "$AMENITY_CREATE_RESPONSE")
echo "Amenity ID: $AMENITY_ID"

# 4. REVIEW TESTS
if [ ! -z "$PLACE_ID" ] && [ ! -z "$USER_ID" ]; then
    echo -e "\n=== 4. REVIEW TESTS ==="
    echo "4.1 Creating review..."

    REVIEW_CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/reviews/ \
      -H "Content-Type: application/json" \
      -d '{
        "text": "Great place!",
        "rating": 5,
        "user_id": "'$USER_ID'",
        "place_id": "'$PLACE_ID'"
    }')

    show_response "Create Review Response" "$REVIEW_CREATE_RESPONSE"
    REVIEW_ID=$(extract_id "$REVIEW_CREATE_RESPONSE")
    echo "Review ID: $REVIEW_ID"

    if [ ! -z "$REVIEW_ID" ]; then
        echo "4.2 Testing invalid review data..."
        INVALID_REVIEW_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/reviews/ \
          -H "Content-Type: application/json" \
          -d '{
            "text": "Invalid rating",
            "rating": 6,
            "user_id": "'$USER_ID'",
            "place_id": "'$PLACE_ID'"
        }')
        show_response "Invalid Review Response" "$INVALID_REVIEW_RESPONSE"

        echo "4.3 Getting reviews for place..."
        PLACE_REVIEWS_RESPONSE=$(curl -s -X GET "http://localhost:5000/api/v1/reviews/places/$PLACE_ID/reviews")
        show_response "Place Reviews" "$PLACE_REVIEWS_RESPONSE"

        echo "4.4 Deleting review..."
        DELETE_RESPONSE=$(curl -s -X DELETE "http://localhost:5000/api/v1/reviews/$REVIEW_ID")
        show_response "Delete Review Response" "$DELETE_RESPONSE"
    fi
fi

# Test Summary
echo -e "\n======================================"
echo "Test Summary"
echo "======================================"
echo "User ID: $USER_ID"
echo "Place ID: $PLACE_ID"
echo "Amenity ID: $AMENITY_ID"
echo "Review ID: $REVIEW_ID"
echo "Testing Complete"