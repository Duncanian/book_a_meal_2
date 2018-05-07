[![Build Status](https://travis-ci.org/Duncanian/book_a_meal_2.svg?branch=feature)](https://travis-ci.org/Duncanian/book_a_meal_2)
[![Coverage Status](https://coveralls.io/repos/github/Duncanian/book_a_meal_2/badge.svg?branch=feature)](https://coveralls.io/github/Duncanian/book_a_meal_2?branch=feature)

### Book-A-Meal API

#### Description
This is a meal booking API that is used by users(customers) alongside with Admins (Caterers) to administer meal activities. 

 - #### Available working endpoints
|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v2/auth/signup` |  Register a user. |
|POST| `/api/v2/auth/login` | Login user.|
|GET| `/api/v2/meals/` | Get all the meal options. |
|POST| `/api/v2/meals/` |  Add a meal option. | 
|PUT| `/api/v2/meals/<meal_id>` | Update the information of a meal option. |
|DELETE| `/api/v2/meals/<meal_id>` | Remove a meal option. |
|POST| `/api/v2/menu/` | Set up the menu for the day. |
|GET| `/api/v2/menu/` | Get the menu for the day. |
|POST| `/api/v2/orders/` | Select the meal options from the menu. |
|PUT|`/api/v2/orders/<order_id>` | Modify an order. |
|GET|`/api/v2/orders/` | Get all the orders. |


### Development

Clone the repository: 

```
git clone https://github.com/Duncanian/book_a_meal_2.git
```

Navigate to the cloned repo. 

Ensure you have the following:

```
1. python3 & a virtualenv
2. Flask
3. Postman
```

To install Python checkout:
```
https://www.python.org/
```

Create a virtualenv and activate it.
``` 
[Refer here](https://docs.python.org/3/tutorial/venv.html)
```

### Dependencies and Installation
- Install the project dependencies:
```
> $ pip install -r requirements.txt
```

- Configure Environment.
```
$ export APP_SETTINGS="default"
$ export DEV_DATABASE="path to your database"
$ export SECRET="Secret Key Here"
```
> Note replace the value for DEV_DATABASE with real database path and SECRET with a strong string value


- Configure database
```
$ python manage.py database init
$ python manage.py database migrate
$ python manage.py database upgrade
```

After setting up the above. Run:

```python run.py```

Test the endpoints registered on `base.py` on Postman/curl on the port the app is running on.
The app should be accessiable via : http://127.0.0.1:5000/

### Session Examples
To Follow along with this examples get postman : 
```We will start off with an Admin(Caterer)```  

The admin user is created manually as it should be only one unique person. So we have one by the username of "admin" and password is "admin"

- Login
    - Post data in the format below to the login endpoint : ```/api/v2/auth/login```
    ```
    {
        "username":"admin",
	    "password":"admin"
    }
    ```

	- Output
	Copy the token returned and add it into the headers as a key pair value of ```Authorization : [put token here]```


- Add a meal Item

    - Post data in the format below to the book_a_meal endpoint: ```/api/v2/meals/```
    ```
    {
        "meal_name":"Rice",
        "meal_price":20
    }
    ```
    -Output
    ```
    {
    	"message": "New meal added!"
    }
    ```

- Get all meals
    - Get data from the endpoint: ```/api/v2/meals/```
    ```
    {
	    "status": "success",
	    "data": [
	        {
	            "meal_id": 1,
	            "meal_name": "Rice",
	            "meal_price": 20
	        },
	        {
	            "meal_id": 2,
	            "meal_name": "Beans",
	            "meal_price": 27
	        }
	    ]
	}
    ```

- Update a meal
    - Put data to the endpoint :```/api/v2/meals/<meal_id>```
    ```
    {
        "meal_name":"Rice",
        "meal_price":70
    }
    ```
    -Output
    ```
    {
    	"status": "success",
    	"data": 'Meal modified!'
    }
    ```

- Delete a meal
    - Delete data at an endpoint:```/api/v2/meals/<meal_id>```
    -Output
    ```
    {
    	"message": "The meal has been deleted"
    }
    ```

- Add meals to a menu
    - Post data to ```/api/v2/menu/``` in the format:
    ```
    {
        "meal_ids":[1, 2, 3],
        "menu_name":"Easter"
    }
    ```

    -Output
    ```
    {
    	"message": "New meal added to the menu!"}
    ```


- Get all orders made
    - Get data from the endpoint:```/api/v2/orders/```
    -Output
    ```
    {
	    "status": "success",
	    "data": [
	        {
	            "id": 1,
	            "order_meal": "Rice",
	            "order_price": 20,
	            "order_date": "2018-05-06",
	            "order_time": "15:29:39.433448",
	            "qty": 1,
	            "user_id": 1
	        },
	        {
	            "id": 2,
	            "order_meal": "Beans",
	            "order_price": 27,
	            "order_date": "2018-05-06",
	            "order_time": "15:29:39.433448",
	            "qty": 1,
	            "user_id": 1
	        }
	    ]
	}
    ```


```A normal user's activities```
- Signup/Register
    - Post data in the format below to the signup endpoint : ```/api/v2/auth/signup```
    ```
    {
        "username":"ian",
	    "password":"#2345"
    }
    ```

	- Output
	```
    {
    	"message": "New user created!"
    }
    ```

- Login
    - Post data in the format below to the login endpoint : ```/api/v2/auth/login```
    ```
    {
        "username":"ian",
	    "password":"#2345"
    }
    ```

	- Output
	Copy the token returned and add it into the headers as a key pair value of ```Authorization : [put token here]```


- Get all items in the menu
    - Get data from the menu endpoint: ```/api/v2/menu/```
    ```
    ```

- Order items in the menu
    - Post data in the format below to the menu endpoint : ```/api/v2/orders/```
    ```
    {
        "meal_ids" : [1, 2, 3]
    }
    ```

	- Output
	```
	{
		"message": "Your order was successfully created!"
	}
	```

- Update an order
    - Put data to the endpoint :```/api/v2/orders/<order_id>```
    ```
    {
        "qty" : 3
    }
    ```
    -Output
    ```
    {
    	"status": "success", 
    	"data": 'Order modified!'
    }
    ```

- Delete a meal
    - Delete data at an endpoint:```/api/v2/orders/<order_id>```
    -Output
    ```
    {
    	"message": "The order has been removed"
    }
    ```


## Running the tests

```
$ python -m pytest
```
- With Coverage

```
 $ python -m pytest --cov-report term-missing --cov=views
```

#### Contribution
Fork the repo, create a PR to this repository's develop.
