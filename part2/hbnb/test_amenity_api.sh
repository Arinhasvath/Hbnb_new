#!/bin/bash

echo "=== Testing Amenity API ==="

# Variables pour stocker les réponses
AMENITY_ID=""

# Fonction pour afficher les réponses avec un titre
show_response() {
    local title=$1
    local response=$2
    echo -e "\n=== $title ==="
    echo "$response"
    echo "===================="
}

# 1. Création d'un amenity
echo -e "\nTest 1: Creating amenity"
RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}')
show_response "CREATE RESPONSE" "$RESPONSE"
AMENITY_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created Amenity ID: $AMENITY_ID"

# 2. Récupération de l'amenity créé
echo -e "\nTest 2: Getting created amenity"
RESPONSE=$(curl -s -X GET "http://localhost:5000/api/v1/amenities/$AMENITY_ID")
show_response "GET SPECIFIC RESPONSE" "$RESPONSE"

# 3. Mise à jour de l'amenity
echo -e "\nTest 3: Updating amenity"
RESPONSE=$(curl -s -X PUT "http://localhost:5000/api/v1/amenities/$AMENITY_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "High-Speed WiFi"}')
show_response "UPDATE RESPONSE" "$RESPONSE"

# 4. Liste de tous les amenities
echo -e "\nTest 4: Getting all amenities"
RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/amenities/)
show_response "GET ALL RESPONSE" "$RESPONSE"

# 5. Test de validation - nom vide
echo -e "\nTest 5: Testing validation (empty name)"
RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}')
show_response "VALIDATION ERROR RESPONSE" "$RESPONSE"

# 6. Test avec ID invalide
echo -e "\nTest 6: Testing invalid ID"
RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/amenities/invalid-id)
show_response "INVALID ID RESPONSE" "$RESPONSE"

# 7. Test de mise à jour avec ID invalide
echo -e "\nTest 7: Testing update with invalid ID"
RESPONSE=$(curl -s -X PUT "http://localhost:5000/api/v1/amenities/invalid-id" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}')
show_response "INVALID UPDATE RESPONSE" "$RESPONSE"

echo -e "\nTests completed."