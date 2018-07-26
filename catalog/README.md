# Item Catalog

> Alan Grinberg

## About

My Item Catalog project is a simple full stack application that stores a list of items associated with a variety of categories. User authentication makes sure nobody can mess around with the data without being authorized.

To view the categories or items in the database the user doesn't need to be logged in. However users who created an item are the only users allowed to update or delete the item that they created.

## Languages/Skills

- Python
- HTML
- CSS
- Flask
- Jinja2
- SQLAchemy
- Google OAuth2 and login

## Requirements

- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Getting Started

- Install Vagrant and VirtualBox
- Clone the Vagrantfile
- Clone this repo into the vagrant directory
- Run `vagrant up` and then `vagrant ssh` to start up the VM
- From the catalog-project directory run `sudo pip install -r requirements`
- run application using `python catalog/application.py`
- go to `http://localhost/8000` on your browser to run the application

## Known issues

- TBD

## Potential improvements

- Prep for live usage - specific users with their specific items
- pictures for items
- Styling of the application with bootstrap
- Facebook auth