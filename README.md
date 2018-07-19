# "News" Web-Application on Django 2.0 with AJAX

There you can find the The Register/Login/Logout User view, category page with their articles and many other things which user can do with them

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You should install python of the 3rd version;
pip for python3 with one of the latest version;
create a virtual environment for python or you can just upload ma github repository to your local machine;
install the libraries in *requirements.txt* using pip3.

## What you can do there?

#### User

You can: 

* Register new user using **/account/register/** uri 
* Login User using **/account/login/** uri
* Logout User using **/account/logout/** uri
* View user profile using **/account/<user_id>/** uri. 
  * You can find user id in Database or in python3 manage.py shell

_How I did it and other things + urls you can find in repository [accounts/](https://github.com/jaselnik/WebNews-with-DJANO-AJAX/tree/master/accounts)_

#### Category

You can: 

* Create a category in django admin panel using **/admin/** uri 
* View category detail with articles related to this category using **/<category_slug>/** uri. 
  * You can find category slug in django Database or using python3 manage.py shell. Also you can see the list of the all category with their links on the top of home page with **/** uri

_How I did it and other things + urls you can find in repository [mainapp/](https://github.com/jaselnik/WebNews-with-DJANO-AJAX/tree/master/mainapp)_

#### Article

You can: 

* Create an article using **/<category_slug>/** uri.
* Create an article in django admin panel using **/admin/** uri
* View the article detail using **/<category_slug>/<artilce_slug>/** uri. 
  * (you can find the article slug in th Database or using python3 manage.py shell. Also you can see the list of the all articles related to category with their links content block on category-detail page **/<category_slug>/** uri)
* Like or Dislike the article using **/<category_slug>/<artilce_slug>/** uri below the article content with Ajax JavaScrpt on FrontEnd.
* Comment the article using **/<category_slug>/<artilce_slug>/** uri below the article content with Ajax JavaScrpt on FrontEnd.
* Like or Dislike the comment using **/<category_slug>/<artilce_slug>/** uri below the article content with Ajax JavaScrpt on FrontEnd.
* Repost the article using **/<category_slug>/<artilce_slug>/** uri below the article content with Ajax JavaScrpt on FrontEnd.
  * All the reposts you can find on your profile page using **/account/<user_id>/**. Also you can Like or Dislike User Reposts there

_How I did it and other things + urls you can find in repository [mainapp/](https://github.com/jaselnik/WebNews-with-DJANO-AJAX/tree/master/mainapp)_

### Installing

A step by step series of examples that tell you how to get a development env running

If you have no python3 on your local machine yet you should type this command

```commandline
sudo apt-get install python3.6
```

If you have no pip3 for python3 on your local machine yet you should type this command

```commandline
sudo apt-get install python3-pip
```

Now you should install virtualenv using this command

```commandline
sudo pip3 install virtualenv
```

Create a new local repository on your machine for your project and go into this repo

```commandline
mkdir NewDjangoApp
```

```commandline
cd mkdir/
```

Install a GIT on your local machine and the other commands below to upload a my github repositoy

```commandline
sudo apt-get install git-core
```

```commandline
git init
```
```commandline
git remote add origin https://github.com/jaselnik/WebNews-with-DJANO-AJAX.git
```

I have two branches of my application there, so you can download master-branch or develop-branch using one of the commands below

```commandline
git pull origin master
```

```commandline
git pull origin develop
```

Create virtual environment using those command and actiavate it or just activate my using the 2nd command 

```commandline
virtualenv venv
```

```commandline
source venv/bin/activate
```

Install all the libraries to use this application

```commandline
pip3 install -r requirements.txt
```

That's it. Run the Django-application and try it yourself

```commandline
python3 manage.py runserver
```

## Authors

* **Denis Tamkovich** - On a GITHUB [jaselnik](https://github.com/PurpleBooth)

## My other links

* [Denis Tamkovich](https://www.linkedin.com/in/jaselnik/) - LinkedIn
* [Denis Tamkovich](https://www.facebook.com/jaselnik) - Facebook
* [Denis Tamkovich](https://vk.com/jaselnik) - VK

## Used

* [Django](https://www.djangoproject.com/) - The web framework used
