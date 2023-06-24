DESCRIPTION :

API permettant de remonter et suivre des problèmes techniques (issue tracking system).

_______________________________________________________________________________

TECHNOLOGIES : 
interpréteur : Python 3.0+
frameworks : django 4.2.2+, django rest framekwork 3.14.0+
(veuillez vérifier requirements.txt pour plus d'informations)

_______________________________________________________________________________

AUTHOR:
développeur : Nicolas Deleu
société : Softdesk

_______________________________________________________________________________
_______________________________________________________________________________

ENVIRONNEMENT :

    Mise en place de l'environnement de travail :

* Dans votre terminal, accédez au dossier projet_10_OC : Saisissez dans votre terminal : `cd nom_du_chemin_d_acces`. 
Si vous recherchez le path de ce chemin, allez dans le dossier projet_10_OC, et dans la barre de recherche du dossier, située en haut du dossier, faites un clic gauche pour sélectionner le chemin, puis un clic droit pour copier coller ce chemin.

* Dans votre terminal, créez un environnement virtuel pour Python, par convention nous appelerons cet environnement : env

Sous Microsoft Windows : `python -m venv env`.

Sous Linux et Mac : `python3 -m venv env`.

* Connectez vous à cet environnement virtuel :

Sur un terminal Windows powershell : `env/Scripts/Activate.ps1`

Sur un terminal Windows invite de commande : `env/Scripts/activate.bat`

Sur un terminal Linux ou Mac : `source env/bin/activate`

* Vérifiez que vous êtes bien connecté à votre environnement virtuel, au début de la ligne du terminal doit apparaître : (env) Si vous désirez vous déconnecter de votre environnement virtuel, saisissez la commande : `deactivate`

* Installez dans votre environnement virtuel les modules attendus pour le bon fonctionnement du script de l'application web : Une fois connecté à votre environnement virtuel saisissez dans votre terminal la commande : `pip install -r requirements.txt` Votre environnement de travail est maintenant initialisé et prêt a pouvoir lancer l'API. Nous allons découvrir comment y parvenir dans le prochain point. Pour toute problématique de lancement lié à l'installation de Python ou des Path liés à Microsoft, Mac ou Linux, Merci de vous référer directement au site officiel de Python : https://www.python.org/downloads/

_______________________________________________________________________________

    Démarrage du serveur :

* Afin de lancer le serveur, accèdez au dossier contenant le fichier python "manage.py". Pour cela, à partir de la position que vous aviez pour initialiser votre environnement de travail, Saisissez dans votre terminal : `cd ITSys`

* Vous pouvez maintenant lancer le serveur en saisissant dans votre terminal :

Sur Microsoft Windows : `python manage.py runserver`

Sur Linux ou Mac : `python3 manage.py runserver`

_______________________________________________________________________________
_______________________________________________________________________________

INFORMATIONS SUR LES ENDPOINTS :

    avant propos :

`{int:obj}` est une variable que nous n'utiliserons que pour ce README.md. Il nous permettra de comprendre et de nous représenter les urls pour accéder aux Endpoints. int correspond à l'id assigné à l'objet, obj correspond quand à lui à l'objet. L'objet peut être un `project`, ou un `user`, ou un `issue`, ou un `comment`. Ainsi, sous forme abstraite, il est représenté ainsi : `http://127.0.0.1:8000/api/projects/{int:obj}`, dans notre exemplification nous le représenterons ainsi : `http://127.0.0.1:8000/api/projects/{int:project}`, mais en cas pratique il faudra le représenté ainsi : `http://127.0.0.1:8000/api/projects/1`, ici si nous souhaitons accéder au projet d'identifiant 1.

    endpoints :

Enregistrer un utilisateur : `http://127.0.0.1:8000/api/register/`

S'identifier : `http://127.0.0.1:8000/api/token/`

Rafraichir le jeton : `http://127.0.0.1:8000/api/refresh/`

Accéder à la liste de ses projets : `http://127.0.0.1:8000/api/projects/`

Créer un projet : `http://127.0.0.1:8000/api/projects/`

Accéder au détail d'un projet : `http://127.0.0.1:8000/api/projects/{int:project}`

Modifier un projet : `http://127.0.0.1:8000/api/projects/{int:project}`

Supprimer un projet : `http://127.0.0.1:8000/api/projects/{int:project}`

Accéder à la liste des utilisateurs d'un projet : `http://127.0.0.1:8000/api/projects/{int:project}/users/`

Ajouter un utilisateur au projet : `http://127.0.0.1:8000/api/projects/{int:project}/users/`

Retirer un utilisateur du projet : `http://127.0.0.1:8000/api/projects/{int:project}/users/{int:user}`

Accéder à la liste des rapports de problèmes liés au projet : `http://127.0.0.1:8000/api/projects/{int:project}/issues/`

Créer un rapport de problème lié au projet : `http://127.0.0.1:8000/api/projects/{int:project}/issues/`

Accéder au détail d'un rapport de problème lié au projet : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}`

Modifier un rapport de problème lié au projet : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}`

Supprimer un rapport de problème lié au projet : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}`

