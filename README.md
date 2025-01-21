# Django_Ecommerce

Creating an Ecommerce with Django

# Virtual env

All dependencies and packages for the web, won't affect python's default OS dependencies

## Create virtual env

```bash
    python -m venv .venv
```

## Run virtual env

```bash
    . .venv/Scripts/activate
    # or
    source .venv/Scripts/activate
```

## Exit virtual env

Control + C or

```bash
    deactivate
```

# Django

## Install Django

Of course inside virtual env

```bash
    pip3 install django
```

## Create new Django project

django-admin startproject NAME_APP [actual_directory]

```bash
    django-admin startproject ecommerce .
```

## Run server

```bash
    python manage.py runserver
```

## About Django app generated files by default

init.py
default file that will start in any module

asgi.py & wsgi.py
config to the door of django, it administrate the async door for the server

settings.py
here contains or properties and settings the app need to start

urls.py
contains all urls of the website

---
## MVT Pattern in Django

Django uses the MVT Pattern = Model > View > Template

---
# Creating Home Page of eCommerce

lets copy the html template and create ecommerce > static folder, then copy the 4 folders inside static
let's do the changes in settings.py and finally execute:

```bash
    python manage.py collectstatic
```

---
# Create "Category" model in Django
1.  `python manage.py startapp category`
2. then we have to register the app in our project, we go to ecommerce > [settings.py](./ecommerce_django/ecommerce/settings.py)
and write in "INSTALLED APPS"
    ```python
        INSTALLED_APPS = [
            ...
            "category",
            ...
        ]
    ```
3. create the Category model in category > [models.py](./ecommerce_django/category/models.py)
   ```python
        # Create your models here.
        class Category(models.Model):
            category_name = models.CharField(max_length=50, unique=True)
            description = models.CharField(max_length=255, blank=False)
            slug = models.CharField(max_length=100, unique=True)
            category_image = models.ImageField(upload="photos/categories", blank=True)

            class Meta: # how will be shown in Django admin panel
                verbose_name= "category" # when singular
                verbose_name_plural = "categories" # when plural

            def __str__(self) -> str:
                return self.category_image + ": " + self.slug
    ```
4. Now to register the new Category entity in Django, have to go to category > [admin.py](./ecommerce_django/category/admin.py)
    ```python
        from .models import Category

        # Register your models here.
        admin.site.register(Category)
    ```

5. Have to install Pillow package so we can upload files like the category_image
    `pip3 install pillow`

6. Now we have to do migrations
`python manage.py makemigrations`
will generete the changes in [0001_initial.py](./ecommerce_django/category/migrations/0001_initial.py) that will do once we migrate:
`python manage.py migrate`
now the table in Django has been generated
---
# Create superuser in Django
`winpty python manage.py createsuperuser`
___
# Create Users App 'account' model in Django
## Why exactly?
by default, Django uses the username to join to the Django admin dashboard, so what I'm doing here is reestructuring this so we can login not only with username, so now can login with username and email. 

