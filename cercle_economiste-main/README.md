
1) Créer et activer un environnement virtuel**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```
2) Base de données

```sql
CREATE DATABASE association_cabro_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3) Appliquer les migrations & créer un superuser**

python manage.py migrate
python manage.py createsuperuser

4) Lancer le serveur de développement**

python manage.py runserver 0.0.0.0:8000

ACCES:
- Frontend: http://localhost:8000/
- Admin Django: http://localhost:8000/admin/

