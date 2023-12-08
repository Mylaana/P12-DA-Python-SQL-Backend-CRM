# CRM EpicEvents

## Initialisation

Suivez ces étapes pour configurer et lancer l'outil CRM sur votre machine locale.

### Prérequis

Assurez-vous d'avoir installé les outils suivants sur votre machine :
- Python (version recommandée : 3.11 ou ultérieure)
- Pip (installé avec Python)
- MySQL (version recommandée : 8.0 ou ultérieure)

### Installation des dépendances

1. Clonez le dépôt sur votre machine locale :
    ```bash
    git clone https://github.com/Mylaana/P12-DA-Python-SQL-Backend-CRM.git
    cd repertoire/projet/
    ```

2. Créez un environnement virtuel :
    ```bash
    python -m venv myenv
    ```

3. Activez l'environnement virtuel :
   
    Sur macOS et Linux :
    ```
    source myenv/bin/activate
    ```
      
    Sur Windows (PowerShell) :
    ```
    .\myenv\Scripts\Activate.ps1
    ```

4. Installez les dépendances Python :
    ```bash
    pip install -r requirements.txt
    ```

### Configuration et migration de la base de données

1. Créez une base de données MySQL vide pour l'application CRM.

2. Copiez le fichier `db_config_example.ini` et renommez-le en `db_config.ini`. Modifiez les paramètres de base de données dans ce fichier en fonction des paramètres de votre base de donnée MySql :

    ```dotenv
    # db_config_example.ini
    [mysql]
    database = database_name
    user = database_root_username
    password = database_password
    ```

3. Après avoir configuré le fichier `db_config.ini`, vous pouvez maintenant migrer la base de données en appliquant les migrations :
    ```bash
    python manage.py migrate
    ```

Ces étapes garantissent que votre application CRM utilise la base de données MySQL.

### Utilisation du CRM
1. Lancez l'application CRM avec la commande suivante :

```bash
python manage.py runserver
```
L'outil CRM sera accessible à l'adresse http://localhost:8000.

2. Liste des commandes de l'application :
