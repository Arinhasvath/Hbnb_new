# Hbnb_new

Pour tester localement ton projet **Hbnb_new** (un backend Flask avec une API de gestion des utilisateurs, des lieux, des avis, etc.), voici un guide détaillé pour réaliser les tests, avec des commandes `cURL`, ainsi que des tests unitaires pour vérifier la stabilité de tes endpoints. Ces tests incluent la création d'utilisateurs, de lieux, d'avis, et la gestion des erreurs.

### 1. **Tests avec cURL**

Voici les différentes commandes `cURL` pour tester les principales fonctionnalités de ton API en local.

#### Créer un utilisateur

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
}'
```

- **Réponse attendue :**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
// Statut : 201 Created
```

#### Créer un utilisateur avec des données invalides

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email",
    "password": ""
}'
```

- **Réponse attendue :**
```json
{
  "error": "Invalid input data"
}
// Statut : 400 Bad Request
```

#### Lister les utilisateurs

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json"
```

- **Réponse attendue :**
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }
]
// Statut : 200 OK
```

#### Créer un lieu (Place)

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
    "title": "Beautiful Apartment",
    "price": 100,
    "latitude": 48.8566,
    "longitude": 2.3522
}'
```

- **Réponse attendue :**
```json
{
  "id": "abcd1234",
  "title": "Beautiful Apartment",
  "price": 100,
  "latitude": 48.8566,
  "longitude": 2.3522
}
// Statut : 201 Created
```

#### Créer un lieu avec des données invalides

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
    "title": "",
    "price": -10,
    "latitude": 200,
    "longitude": -300
}'
```

- **Réponse attendue :**
```json
{
  "error": "Invalid input data"
}
// Statut : 400 Bad Request
```

#### Créer un avis (Review)

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
    "text": "Great place!",
    "user_id": "abcd1234",
    "place_id": "abcd5678"
}'
```

- **Réponse attendue :**
```json
{
  "id": "efgh5678",
  "text": "Great place!",
  "user_id": "abcd1234",
  "place_id": "abcd5678"
}
// Statut : 201 Created
```

### 2. **Tests unitaires avec `unittest`**

Tu peux automatiser ces tests avec `unittest` en créant des tests unitaires pour chaque endpoint de ton API. Voici un exemple de tests unitaires pour les utilisateurs.

#### Créer un fichier de test `test_users.py` :

```python
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "securepassword"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "short"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
```

#### Créer un fichier de test `test_places.py` :

```python
import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful House",
            "price": 150,
            "latitude": 40.7128,
            "longitude": -74.0060
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -20,
            "latitude": 200,
            "longitude": -300
        })
        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
```

### 3. **Lancer les tests avec `unittest`**

Pour exécuter les tests unitaires en local, tu peux utiliser la commande suivante dans le répertoire contenant tes fichiers de tests :

```bash
python -m unittest discover -s tests
```

Cela va exécuter tous les tests présents dans le dossier `tests/` et te donner un rapport sur la réussite ou l’échec des différents tests.

### 4. **Vérification de la stabilité**

Pour vérifier la **stabilité** de ton API en local, tu peux combiner les tests manuels (avec `cURL`), les tests unitaires, ainsi que des tests de charge (Load Testing) et de stress.

#### Exemple d'outil pour le **test de charge** :

- **Apache JMeter** ou **Locust** sont recommandés pour tester la stabilité de ton application sous une charge importante.
  
- Exemple avec **Locust** (comme mentionné précédemment) :
  - Lancer Locust pour tester un grand nombre d’utilisateurs accédant à ton API.

Cela t'aidera à voir comment ton API réagit en cas de forte utilisation, tout en identifiant les éventuels points de défaillance.

---

Pour effectuer des tests complets et approfondis de ton projet **HBNB** en local, notamment pour valider la création d'utilisateurs, la gestion des entités comme les lieux (`Place`), les avis (`Review`), les commodités (`Amenity`), ainsi que les différentes relations entre elles, tu peux suivre ces étapes. Je vais également te fournir les commandes appropriées pour chaque type de test, ainsi que des explications sur la stabilité et les vérifications nécessaires.

### 1. **Configurer l’environnement de test local**

Avant de commencer à tester, assure-toi d'avoir configuré correctement ton environnement local.

#### a. **Démarrage de l'application**
Lance ton application Flask en mode développement pour qu'elle soit accessible en local.

```bash
flask run
```

Cela va démarrer ton application sur `http://127.0.0.1:5000/`.

#### b. **Vérifier la base de données**
Assure-toi que ta base de données locale est configurée et migrée avec les bons schémas.

```bash
flask db upgrade
```

Si tu utilises une base MySQL ou SQLite, vérifie que tout est en place avec les commandes SQL correspondantes.

### 2. **Tests de création des utilisateurs**

#### a. **Commande cURL pour créer un utilisateur**

