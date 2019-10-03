<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple RESTful app written in php using laravel framework 

Here's what this app can do:
* Authentication operations such as sign up, login, logout.
* Logged in user can add, update and delete products with different attributes.
* All users can search among products.

About the app:
* Searching is implemented using elasticsearch to be fast.
* Main database is MySql. But elasticsearch is also used for searching.
* Communicating with elasticsearch is done using laravel queues to prevent performance drop.
* This app also has a simple user interface.
