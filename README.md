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

2. Dans le répertoire nommé 'EpicEvents', copiez le fichier `db_config_example.ini` et renommez-le en `db_config.ini`. Modifiez les paramètres de base de données dans ce fichier en fonction des paramètres de votre base de donnée MySql :

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

    Ces étapes garantissent que l'application CRM utilise la base de données MySQL.

### Initialisation de Sentry
1. Créez un nouveau projet Sentry et sélectionnez Django: www.sentry.io
2. Dans la section 'Configure SDK' vous devriez voir une sous section comme suit :
    ```dotenv
    # settings.py
    import sentry_sdk
    
    sentry_sdk.init(
        dsn="https://code_a_copier.ingest.sentry.io/code_a_copier",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
    ```

copiez le lien http de la ligne 'dsn="https://..."'

3. Dans le répertoire EpicEvents du projet, retournez dans le fichier `db_config.ini`, et collez ce lien dans la section : 
    ```dotenv
    # db_config.ini
    [sentry]
    sentry_link = https://sentry_link_here.com.123456789
    ```

### Utilisation du CRM
1. Créez un compte administrateur:
    ```bash
    python manage.py createsuperuser
    ```
2. Lancez l'application CRM avec la commande suivante :

    ```bash
    python manage.py runserver
    ```
    L'outil CRM sera accessible à l'adresse http://localhost:8000.

3. Créez les équipes:  
   L'application étant concue pour fonctionner avec 3 équipes de base, veuillez vous authentifier en tant que superuser puis utiliser la commande suivante :
   ```bash
    python manage.py team -create
    ```
    Créez ainsi trois équipes : 'commerciale', 'support', 'gestion'.
    Notez qu'il est possible d'utiliser d'autres noms d'équipe à condition de modifier les permissions d'accès dans le fichier EpicEvents/'permissions.py'.


3. Liste des commandes de l'application :
    Toutes les commandes doivent être précédées de 'python manage.py ':  
    Authentification :
   ```bash
   login # permet de s'authentifier dans la base de données.
   logout # permet de se déconnecter.
   ```
    
    Une fois authentifié, vous pouvez appeler les menus suivants :
    ```bash
    user # permettra d'intéragir avec les données liées aux utilisateurs.
    team # permettra d'intéragir avec les données liées aux équipes.
    client # permettra d'intéragir avec les données liées aux clients.
    contract # permettra d'intéragir avec les données liées aux contrats.
    event # permettra d'intéragir avec les données liées aux événements.
    ```
    Chaque menu doit être accompagné d'une opération :
    ```bash
    -list # listera tous les éléments correspondant au menu
    -read # le CRM demandera le nom de l'élément à lire et affichera ensuite ses informations.
    -create # le CRM demandera les informations clés de l'objet à créér puis l'ajoutera à la base de données.
    -update # le CRM demandera le nom de l'élément à mettre à jour puis demandera à l'utilisateur quel(s) champ(s) mettre à jour.
    -delete # le CRM demandera le nom de l'élément à supprimer puis le retirera de la base de données.
    ```
    
    Options supplémentaires :
    ```bash
    client -list -own # affichera uniquement les clients attribués à l'utilisateur actif.
    contract -list -own # affichera uniquement les cotnrats attribués à l'utilisateur actif.
    event -list -own # affichera uniquement les événements attribués à l'utilisateur actif.
    event -list -no-owner # affichera uniquement les événements qui ne sont attribués à personne.
    ```
    
    Exemple d'utilisation :
    ```bash
    python manage.py client -create # permettra de créer un client.
    python manage.py event -list # permettra d'afficher les événements.
    python manage.py event -list -no-owner # permettra d'afficher les événements non attribués uniquement.
    ```