Accéder à la liste des commentaires d'un rapport de problème : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}/comments/`

Créer un commentaire d'un rapport de problème : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}/comments/`

Accéder au détail d'un commentaire d'un rapport de problème : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}/comments/{int:comment}`

Modifier un commentaire d'un rapport de problème : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}/comments/{int:comment}`

Supprimer un commentaire d'un rapport de problème : `http://127.0.0.1:8000/api/projects/{int:project}/issues/{int:issue}/comments/{int:comment}`

    Informations complémentaires :

Pour d'avantage d'informations liés aux Endpoints (méthodes html (get (list, retrieve), post, update, delete), et les authorisations) Merci de vous référez à la documentation Postman proposée à la fin de ce document.

_______________________________________________________________________________
_______________________________________________________________________________

ECHANTILLON TEST ET MISE EN GARDE :

    Informations sur l'échantillon permettant d'exemplifier l'utilisation de l'application :

Des comptes utilisateurs, tables de contributions, projets, rapports de problèmes et commentaires sont proposés afin que vous puissiez tester l'API.

Afin de vous connecter avec l'un de ces comptes utilisateurs, voici leur email et mot de passe :

Premier utilisateur :
email : coucou@coucou.fr
password : coucou_password

Second utilisateur :
email : userone@users.fr
password : userone_password

Troisième utilisateur :
email : testuserone@test.fr
password : testuserone_password

Si vous désirez consulter directement ces informations, vous pouvez vous connecter sur la page d'administration proposée à cet effet avec l'email admin et le password admin sur le lien : `http://127.0.0.1:8000/admin/`

email admin : admin@admin.fr
password admin : admin_password
_______________________________________________________________________________

    Attention ! :

Cet API a été réalisé dans le cadre d'un exercice éducatif. 

C'est dans ce contexte que des échantillons servant d'exemple d'application, communiquant des données sensibles, ont été partagés ci-dessus. 

Si vous désirez utiliser et déployer cet API pour d'autres usages, merci de prendre ces informations en considration et de supprimer cet échantillon pour éviter toute problématique liée à la sécurité de votre application utilisant l'API.

Pour cela, vous pouvez soit :

* Partant de la page d'administration supprimer manuellement les échantillons comportant des données sensibles

* Réinitialiser la base de données

Pour réitnialiser la base de données:  

* Veuillez supprimer les fichiers de migration actuels :

- Pour supprimer les migrations d'authentication , dans votre terminal, accéder au dossier ITSys, puis entrez les commandes :

Sur Microsoft Windows : `cd authentication/migrations`

puis, toujours sur Microsoft Windows : `Remove-Item * -Include *.py -Exclude *__init__*`

Sur Linux ou Mac : `cd authentication/migrations`

puis, toujours sur Linux ou Mac : `rm -v !("__init__.py")`

- Ensuite, pour supprimer les migrations de projectsManager, dans votre terminal, accéder au dossier ITSys, puis entrez les commandes :

Sur Microsoft Windows : `cd projectsManager/migrations`

puis, toujours sur Microsoft Windows : `Remove-Item * -Include *.py -Exclude *__init__*`

Sur Linux ou Mac : `cd projectsManager/migrations`

puis, toujours sur Linux ou Mac : `rm db.sqlite3`

- Enfin, pour supprimer votre base de données actuelle, dans votre terminal, accéder au dossier ITSys, puis entrez les commandes : 

Sur Microsoft Windows : `Remove-Item db.sqlite3`

Sur Linux ou Mac : `rm db.sqlite3`

* Veuillez récréer une base de donnée vierge, en réalisation une migration, 

- Pour cela, initialisez la migration, à partir du terminal veuillez accéder au dossier ITSys, puis entrez la commande :

Sur Microsoft Windows : `python manage.py makemigrations`

Sur Linux ou Mac : `python3 manage.py makemigrations`

- Puis réalisez la migration,  à partir du terminal , entrez la commande :

Sur Microsoft Windows : `python manage.py migrate`

Sur Linux ou Mac : `python3 manage.py migrate`

La base de données a été réinitialisée.

Attention, cela signifie que l'administrateur n'existe plus non plus, vous devez en créer un si vous désirez accéder à la page d'administration. Pour cela, à partir du terminal veuillez accéder au dossier ITSys, puis entrez la commande :

Sur Microsoft Windows : `python manage.py createsuperuser`

Sur Linux ou Mac : `python3 manage.py createsuperuser`

Puis renseignez les informations demandées dans le terminal pour finaliser la création du compte administrateur. Veillez à enregistrer un mot de passe robuste pour éviter toute faille liée à la sécurité. Il est conseillé à cet effet de créer un mot de passe d'au moins 8 caractères, composé de lettres, de chiffres et de caractères spéciaux.

_______________________________________________________________________________
_______________________________________________________________________________

DOCUMENTATION :

Documentation technique Postman sur les Endpoints et leurs logiques : https://documenter.getpostman.com/view/27948551/2s93z6diwa
