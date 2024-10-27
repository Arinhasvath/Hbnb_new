#!/bin/bash

# Fonctions utilitaires
show_response() {
    local title="$1"
    local response="$2"
    echo -e "\n=== $title ==="
    echo "$response"
    echo "===================="
}

extract_id() {
    local json="$1"
    echo "$json" | python3 -c "import sys, json; print(json.loads(sys.stdin.read()).get('id', ''))"
}

# Variables globales pour stocker les IDs
USER_ID=""
PLACE_ID=""
AMENITY_ID=""
REVIEW_ID=""

echo "======================================"
echo "Starting HBnB API Integration Tests..."
echo "======================================"

# 1. TESTS USER
echo -e "\n=== 1. USER TESTS ==="

echo "1.1 Testing User Creation..."
# Créer un utilisateur valide
USER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test'$(date +%s)'@example.com"
}')
show_response "Create Valid User" "$USER_RESPONSE"
USER_ID=$(extract_id "$USER_RESPONSE")

# Test email déjà utilisé
echo "Testing duplicate email..."
curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "'$(echo $USER_RESPONSE | jq -r .email)'"
}'

# Test données invalides
echo "Testing invalid data..."
curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "",
    "email": "invalid-email"
}'

echo "1.2 Testing User Retrieval..."
# Get all users
curl -s -X GET http://localhost:5000/api/v1/users/

# Get specific user
curl -s -X GET "http://localhost:5000/api/v1/users/$USER_ID"

# 2. TESTS PLACE
echo -e "\n=== 2. PLACE TESTS ==="

echo "2.1 Testing Place Creation..."
# Créer un place valide
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
show_response "Create Valid Place" "$PLACE_RESPONSE"
PLACE_ID=$(extract_id "$PLACE_RESPONSE")

# Test coordonnées invalides
echo "Testing invalid coordinates..."
curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Invalid Place",
    "description": "Test",
    "price": 100,
    "latitude": 100,
    "longitude": -200,
    "owner_id": "'$USER_ID'"
}'

# 3. TESTS AMENITY
echo -e "\n=== 3. AMENITY TESTS ==="

echo "3.1 Testing Amenity Creation..."
# Créer un amenity valide
AMENITY_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WiFi"
}')
show_response "Create Valid Amenity" "$AMENITY_RESPONSE"
AMENITY_ID=$(extract_id "$AMENITY_RESPONSE")

# Test nom vide
curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'

# 4. TESTS REVIEW
echo -e "\n=== 4. REVIEW TESTS ==="

echo "4.1 Testing Review Creation..."
# Créer une review valide
REVIEW_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "user_id": "'$USER_ID'",
    "place_id": "'$PLACE_ID'"
}')
show_response "Create Valid Review" "$REVIEW_RESPONSE"
REVIEW_ID=$(extract_id "$REVIEW_RESPONSE")

# Test rating invalide
echo "Testing invalid rating..."
curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Invalid rating",
    "rating": 6,
    "user_id": "'$USER_ID'",
    "place_id": "'$PLACE_ID'"
}'

# Test suppression review
echo "4.2 Testing Review Deletion..."
curl -s -X DELETE "http://localhost:5000/api/v1/reviews/$REVIEW_ID"

# Vérifier reviews par place
echo "4.3 Testing Place Reviews..."
curl -s -X GET "http://localhost:5000/api/v1/reviews/places/$PLACE_ID/reviews"

echo -e "\n======================================"
echo "Testing Complete"
echo "======================================"