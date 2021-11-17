
---

# The Good Samaritan Org

![GS logo](media/base/logo-no-bg.png)

The Good Samaritan is a non profit organization for humanitarian support. Our target is support orphan children, widows, disabled people and elderly.
Please donate to The Good Samaritan Organization to support people in Mozambique to have a more dignified life.

Find out more about this project and help:

[Instagram](https://www.instagram.com/bomsamaritanomozambique/)

[Facebook](https://www.facebook.com/Minist%C3%A9rio-BOM-Samaritano-Mozambique-800507056757640)

[Click here to see the project live]()

---

## Tables of Contents

- [Borderless](#borderless)
- [Tables of Contents](#tables-of-contents)
- [UX](#ux)
  - [The purpose of the website is to present the follow values:](#the-purpose-of-the-website-is-to-present-the-follow-values)
  - [User Stories:](#user-stories)
- [Design Process:](#design-process)
  - [Framework](#framework)
  - [Wireframing the project on Balsamiq](#wireframing-the-project-on-balsamiq)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Implementations](#future-implementations)
- [Technologies Used](#technologies-used)
  - [Front-End Technologies](#front-end-technologies)
  - [Back-End Technologies](#back-end-technologies)
- [Testing](#testing)
  - [Testing User Stories](#testing-user-stories)
  - [Creating an Account](#creating-an-account)
  - [Log In](#log-in)
  - [Add, Edit and Delete a Trip Post](#add-edit-and-delete-a-trip-post)
  - [Pagination](#pagination)
  - [Trip Post](#trip-post)
  - [Validating The HTML and CSS code](#validating-the-html-and-css-code)
  - [Testing in different browsers](#testing-in-different-browsers)
  - [Known Issues](#known-issues)
- [Accessibility](#accessibility)
- [Deployment](#deployment)
  - [Local Deployment](#local-deployment)
  - [Remote Deployment](#remote-deployment)
- [Cloning my project](#cloning-my-project)
- [Credits](#credits)
  - [Acknowledgements](#acknowledgements)

---

## UX

### The purpose of the website is to present the follow values:
  * Share the purpose of The Good Samaritan org in Mozambique.
  * Encourage and gain user confidence.
  * Provide multiple options of donating and help.
  * Create a resposive design, wich works in different screen sizes and devices, due the fact that people use more mobile devices nowadays.

### User Stories:

  *"As a user, I would like to _____________________________"*

  * *view the site from any device (mobile, tablet, desktop).*
  * *donate products as a guest.*
  * *donate all products at once.*
  * *sort products.*
  * *Filter products by category.*
  * *search products by trip name and category.*
  * *donate a parcel as a guest.*
  * *sponsor a child, widow or elderly as a guest. (recurrent donation)*
  * *view my donation in a pre checkout are like a cart or a bag*
  * *edit my donation in the cart*
  * *remove products from the cart*
  * *remove all products from the cart at once*
  * *have a secure checkout*
  * *receive an email confirming my donation after checkout*
  * *have the possibility to download a pdf with donation details after checkout*
  * *find a page where I can know more about the organization*
  * *Finish any current sponsorship as a guest*
  * *create my own account.*
  * *login with my email or user name.*
  * *login with third party account(google).*
  * *Recover any sponsorship created before create my account on my profile*
  * *view my order history on my own profile.*
  * *manage my sponsorship on my own profile. (see details and finish sponsorship)*
  * *edit my profile details.*
  * *save my profile details when checkout.*
  * *find a contact form.*
  * *be able to log out.*

Back to the [Tables of Contents](#tables-of-contents)

---  

## Design Process:

  ### Framework
  * [Bootstrap](https://getbootstrap.com/):
    * Bootstrap is a responsive mobile-first design framework with a clean and modern layout, with its simple-to-understand documentation.
  * [Jquery](https://jquery.com/):
    * In an effort to keep the JavaScript minimal, I have decided to use jQuery as foundation to my scripts framework.
  * [Django](https://www.djangoproject.com/):
    * Django is a framework that I've used to render the back-end Python with the front-end Bootstrap.
  * [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/):
    * Django-crispy-forms is an application that helps to manage Django forms. It allows adjusting forms' properties (such as method, send button or CSS classes) on the backend without having to re-write them in the template.


  ### Wireframing the project on Balsamiq
  * [Balsamiq](https://balsamiq.com/):
    * Software used to build the wireframe of this project. Because Code Institute have provided all students with free access for a limited time and the simplicity and ease of use.

  * **The wireframe can be seen here**:
    <!-- * [Wireframe](app/static/files/readme/borderless_wireframe.pdf) -->

Back to the [Tables of Contents](#tables-of-contents)

---

## Features

### Existing Features

  * This project has eighteen separate pages, which are:
    * **"Home"** page, which is the land page;
    * **"Who We Are"** page which contains the information about the organization;
    * **"FAQs"** page which contains the questions that are frequently asked to The Good Samaritan Org;
    * **"Contact Us"** page which contains a form to the user send any question to the org;
    * **"Register"** page which contains a form to the user create an account;
    * **"Log In"** page which contains a form to the user log in using email, user name or third party account (google);
    * **"Finish Sponsorship"** page which contains a form to the user finish a sponsorship as a guest;
    * **"Product Management"** page where the site owner can manage products and parcels;
    * **"Update Product or Parcel"** page which contains a form to the site owner update products or parcels details;
    * **"My Profile"** page where the user can view his donation history, current sponsorship, recover a sponsorship, edit profile details and access the Product Management page (if site owner);
    * **"Family Parcels"** page where the user can choose a parcel to donate;
    * **"Sponsorship"** page where the user can choose a sponsorship to subscribe;
    * **"Products"** page where the user can choose a product to donate;
    * **"Products Details"** page where the user can view the product details before donate;
    * **"Donation Cart"** page where the user can see all chosen products before checkout;
    * **Check Out (products, parcels or sponsorship)** page which contains a form to the user checkout the chosen donation;
    * **"Confirmation Order"** page where the user can view and download donation details after checkout;
    * **"Past Confirmation Order"** page where the user can view and download donation details of a past order in the order history;

  * **Register Account**:
    * Anybody can register for free and create their own unique account. The project has built-in authentication and authorization to check certain criteria is met before an account is validated. All passwords are hashed for security purposes.
    ![signup form](app/static/images/readme/test/manual/signup_form.png)

  * **Log In to Account**:
    * For existing users, I have more authentication and authorization incorporated to check that the hashed passwords and username match the database, the user can log in using a third party account (google) as well.
    ![signup form](app/static/images/readme/test/manual/login_form.png)

  * **Log Out of Account**:
    * Users can easily log out of their account with the click of a button.
    ![logout btn](app/static/images/readme/test/manual/logout_btn.png)
  
  * **Navbar**:
    * The navbar is different, depending whether the user is logged in or not. The 'My Account' Dropdown menu options will be different.
    
      * Navbar when the user is logged:
      ![logged navbar](app/static/images/readme/test/manual/logged_navbar.png)

      * Navbar when the user is logged out:
      ![logged out navbar](app/static/images/readme/test/manual/loggedout_navbar.png)
  
  * **Donate as a guest**:
    * Every user logged or not can donate a product, parcel and subscribe to a sponsorship.

        * [Feed Page](https://borderless-project.herokuapp.com/)
  
  * **Donate All Products**:
    * Button located in products page to donate all products at once, the products and total value may vary if the user sort the product list.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Most-Needed Items**:
    * Button located in products page to list the most needed items, products in this list may vary.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Donate Button (Products page)**:
    * Button located in products page to open the product details.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Donate Button (Product Details page)**:
    * Button located in products details page to add the product to the cart.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Donate Parcel Button (Parcels page)**:
    * Button located in parcels page to add the parcel to the cart.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
   
  * **Sponsor Button**:
    * Button located in Sponsorship page to subscribe to a sponsorship, just one subscription is allowed per user or email.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Profile Form**:
    * Form in the profile page to update profile details, this details are used to pre populate the checkout form and they can be updated when the user checkout a form and save details to profile.

    ![search bar feature](app/static/images/readme/test/manual/search_feat.png)

  * **Order History Column**:
    * Column in the profile page where the user can view his past donations and see the past donation details.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Recover Sponsorship**:
    * Section in the profile page where the user can recover any sponsorship created as a guest, the user only can see this section if he does not created a sponsorship while logged.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Sponsorship**:
    * Section in the profile page where the user can view and manage his current sponsorship, the user only can see this section if he already has a sponsorship.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Product Management Button**:
    * Button located in Profile page access the Product Management page, Just the site owner can see this button.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Edit Product or Parcel Button**:
    * Button to update product or parcel details, like price, name, sku and others details.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Remove Product Button**:
    * Button to remove a product from database.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Add New Product Button**:
    * Button to add a new product to database, Parcels can't be added, the number of parcels is fixed, they can be just edited.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Update Product Quantity Button**:
    * Button located in Donation Cart page to update the quantity of a product in the cart.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Remove Product Button**:
    * Button located in Donation Cart page to remove a product from cart.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Remove All Items From The Cart**:
    * Button located in Donation Cart page to remove all products from cart at once.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Save this information to my profile checkbox**:
    * checkbox located in checkout page to details from checkout form to profile.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)
  
  * **Top Page Search Bar**:
    * Search bar present in all pages to search any product by name or category.

      ![search bar feature](app/static/images/readme/test/manual/search_feat.png)

### Future Implementations

  * Enhace automated tests.

  * Create a way of interaction between sponsor and sponsored.

  * Create an annual report page, to inform the organization improvements, events and detailed spending.

Back to the [Tables of Contents](#tables-of-contents)

---

## Technologies Used

  * [Gitpod](https://gitpod.io/)
    * Used as my primary IDE for coding. Gitpod is an open source platform for automated and ready-to-code development environments that blends into your existing workflow directly from your browser.
  
  * [GitHub](https://github.com/)
    * Used as remote storage of my code online. A company that provides hosting for software development version control using Git.

  * [Code Institute Full Template](https://github.com/Code-Institute-Org/gitpod-full-template)
    * Used as a basic template to kick start the project.

  * [Balsamiq](https://balsamiq.com/)
    * Used for wireframing the project. [see wireframe](app/static/files/readme/borderless_wireframe.pdf)

  * [draw.io](https://drawio-app.com/)
      * Used to create the database schema. [See data base schema](app/static/files/readme/NoSQL_Schema.pdf)
  
  * [Chrome Dev Tools](https://developers.google.com/web/tools/chrome-devtools)
    * A set of web developer tools built directly into the Google Chrome browser. I used these tools constantly thoughout the development cycle.
  
  * [Canva](https://www.canva.com/)
    * I used the Canva platform to make the style guide.

  * [TinyPNG](https://tinypng.com/)
    * I used TinyPNG to compress my image files to try to reduce the loading time for each page.
  
  * [W3C markup validation service](https://validator.w3.org/)
    * Great tool to support throught the web development that helps to test and find issues on markup file.

  * [CSS validation service](https://jigsaw.w3.org/css-validator/)
    * Great tool to support throught the web development that helps to test and find issues on style file.
  
  * [W3C Schools](https://www.w3schools.com/)
    * W3C Schools is a great platform that covers all aspects of web development, great tools that provides information for developers.

  * [Stack Overflow](https://stackoverflow.com/)
    * Although it isn't a technology, I found a lot of guidance on Stack Overflow.

  * [MND Web Docs](https://developer.mozilla.org/en-US/docs/Web)
    * DN Web Docs, previously Mozilla Developer Network and formerly Mozilla Developer Center, is a documentation repository for web developers used by Mozilla, Microsoft, Google, and Samsung.

  * [CSS-tricks](https://css-tricks.com/)
    * Is a blog where you can find lots of tutorial and tricks to write a good css.

Back to the [Tables of Contents](#tables-of-contents)

  ### Front-End Technologies

  * [HTML 5](https://en.wikipedia.org/wiki/HTML5)
    * Used as the base for markup text. The language used to build the structure and add its content.

  * [CSS3](https://en.wikipedia.org/wiki/CSS)
    * Used as the base for cascading styles. The language used to style the HTML5 elements according to the design and color scheme.

  * [Bootstrap framework](https://getbootstrap.com/)
    * Used as the overall design framework. I decided to use Bootstrap's grid container system as I wanted to design my project with a 'mobile first' approach, but another bootstrap resources were used like the contact form.

  * [FontAwesome](https://fontawesome.com/)
    * FontAwesome icons is where I got most part of the icons for my design project.

  * [Google Fonts](https://fonts.google.com/)
    * I used Google fonts to provide the fonts of the website.

  * [Jquery](https://jquery.com/):
    * Used as the primary JavaScript functionality. In an effort to keep the JavaScript minimal, I have decided to use jQuery as foundation to my scripts framework.

  * [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/):
    * Django-crispy-forms is an application that helps to manage Django forms. It allows adjusting forms' properties (such as method, send button or CSS classes) on the backend without having to re-write them in the template.

Back to the [Tables of Contents](#tables-of-contents)
  
  ### Back-End Technologies

  * [Django](https://www.djangoproject.com/):
    * Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
  
  * [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html)
    * Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication.
  
  * [django-countries](https://pypi.org/project/django-countries/)
    * A Django application that provides country choices for use with forms, flag icons static files, and a country field for models.
  
  * [Pillow](https://pillow.readthedocs.io/en/stable/)
    * This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.
  
  * [pylint-django](https://pypi.org/project/pylint-django/)
    * pylint-django is a Pylint plugin for improving code analysis when analysing code using Django. It is also used by the Prospector tool.

  * [Cloudinary](https://cloudinary.com/)
    * Used to store products pictures

  * [Heroku](https://www.heroku.com/what)
    * Used for app hosting.
  
  * [Gunicorn - WSGI Server](https://docs.gunicorn.org/en/stable/)
    * Web Server used on Heroku for this project.
  
  * [Dj-database-url](https://pypi.org/project/dj-database-url/)
    * This simple Django utility allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application.
  
  * [Dango-storages](https://django-storages.readthedocs.io/en/latest/)
    * Django-storages is a collection of custom storage backends for Django.
  
  * [Amazon Web Services (S3)](https://aws.amazon.com/)
    * S3 provides the ability to store, retrieve, access, and back up any amount of data at any time and place. Used to store static files.
  
  * [Python 3.9.6](https://www.python.org/)
    * Used as the back-end programming language.
  
  * [Stripe](https://stripe.com/ie/about)
    * Online payment and subscription API, used as UI to manage the store payments as well.
  
  * [Dj-stripe](https://dj-stripe.readthedocs.io/en/master/)
    * dj-stripe implements all of the Stripe models, for Django. Set up your webhook endpoint and start receiving model updates. You will then have a copy of all the Stripe models available in Django models, as soon as they are updated!
  
  * [xhtml2pdf](https://xhtml2pdf.readthedocs.io/en/latest/usage.html)
    * xhtml2pdf enables users to generate PDF documents from HTML content easily and with automated flow control such as pagination and keeping text together.
  
  * [Waypoints](http://imakewebthings.com/waypoints/)
    * Waypoints is the easiest way to trigger a function when you scroll to an element, used to infinite scroll.

Back to the [Tables of Contents](#tables-of-contents)

---

## Testing

### Testing User Stories

*"As a user, I would like to _____________________________"*

* *view the site from any device (mobile, tablet, desktop).*

  * I manually tested the live project by doing the following:  
    * Using Google Developer Tools to view the project on devices with different screen sizes.
    * Asking for feedback from friends and family who opened and interacted with the project on their devices.
    ![responsiveness TEST](media/readme/responsiveness-test.PNG)

* *donate products as a guest.*
  * All visitors are able to donate products without an account.
    ![feed page](app/static/images/readme/test/manual/feed_page.png)

* *donate all products at once.*
![feed page](app/static/images/readme/test/manual/search.png)

* *sort products.*

* *Filter products by category.*

* *search products by trip name and category.*

* *donate a parcel as a guest.*
* *sponsor a child, widow or elderly as a guest. (recurrent donation)*
  * All visitors are able to donate parcels or subscribe to a Sponsorship without an account.

* *view my donation in a pre checkout are like a cart or a bag*

* *edit my donation in the cart*

* *remove products from the cart*

* *remove all products from the cart at once*

* *have a secure checkout*

* *receive an email confirming my donation after checkout*

* *have the possibility to download a pdf with donation details after checkout*

* *find a page where I can know more about the organization*

* *Finish any current sponsorship as a guest*

* *create my own account.*
    I've created my own personal account. In addition to this primary account, I've tested with about 5 fake accounts in order to confirm authentication and validation worked as expected. All authentication is handled by Django-Allauth.

* *login with my email or user name.*

* *login with third party account(google).*

* *Recover any sponsorship created before create my account on my profile*

* *view my order history on my own profile.*

* *manage my sponsorship on my own profile. (see details and finish sponsorship)*

* *edit my profile details.*

* *save my profile details when checkout.*

* *find a contact form.*

* *be able to log out.*

### Validating The HTML and CSS code
  
  #### HTML

  All pages checked. All errors and warnings fixed.

  * [W3C HTML Validator](https://validator.w3.org/) - Some erros and warning were found, like:
    * Duplicated Id;
    * Section lacks heading. Consider using h2-h6 elements to add identifying headings to all sections;
    * Bad value for attribute action on element form: Must be non-empty;
    * End tag span seen, but there were open elements;
    * Unclosed element i;

    When checking the sponsorship form page the HTML validator rise the following error:
    * "Duplicate ID id_stripe_public_key."
    I still trying to find what is causing it, because I can't find this id duplicated in the HTML document.
  
  In the second check was found a typo error, in the maxlength and minlength attribute of some input elements. This error was fixed.


  #### CSS3

  * [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) - No error found in the style sheet.

  #### JavaScript

  * [JShint](https://jshint.com/) - "Metrics: There are 20 functions in this file. Function with the Largest function has 13 statements in it, while the median is 1. The most complex function has a cyclomatic complexity value of 5 while the median is 1."

    ##### Common warnings:

    * "'arrow function syntax (=>)' is only available in ES6 (use 'esversion: 6').";
    * "'let' is available in ES6 (use 'esversion: 6') or Mozilla JS extensions (use moz).";
    * "'const' is available in ES6 (use 'esversion: 6') or Mozilla JS extensions (use moz).";
    * "'template literal syntax' is only available in ES6 (use 'esversion: 6')."
    * This code works well despite these warnings

    ##### Two undefined variables:

    * '$' - This is for jQuery, is a sign to define/access jQuery;
    * 'modal' - Which is a function to handle the modals;

* [JSesprima](https://esprima.org/demo/validate.html) - "Code is syntactically valid."

### Testing in different browsers

I manually tested the website on the following web browsers, checking buttons, responsiveness and design worked as planned:

  * Google Chrome
  * Mozilla Firefox
  * Microsoft Edge

### Known Issues

  1. The Unfollow button in public profile page, when clicked all code related to remove user from the specific field in the database works well and the button UI turn to a Follow Button, but it does not behave as a Follow button unless the page is reloaded.

  2. In case an user is logged with two pages opened in different tabs and one of theses pages is the profile page, if the user log out in the tab that isn't the profile and after try to reload the profile page, then he would see a KeyError error, because there is no longer any session called 'user'. This error was fixed adding a try/except statement in every page that needs a user logged to be used, if there is no longer session 'user', then redirect to feed page, which does not need the session 'user'.

  3. If a user create a trip where the place name does not exists in the country, the google maps is not rendered.

  4. Unfollow link in Following tab (profile page) and Remove Follower in the Followers tab (profile page), just work with a double click.

  5. ~~Icons from google maps are not rendering.~~ Fixed adding 'data:' data scheme to content security policy.

  6. ~~Pictures in preview photos in edit trip page are not redering~~ Fixed adding 'blob:' data scheme to content security policy

Back to the [Tables of Contents](#tables-of-contents)

---

## Accessibility

  * Each image has an alt attribute describing the image's function
  * Each anchor tag has an aria-label attribute describing where that link goes
  * Each section has an aria-labelledby attribute
  * Content has a contrast with the background to improve the visibility
  * Form inputs have labels

Back to the [Tables of Contents](#tables-of-contents)
---

## Deployment

### Local Deployment

Please note - in order to run this project locally on your own system, you will need the following installed:
  * [Python3](https://www.python.org/downloads/) to run the application.
  * [PIP](https://pip.pypa.io/en/stable/installation/) to install all app requirements.
  * Any IDE such as [Microsoft Visual Studio Code](https://code.visualstudio.com/).
  * [GIT](https://www.atlassian.com/git/tutorials/install-git) for cloning and version control.
  * [MongoDb](https://www.mongodb.com) to develop your own database either locally or remotely on MongoDB Atlas.

Next, there's a series of steps to take in order to proceed with local deployment:

  * Clone this GitHub repository by either clicking the green Clone or download button and downloading the project as a zip-file (remember to unzip it first), or by entering the following into the Git CLI terminal:
    * > git clone https://github.com/SanclerZanella/borderless_project.git

  * Navigate to the correct file location after unpacking the files.
    * > cd <path to folder>
  
  * Create a .env file with your credentials. An example can be found [here](.env_sample). Be sure to include your MONGO_URI and SECRET_KEY values.

  * Create a .flaskenv file and add the following entries:
    * > FLASK_APP=run.py
    * > FLASK_ENV=development
  
  * Install all requirements from the [requirements.txt](requirements.txt) file using this command:
    * > sudo -H pip3 -r requirements.txt
  
  * Sign up for a free account on [MongoDB](https://www.mongodb.com) and create a new Database called 2BN-Desserts. The Collections in that database should be as in the schema:
    * [Database Schema](app/static/files/readme/NoSQL_Schema.pdf)

  * You should now be able to launch your app using the following command in your terminal:
   * > flask run

  * The app should now be running on localhost on an address similar to http://10.116.8.16:8000/. Simply copy/paste this into the browser of your choice!

Back to the [Tables of Contents](#tables-of-contents)

### Remote Deployment

This site is currently deployed on [Heroku](https://circleci.com/signup/?gclid=CjwKCAjw9uKIBhA8EiwAYPUS3Jo8VIjh71KAycLOnAlgya-XRQB5GyYpVMR-wvLIxuVPrR3sgcD2bRoCZS0QAvD_BwE) using the master branch on GitHub. To implement this project on Heroku, the following steps were taken:

1. Create a requirements.txt file so Heroku can install the required dependencies to run the app.
    * > pip3 freeze --local > requirements.txt
    * My file can be found [here](requirements.txt).

2. Create a Procfile to tell Heroku what type of application is being deployed, and how to run it.
    * > echo web: python run.py > Procfile
    * My file can be found [here](Procfile).

3. Sign up for a free Heroku account, create your project app, and click the Deploy tab, at which point you can Connect GitHub as the Deployment Method, and select Enable Automatic Deployment.

4. In the Heroku Settings tab, click on the Reveal Config Vars button to configure environmental variables as follows:
    * IP: 0.0.0.0
    * PORT: 5000
    * MONGO_URI: <database_uri>
    * MONGO_DBNAME: <database_name>
    * SECRET_KEY: <your_own_secret_key>
    * MAP_KEY: <Google_maps_API_key>
    * CLOUDINARY_API_KEY: <Cloudinary_API_key>
    * CLOUDINARY_API_SECRET: <Cloudinary_secret>
    * CLOUDINARY_CLOUD_NAME: <Cloudinary_cloud_name>

5. Your app should be successfully deployed to Heroku at this point.

---

## Cloning a Repository

If you would like to work on my project further you can clone it to your local machine using the following steps:

  1. Scroll to the top of my repository and click on the "clone or download button"
  2. Decide whether you want to clone the project using HTTPS or an SSH key and do the following:
    * HTTPS: click on the checklist icon to the right of the URL
    * SSH key: first click on 'Use SSH' then click on the same icon as above
  3. Open the 'Terminal'
  4. Change the current working directory to the location where you want the cloned directory
  5. Type 'git clone', and then paste the URL you copied earlier.
  6. Press 'Enter' to create your local clone.

You can find both the source of this information and learn more about the process on the following link: [Cloning a Repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

Back to the [Tables of Contents](#tables-of-contents)

---

## Credits

### Acknowledgements

Thank you to the following people who helped with support, inspiration and guidance at different stages in the project:

  * My mentor [Caleb Mbakwe](https://www.linkedin.com/in/calebmbakwe/?originalSubdomain=ng)
  * [Tim Nelson](https://github.com/TravelTimN) whom I inspired to organize the project and the README file.
  * Code Institute Mentors and Tutors.
  * Code Institute Student Care, which is always Kind.
  * My class on slack.
  * The supportive Code Institute community on Slack.
  * My family and friends for their patience and honest critique throughout.