**Create this new app just as we did before with 'Category'.**
**BUT** there are some changes in accounts > [models.py](./ecommerce_django/accounts/models.py)
    ```python
        from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

        # Create your models here.
        class MyAccountManager(BaseUserManager):
            def create_user(self, first_name, last_name, username, email, password=None):
                if not email:
                    raise ValueError("User must have an email! -.-")
                if not username:
                    raise ValueError("User must have an username! -.-")

                user = self.model(
                    email = self.normalize_email(email),
                    username = username, 
                    first_name = first_name,
                    last_name = last_name,

                )
                user.set_password(password)
                user.save(using=self._db)
                return user

            def create_superuser(self, first_name, last_name, username, email, password):
                user = self.create_user(
                    email = self.normalize_email(email),
                    username= username,
                    password= password,
                    first_name= first_name,
                    last_name= last_name,
                )
                user.is_active = True
                user.is_superadmin = True
                user.is_admin = True
                user.is_staff = True
                user.save(using=self._db)
                return user

        class Accounts(AbstractBaseUser):
            first_name = models.CharField(max_length=50)
            last_name = models.CharField(max_length=50)
            username = models.CharField(max_length=50, unique=True)
            email = models.CharField(max_length=100, unique=True)
            phone_number = models.CharField(max_length=100)

            # Django attributes
            # that need Django by default, if not have them, will show errors
            date_joined = models.DateTimeField(auto_now_add=True)
            last_login = models.DateTimeField(auto_now_add=True)
            is_active = models.BooleanField(default=False)
            is_superadmin = models.BooleanField(default=False)
            is_admin = models.BooleanField(default=False)
            is_staff = models.BooleanField(default=False)

            USERNAME_FIELD = 'email' # use the email as necessary field for login
            REQUIRED_FIELDS= ["username", "first_name", "last_name"]

             # so we can use create users just as I specified
            objects = MyAccountManager()


            def __str__(self):
                return self.email + ": " + self.first_name + " " + self.last_name

            def has_admin_permissions(self, perm, obj=None):
                return self.is_admin

            def has_module_permissions(self, add_label):
                return True
    ```
this is what it needs.

2. Now have to go to ecommerce > [settings.py](./ecommerce_django/ecommerce/settings.py)
```python
    WSGI_APPLICATION = 'ecommerce.wsgi.application'
    # after this line, write: 

    AUTH_USER_MODEL = "accounts.Account"
``` 
so we are specifying to Django that the user structure will be the one I created

3. Register the "account" class in Django
go to accounts / [admin.py](./ecommerce_django/accounts/admin.py)
    ```python
        from .models import Account

        # Register your models here.
        admin.site.register(Account)
    ```

## New Migration ?
we are restructuring Django, so we can't just do makemigrations & migrate, we have to do something first.
**WE HAVE TO DELETE:**
1. delete [db.sqlite3](./ecommerce_django/db.sqlite3)
    so we delete the user information we have, we have to delete it because we reestructured the user info
2. go to category / [migrations](./ecommerce_django/category/migrations/)
    and delete all migrations files we have done before, like:
    * [0001_initial.py](./ecommerce_django/category/migrations/0001_initial.py)
    * [0002_alter_category_options.py](./ecommerce_django/category/migrations/0002_alter_category_options.py)

## Run server
we have to run the server now, so we can regenerate the [db.sqlite3](./ecommerce_django/db.sqlite3) file.
Will show errors, but is ok, we do this only to regenerate the db.

## Do new migrations
`python manage.py makemigrations`, then `python manage.py migrate`
now we can run the server

## Create superuser one more time, bc we deleted it
`winpty python manage.py createsuperuser`

# Changes in Account table in Django admin dashboard
these are some changes in account > [admin.py](./ecommerce_django/accounts/admin.py)
so we can set password as not editable.
and some changes in table visualization

# Download SQLite Studio
go to [https://sqlitestudio.pl/](https://sqlitestudio.pl/) and install the download it recommends to you.

# Products Module
## Create Products app and setting it up
**just as we did before with "Category" app, in line 85**
1. `python manage.py startapp store`
2. add the app to INSTALLED APPS
3. create the Store model in store > models.py
4. Now to register the new Store entity in Django, have to go to store > admin.py
5. make migrations: `python manage.py makemigrations` so can create the db table of
6. `python manage.py migrate` so now execute the migration file

## Show Categories in dropdown & filtering products
1. create new file "context_processor.py" in category app
2. go to [settings.py](./ecommerce_django/ecommerce/settings.py) and go to "TEMPLATES = []"
and add the menu links. here what we are doing is making public this "menu_links" to any template. 
So any template will have access to it.
    ```python
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': ["templates"],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'djancgo.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        "category.context_processors.menu_links",
                    ],
                },
            },
        ]
    ```
3. modifyin html
4. create "get_url" function in [models.py](./ecommerce_django/category/models.py)

# Create 'Carts'
`python manage.py startapp carts`