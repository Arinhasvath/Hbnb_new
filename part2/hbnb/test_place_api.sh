#!/bin/bash

echo "=== Testing Place API ==="

# Fonction pour afficher les réponses formatées
show_response() {
    local title=$1
    local response=$2
    echo -e "\n=== $title ==="
    echo "$response"
    echo "===================="
}

# 1. Créer un utilisateur pour être propriétaire
echo -e "\n1. Creating owner..."
OWNER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Owner",
    "email": "owner@test.com"
}')
show_response "Owner Creation Response" "$OWNER_RESPONSE"
OWNER_ID=$(echo "$OWNER_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Owner ID: $OWNER_ID"

# 2. Créer un amenity
echo -e "\n2. Creating amenity..."
AMENITY_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WiFi"
}')
show_response "Amenity Creation Response" "$AMENITY_RESPONSE"
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Amenity ID: $AMENITY_ID"

# 3. Test Place endpoints
echo -e "\n3. Testing Place endpoints..."

# 3.1 Create Place
echo "3.1. Creating place..."
CREATE_PLACE_PAYLOAD=$(cat <<EOF
{
    "title": "Test Place",
    "description": "A test place",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "$OWNER_ID",
    "amenity_ids": ["$AMENITY_ID"]
}
EOF
)
echo "Request payload:"
echo "$CREATE_PLACE_PAYLOAD"

PLACE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "$CREATE_PLACE_PAYLOAD")
show_response "Place Creation Response" "$PLACE_RESPONSE"
PLACE_ID=$(echo "$PLACE_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Place ID: $PLACE_ID"

# 3.2 Get All Places
echo -e "\n3.2. Getting all places..."
LIST_RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/places/)
show_response "List Places Response" "$LIST_RESPONSE"

# 3.3 Get Specific Place (seulement si nous avons un ID)
if [ ! -z "$PLACE_ID" ]; then
    echo -e "\n3.3. Getting specific place..."
    GET_RESPONSE=$(curl -s -X GET "http://localhost:5000/api/v1/places/$PLACE_ID")
    show_response "Get Place Response" "$GET_RESPONSE"

    # 3.4 Update Place
    echo -e "\n3.4. Updating place..."
    UPDATE_RESPONSE=$(curl -s -X PUT "http://localhost:5000/api/v1/places/$PLACE_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "title": "Updated Place",
        "price": 150.0
    }')
    show_response "Update Place Response" "$UPDATE_RESPONSE"
fi

echo -e "\nTests completed."