Voici comment tu peux créer un utilisateur avec cURL :

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "123456"
}'
```

**Attendu :** 
Un utilisateur est créé avec les informations fournies et un code **201 Created** est retourné.

**Réponse attendue :**
```json
{
    "id": "unique-user-id",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "created_at": "2024-10-22T12:34:56.789Z",
    "updated_at": "2024-10-22T12:34:56.789Z"
}
```

#### b. **Test de validation des données d'utilisateur (email invalide)**

Test pour vérifier si les emails invalides sont correctement rejetés.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "invalid-email",
    "password": "password123"
}'
```

**Attendu :** 
Le serveur doit retourner une réponse **400 Bad Request** avec un message d'erreur expliquant que l'email est invalide.

**Réponse attendue :**
```json
{
    "error": "Invalid email format"
}
```

### 3. **Tests de création de lieux (Places)**

#### a. **Création d’un lieu avec cURL**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Maison de campagne",
    "price": 150,
    "latitude": 48.8566,
    "longitude": 2.3522
}'
```

**Attendu :** 
Un lieu est créé avec succès et un code **201 Created** est retourné.

**Réponse attendue :**
```json
{
    "id": "unique-place-id",
    "title": "Maison de campagne",
    "price": 150,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "created_at": "2024-10-22T12:34:56.789Z",
    "updated_at": "2024-10-22T12:34:56.789Z"
}
```

#### b. **Validation des coordonnées (lat/long)**

Teste les limites géographiques pour t'assurer que les coordonnées sont valides.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Invalid Place",
    "price": 200,
    "latitude": 150,
    "longitude": -250
}'
```

**Attendu :** 
Le serveur retourne un code **400 Bad Request** et un message d'erreur signalant que les coordonnées ne sont pas valides.

**Réponse attendue :**
```json
{
    "error": "Latitude must be between -90 and 90, and longitude must be between -180 and 180"
}
```

### 4. **Tests des avis (Reviews)**

#### a. **Création d’un avis pour un lieu**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "user_id": "valid-user-id",
    "place_id": "valid-place-id",
    "text": "Great place to stay!"
}'
```

**Attendu :**
L'avis est créé avec succès et un code **201 Created** est retourné.

**Réponse attendue :**
```json
{
    "id": "unique-review-id",
    "user_id": "valid-user-id",
    "place_id": "valid-place-id",
    "text": "Great place to stay!",
    "created_at": "2024-10-22T12:34:56.789Z",
    "updated_at": "2024-10-22T12:34:56.789Z"
}
```

#### b. **Test de la validation de l'avis (texte vide)**

Teste l'envoi d'un avis sans texte.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "user_id": "valid-user-id",
    "place_id": "valid-place-id",
    "text": ""
}'
```

**Attendu :** 
Le serveur doit retourner un code **400 Bad Request** avec un message d'erreur expliquant que le texte de l'avis ne peut pas être vide.

**Réponse attendue :**
```json
{
    "error": "Review text cannot be empty"
}
```

### 5. **Tests des commodités (Amenity)**

#### a. **Création d’une commodité**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{
    "name": "Wi-Fi"
}'
```

**Attendu :**
La commodité est créée avec succès et un code **201 Created** est retourné.

**Réponse attendue :**
```json
{
    "id": "unique-amenity-id",
    "name": "Wi-Fi",
    "created_at": "2024-10-22T12:34:56.789Z",
    "updated_at": "2024-10-22T12:34:56.789Z"
}
```

### 6. **Tests de performance et de stabilité**

Une fois que tu as validé les tests fonctionnels, il est important de tester la **stabilité** de ton application sous charge en local.

#### a. **Test de charge avec Apache JMeter ou Locust**

Comme décrit précédemment, tu peux utiliser des outils comme **Locust** ou **JMeter** pour simuler plusieurs utilisateurs accédant à tes endpoints. Voici un exemple pour Locust :

1. Installe Locust : `pip install locust`
2. Crée un fichier `locustfile.py` pour tester la création des utilisateurs :

    ```python
    from locust import HttpUser, TaskSet, task

    class UserBehavior(TaskSet):
        @task
        def create_user(self):
            self.client.post("/api/v1/users/", json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "123456"
            })

    class WebsiteUser(HttpUser):
        tasks = [UserBehavior]
        min_wait = 5000
        max_wait = 9000
    ```

3. Lance Locust : `locust -f locustfile.py`
4. Ouvre `http://localhost:8089` dans un navigateur pour démarrer le test de charge.

Cela permet de vérifier la stabilité et la capacité à gérer plusieurs utilisateurs simultanés en local.

### Conclusion

Ces tests couvrent les principales fonctionnalités du projet **HBNB** en local. Ils permettent de vérifier la création des utilisateurs, des lieux, des avis, ainsi que la gestion des commodités. Les tests de charge et de validation garantissent la stabilité de ton application en environnement local avant un déploiement en production.
