# CoinValueTracker

Flask Web Application

## Introduction

This is a Flask web application that allows users to register, log in, view cryptocurrency prices, and perform a simple bitcoin exchange calculation. The application scrapes data from a website and stores it in a SQLite database for display. It utilizes Flask, SQLAlchemy, BeautifulSoup, and other libraries to handle various functionalities.
Bootstrap is used for visual elements.

## Video Demo
https://youtu.be/LNPvPJb_LDM
## Features

- User registration and login system
- Display of cryptocurrency prices, which are scraped from `www.blockchain.com`
- Bitcoin exchange calculation based on live bitcoin price
- User profile management (*TO BE COMPLETED)
- Dynamic search box using JavaScript


### User Registration and Login System

This feature allows users to register and log in to the web application. Users can create an account by providing a username, email, and password. 
The registration process includes password confirmation. After successful registration, users can log in using their email and password. User information is
saved to `user` table in `info.db` database.

### Display of Cryptocurrency Prices

This feature retrieves cryptocurrency prices from a website and displays them on the web application. 
The application utilizes web scraping techniques using BeautifulSoup library to extract the necessary information. 
The scraped data is then stored in a SQLite database in `price` table and rendered on the prices page.

### Bitcoin Exchange Calculation

The web application provides a simple bitcoin exchange calculation functionality. 
Users can enter the amount of bitcoin they want to exchange, and the application fetches the current bitcoin price from the website.
It then calculates the equivalent amount in the user's selected currency and displays the result.

### User Profile Management

Users can manage their profiles through this feature. After logging in, users can access their profile page, where they can view and update their username. 
The profile update functionality allows users to change their username. The changes are reflected in the database and displayed on the profile page. ***Profile picture
management system is under development**

### Dynamic Search Box using JavaScript

This feature enhances the user experience by providing a dynamic search functionality. 
When a user types in the search input field, the JavaScript code filters the table rows based on the entered search term.
The table rows that match the search term are displayed, while the others are hidden.

## Requirements
- Python 3.11
- Flask
- Flask SQLAlchemy
- Beautiful Soup 4
- requests
- datetime

## Installation

1. Clone the repository:

```
git clone https://github.com/GiorgiTarsaidze/CoinValueTracker
```
2. Run the application with
```
python blockchain.py
```
or
```
flask --app blockchain run
```
3. Access the application in your web browser at `http://localhost:5000`

## Important Notes
1. If for some reason database is not working, comment line 63 in `blockchain.py`, run the application, reach the endpoint `/prices`. After, shut down the server, uncomment line 63 and run the application again.
2. If you want to delete a specific user from the database, uncomment lines 210-222, where you can reach special endpoint `/delete_user/<int:user_id>`, where `<int:user_id>` is the id of the user you want to delete from the table.
## Endpoints
The following are the available endpoints:

- `/home` or `/` - Home page.
- `/prices` - Display cryptocurrency prices.
- `/bitcoin` - Display the current Bitcoin price.
- `/exchange` - Perform a Bitcoin exchange calculation.
- `/register` - User registration page.
- `/login` - User login page.
- `/logout` - Log out the user.
- `/profile` - User profile page.
- `/update_profile` - Update user profile information.
  

Feel free to explore and modify the script according to your needs. This project was created by Giorgi Tarsaidze.
