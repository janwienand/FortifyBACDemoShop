# Fortify Broken Access Control Demo Shop

This is a sample web application for a demo shop built using Flask and SQLite. This project is a simple web shop application that allows users to log in, browse products, add them to a shopping cart, and check out. The application has a known vulnerability: a Cross-Site Request Forgery (CSRF) vulnerability that allows an attacker to perform actions on behalf of a user without their knowledge.

## Vulnerability Details

The CSRF vulnerability occurs when a user logs in to the site and then visits the Malicious Website (CSRF-example.html) that contains a hidden form that performs an action (user creation) on the demo site. If the user is still logged in, the form will be submitted using the user's session information, allowing the attacker to perform actions on behalf of the user without their knowledge or consent.

## Installation

To install and run the project, follow these steps:

    1. Clone the repository to your local machine.
    2. Run the application by running python app.py.
    3. Navigate to localhost:5000 in your web browser to use the application.

## Exploit vulnerability

To exploit the CSRF vulnerability, follow these steps:

    1. Have a look at the current users in the shopping.db database (using SELECT * FROM users or the show-all-users.sql) 
    2. Log in with username 'Alice' and password 'secret'
    3. Open the Malicious Website (CSRF-example.html) in another tab and click on the 'Submit' button.
    4. Have a look at the user database again and look for some new users

![](https://gifyu.com/image/S7Mmb)