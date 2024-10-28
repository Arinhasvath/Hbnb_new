#!/bin/bash

# Couleurs pour meilleure lisibilité
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variables globales
BASE_URL="http://localhost:5000/api/v1"
TIMESTAMP=$(date +%s)
EMAIL="test$TIMESTAMP@example.com"

# Compteurs de tests
PASSED=0
FAILED=0

# Fonction pour les tests
test_endpoint() {
    local description="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local expected_code="$5"

    echo -e "\nTest: $description"
    
    RESPONSE=$(curl -s -w "\n%{http_code}" -X $method \
        -H "Content-Type: application/json" \
        ${data:+-d "$data"} \
        "$BASE_URL/$endpoint")
    
    STATUS=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n1)

    if [ "$STATUS" -eq "$expected_code" ]; then
        echo -e "${GREEN}✓ Success ($STATUS)${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Failed (Expected: $expected_code, Got: $STATUS)${NC}"
        ((FAILED++))
    fi
    
    echo "Response: $BODY"
    echo "$RESPONSE"
}

# 1. USER TESTS
echo -e "\n${BLUE}=== USER TESTS ===${NC}"

# 1.1 Création utilisateur valide
echo -e "\nTesting User Creation"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d "{
        \"first_name\": \"Test\",
        \"last_name\": \"User\",
        \"email\": \"$EMAIL\"
    }")
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$USER_ID" ]; then
    echo -e "${RED}Failed to get User ID. Cannot continue tests.${NC}"
    exit 1
fi

# 1.2 Test email dupliqué
test_endpoint \
    "Create user with duplicate email" \
    "POST" \
    "users" \
    "{
        \"first_name\": \"Test2\",
        \"last_name\": \"User2\",
        \"email\": \"$EMAIL\"
    }" \
    400

# 1.3 Test données invalides
test_endpoint \
    "Create user with invalid data" \
    "POST" \
    "users" \
    '{
        "first_name": "",
        "email": "invalid-email"
    }' \
    400

# 1.4 Test GET user
test_endpoint \
    "Get specific user" \
    "GET" \
    "users/$USER_ID" \
    "" \
    200

# 1.5 Test GET user inexistant
test_endpoint \
    "Get non-existent user" \
    "GET" \
    "users/invalid-id" \
    "" \
    404

# 2. PLACE TESTS
echo -e "\n${BLUE}=== PLACE TESTS ===${NC}"

# 2.1 Création place valide
PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places" \
    -H "Content-Type: application/json" \
    -d "{
        \"title\": \"Test Place\",
        \"description\": \"A test place\",
        \"price\": 100.0,
        \"latitude\": 40.7128,
        \"longitude\": -74.0060,
        \"owner_id\": \"$USER_ID\"
    }")
PLACE_ID=$(echo "$PLACE_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

# 2.2 Test prix négatif
test_endpoint \
    "Create place with negative price" \
    "POST" \
    "places" \
    "{
        \"title\": \"Invalid Place\",
        \"description\": \"Test place\",
        \"price\": -100,
        \"latitude\": 40.7128,
        \"longitude\": -74.0060,
        \"owner_id\": \"$USER_ID\"
    }" \
    400

# Continuer avec tous les tests requis...

# Afficher le résumé des tests
echo -e "\n${BLUE}=== Test Summary ===${NC}"
echo -e "Tests passed: ${GREEN}$PASSED${NC}"
echo -e "Tests failed: ${RED}$FAILED${NC}"
echo -e "Total tests: $((PASSED + FAILED))"
# Suite du script précédent...

# 2.3 Test latitude invalide (>90)
test_endpoint \
   "Create place with invalid latitude >90" \
   "POST" \
   "places" \
   "{
       \"title\": \"Invalid Place\",
       \"description\": \"Test place\",
       \"price\": 100,
       \"latitude\": 91,
       \"longitude\": -74.0060,
       \"owner_id\": \"$USER_ID\"
   }" \
   400

# 2.4 Test latitude invalide (<-90)
test_endpoint \
   "Create place with invalid latitude <-90" \
   "POST" \
   "places" \
   "{
       \"title\": \"Invalid Place\",
       \"description\": \"Test place\",
       \"price\": 100,
       \"latitude\": -91,
       \"longitude\": -74.0060,
       \"owner_id\": \"$USER_ID\"
   }" \
   400

# 2.5 Test longitude invalide (>180)
test_endpoint \
   "Create place with invalid longitude >180" \
   "POST" \
   "places" \
   "{
       \"title\": \"Invalid Place\",
       \"description\": \"Test place\",
       \"price\": 100,
       \"latitude\": 40.7128,
       \"longitude\": 181,
       \"owner_id\": \"$USER_ID\"
   }" \
   400

