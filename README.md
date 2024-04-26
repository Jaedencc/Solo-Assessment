## Computer Shopping Station
This web application is designed as a solo assessment to offer a fundamental online shopping experience. It allows users to execute basic actions such as logging in, registering, searching, and making purchases. Super users have the ability to add, edit, and remove products, as well as access user order details and view bar graphs related to product brands. Additionally, the application integrates a country information table to display data about the virtual sales countries.

## Setting environment
After cloning the repository and navigating to the project directory, you can start the following actions.
```
pyenv local 3.10.7 # this sets the local version of python to 3.10.7
python3 -m venv .venv # this creates the virtual environment for you
source .venv/bin/activate # this activates the virtual environment
pip install --upgrade pip #optional

pip install django==4.1.0
pip install faker
```

## Generating migration fils
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Parsing data from .csv fils
```
python3 manage.py parse_csv
```

## Set libraries for bar chart 
Using the Plotly library to generate the chart needed for the application.(https://plotly.com/python/bar-charts/)
```
pip install plotly   # chart/table library 
pip install pandas   # for Plotly Express
```


## Creating superuser
Before running the application, you also need a create a superuser. Logging into the superuser account in the application gives you access to more features.
```
python manage.py createsuperuser
```

## Running application
```
python3 manage.py runserver 0.0.0.0:8000   # for Codio  
```
You can now access the web application at localhost:8000



## Test
Installing chromium browser
```
sudo apt-get install -y chromium-browser
sudo apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1
```

Installing and configuring Behave
```
pip install behave
pip install selenium
```

Now you can run the Test
```
behave
```

## Reminders for use
- Users can click on the country code in the product detail page to display the map information.
- Users can search for products by brand name.

After Super User Login
- On the Home page you will find new features: View Brand Chart | Add a new product | Orders
- New functions are also available on the product details page: Edit | Delete
