#!/bin/bash

echo "=== Testing Place API ==="

# Function to prettify and show responses
show_response() {
    local title="$1"
    local response="$2"
    echo -e "\n=== $title ==="
    echo "$response"
    echo "===================="
}

TIMESTAMP=$(date +%s)
EMAIL="test$TIMESTAMP@example.com"

# 1. Create User
echo -e "\n1. Creating user..."
USER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Test\",
    \"last_name\": \"Owner\",
    \"email\": \"$EMAIL\"
}")
show_response "User Creation" "$USER_RESPONSE"
USER_ID=$(echo "$USER_RESPONSE" | tr ',' '\n' | grep '"id"' | cut -d':' -f2 | tr -d '"' | tr -d ' ')

# 2. Test Valid Place Creation
echo -e "\n2. Testing valid place creation..."
PLACE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Place\",
    \"description\": \"A test place\",
    \"price\": 100,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\"
}")
show_response "Valid Place Creation" "$PLACE_RESPONSE"
PLACE_ID=$(echo "$PLACE_RESPONSE" | tr ',' '\n' | grep '"id"' | cut -d':' -f2 | tr -d '"' | tr -d ' ')

# 3. Test Invalid Cases
echo -e "\n3. Testing validation cases..."

echo -e "\n3.1 Testing negative price..."
INVALID_PRICE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Invalid Place\",
    \"description\": \"Test place\",
    \"price\": -100,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\"
}")
show_response "Negative Price Test" "$INVALID_PRICE_RESPONSE"

echo -e "\n3.2 Testing invalid coordinates..."
INVALID_COORDS_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Invalid Place\",
    \"description\": \"Test place\",
    \"price\": 100,
    \"latitude\": 100,
    \"longitude\": -200,
    \"owner_id\": \"$USER_ID\"
}")
show_response "Invalid Coordinates Test" "$INVALID_COORDS_RESPONSE"

echo -e "\n3.3 Testing missing fields..."
MISSING_FIELDS_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Invalid Place\"
}")
show_response "Missing Fields Test" "$MISSING_FIELDS_RESPONSE"

# 4. Test Update
if [ ! -z "$PLACE_ID" ]; then
    echo -e "\n4. Testing place update..."
    UPDATE_RESPONSE=$(curl -s -X PUT "http://localhost:5000/api/v1/places/$PLACE_ID" \
      -H "Content-Type: application/json" \
      -d "{
        \"title\": \"Updated Place\",
        \"price\": 150.0
    }")
    show_response "Place Update" "$UPDATE_RESPONSE"
    
    # Verify update
    VERIFY_UPDATE=$(curl -s -X GET "http://localhost:5000/api/v1/places/$PLACE_ID")
    show_response "Verify Update" "$VERIFY_UPDATE"
fi

echo -e "\nTests completed."