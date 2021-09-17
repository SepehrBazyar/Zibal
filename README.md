# Zibal
Zibal Recruitment Task Project with Django REST Framework

### Args:
* type (str): Specifies the Type of Output Value ["count", "amount"]
* mode (str): Specifies the Type of Report Category ["daily", "weekly", "monthly"]
* merchantId (Optional[str]): Mongo ObjectId if not Submit Information of All Users

### Returns:
* A List of Objects Contains "key" for Horizontal Axis and "value" for Vertical Axis

## Tools:
1. Back-End: Python, Django, REST API
2. DataBase: MongoDB(PyMongo), SQLite

## How to Run?
1. Clone the Project
* `git clone https://github.com/SepehrBazyar/Zibal.git`
2. Create a Virtual Environment("venv" is a Selective Name).
* `virtualenv venv`
3. Activate the Interpreter of the Virtual Environment
* Windows: `venv\Script\active`
* Linux: `source venv/bin/active`
4. Install the Requirements
* `pip install -r requirements.txt`
5. Write the Following Command to Import Data Collecton from BSON File
* `python manage.py convert transaction.bson` ("transaction.bson" is an Example File).
6. Write the Following Command to Create Your Tables
* `python manage.py migrate`
7. Run the MongoDB
8. Write the Following Command to Run the Server
* `python manage.py runserver`

## Features:
* Implement Cache Decorator to Faster Query by Save Results in Collection
* Writing Unit Test with Sample Information in TDD Method