# 2.6 Test longitude invalide (<-180)
test_endpoint \
   "Create place with invalid longitude <-180" \
   "POST" \
   "places" \
   "{
       \"title\": \"Invalid Place\",
       \"description\": \"Test place\",
       \"price\": 100,
       \"latitude\": 40.7128,
       \"longitude\": -181,
       \"owner_id\": \"$USER_ID\"
   }" \
   400

# 2.7 Test owner inexistant
test_endpoint \
   "Create place with non-existent owner" \
   "POST" \
   "places" \
   "{
       \"title\": \"Invalid Place\",
       \"description\": \"Test place\",
       \"price\": 100,
       \"latitude\": 40.7128,
       \"longitude\": -74.0060,
       \"owner_id\": \"invalid-owner-id\"
   }" \
   400

# 3. AMENITY TESTS
echo -e "\n${BLUE}=== AMENITY TESTS ===${NC}"

# 3.1 Création amenity valide
AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities" \
   -H "Content-Type: application/json" \
   -d '{
       "name": "WiFi"
   }')
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

# 3.2 Test nom vide
test_endpoint \
   "Create amenity with empty name" \
   "POST" \
   "amenities" \
   '{
       "name": ""
   }' \
   400

# 3.3 Test GET amenity
test_endpoint \
   "Get specific amenity" \
   "GET" \
   "amenities/$AMENITY_ID" \
   "" \
   200

# 3.4 Test GET amenity inexistant
test_endpoint \
   "Get non-existent amenity" \
   "GET" \
   "amenities/invalid-id" \
   "" \
   404

# 4. REVIEW TESTS
echo -e "\n${BLUE}=== REVIEW TESTS ===${NC}"

# 4.1 Création review valide
REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews" \
   -H "Content-Type: application/json" \
   -d "{
       \"text\": \"Great place!\",
       \"rating\": 5,
       \"user_id\": \"$USER_ID\",
       \"place_id\": \"$PLACE_ID\"
   }")
REVIEW_ID=$(echo "$REVIEW_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

# 4.2 Test rating invalide (<1)
test_endpoint \
   "Create review with rating <1" \
   "POST" \
   "reviews" \
   "{
       \"text\": \"Invalid rating\",
       \"rating\": 0,
       \"user_id\": \"$USER_ID\",
       \"place_id\": \"$PLACE_ID\"
   }" \
   400

# 4.3 Test rating invalide (>5)
test_endpoint \
   "Create review with rating >5" \
   "POST" \
   "reviews" \
   "{
       \"text\": \"Invalid rating\",
       \"rating\": 6,
       \"user_id\": \"$USER_ID\",
       \"place_id\": \"$PLACE_ID\"
   }" \
   400

# 4.4 Test texte vide
test_endpoint \
   "Create review with empty text" \
   "POST" \
   "reviews" \
   "{
       \"text\": \"\",
       \"rating\": 4,
       \"user_id\": \"$USER_ID\",
       \"place_id\": \"$PLACE_ID\"
   }" \
   400

# 4.5 Test user inexistant
test_endpoint \
   "Create review with non-existent user" \
   "POST" \
   "reviews" \
   "{
       \"text\": \"Great place!\",
       \"rating\": 5,
       \"user_id\": \"invalid-user-id\",
       \"place_id\": \"$PLACE_ID\"
   }" \
   400

# 4.6 Test place inexistant
test_endpoint \
   "Create review with non-existent place" \
   "POST" \
   "reviews" \
   "{
       \"text\": \"Great place!\",
       \"rating\": 5,
       \"user_id\": \"$USER_ID\",
       \"place_id\": \"invalid-place-id\"
   }" \
   400

# 4.7 Test GET reviews par place
test_endpoint \
   "Get reviews by place" \
   "GET" \
   "reviews/places/$PLACE_ID/reviews" \
   "" \
   200

# 4.8 Test UPDATE review
test_endpoint \
   "Update review" \
   "PUT" \
   "reviews/$REVIEW_ID" \
   "{
       \"text\": \"Updated review\",
       \"rating\": 4
   }" \
   200

# 4.9 Test DELETE review
test_endpoint \
   "Delete review" \
   "DELETE" \
   "reviews/$REVIEW_ID" \
   "" \
   200

# 4.10 Vérifier que la review est supprimée
test_endpoint \
   "Get deleted review" \
   "GET" \
   "reviews/$REVIEW_ID" \
   "" \
   404

# Afficher résumé final détaillé
echo -e "\n${BLUE}=== Test Summary ===${NC}"
echo -e "Tests passed: ${GREEN}$PASSED${NC}"
echo -e "Tests failed: ${RED}$FAILED${NC}"
echo -e "Total tests: $((PASSED + FAILED))"

echo -e "\n${BLUE}=== Test IDs ===${NC}"
echo "User ID: $USER_ID"
echo "Place ID: $PLACE_ID"
echo "Amenity ID: $AMENITY_ID"
echo "Review ID: $REVIEW_ID"