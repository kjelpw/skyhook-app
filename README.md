# skyhook-app
[python release](https://pypi.org/project/skyhook-timer/)

Plugin for tracking Skyhook timers in [Alliance Auth](https://allianceauth.readthedocs.io/en/v4.4.2/index.html)

## Contents

- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Permissions](#permissions)

## Key Features
* Adding a table entry with system name, planet, and countdown time remaining
* Alliance Auth nav menu count of Skyhooks close to their vulnerable timer

## Screenshots

### View timers
![image](https://github.com/user-attachments/assets/12dc48a9-6491-4fc8-bd1a-ce80461d4da7)

### Add a timer (or update an existing one)
![image](https://github.com/user-attachments/assets/0f217720-e334-466c-bc4b-b0d154e3dbab)

### Admin view
![image](https://github.com/user-attachments/assets/6e31a26f-eefa-4ed9-8882-145eeb7e1e61)


## Installation

### 1 - Install app

Install into your Alliance Auth virtual environment from PyPI:

```bash
pip install skyhook-timer
```

### 2 - Configure AA settings

Add `'skyhook_timer'` to `INSTALLED_APPS`

### 3 - Finalize installation into AA

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for AA

### 4 - Setup permissions

Now you can access Alliance Auth and setup permissions for your users. See below

## Permissions

This is an overview of all permissions used by this app:

Name | Purpose | Code
-- | -- | --
Can add skyhook timer | Can create a unique skyhook timer with system/planet and time. If the system/planet timer exists already it overwrites | add_skyhooktimer
Can view skyhook timer | Allows viewing of the nav menu link, and rendering of the skyhook timer page. This should be added to all users/members/states/groups that should be able to view skyhook timers | view_skyhooktimer

# CHANGELOG

### 0.0.49
- Better Skyhook Adding, matches ingame time system.
- Changed default permissions

### 0.0.43
- Limited stable release
