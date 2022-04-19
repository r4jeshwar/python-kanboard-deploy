# python-kanboard-deploy

### The development of this project has moved to https://github.com/r4jeshwar/nornir-kanboard-deploy

# Introduction
Kanboard is a project management open source software application that uses a Kanban board to implement the Kanban process management system.
This repository is an attempt at writing a pure python implementation of a script to deploy **kanboard** as well as it's dependant components, such as **mariadb, httpd**, etc.

# Installation
`Step 1:` Clone the repository.

`Step 2:` pip -r requirements.txt

`Step 3:` Export environment variables 
```
export PASSWORD=<password>
export CONFIRM_PASS=<re-enter_password>
export URL=<url>
```

`Step 4:` ~~For security purposes, remember to modify admin's password using the users management link from the upper right-hand admin drop-down menu~~ This is being currently handled by the playwright library.
    
    

  
