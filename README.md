# risksense_api_examples
This repository is intended to provide some examples of how users can interact with the RiskSense REST API to 
retrieve information from, and perform operations on, the RiskSense platform.  

Currently, all examples are provided using the Python (v3.7) programming language, and leverage an available Python
module called 'Requests'.  You can install this using `pip`.

* To install: `pip install requests`

Additionally, the 'TOML' module is used for the configuration file, and can also be installed using `pip`.

* To install: `pip install toml`


## Generating an API token

Log in to RiskSense.  If you are a multi-client, user, select one of your clients (it doesn't matter which one).
* On the top right corner of the window, click the three vertical dots to open the menu.
  
  ![Menu Location](https://github.com/risksense/risksense_api_examples/blob/master/readme_images/menu_location.png)

* Select 'User Settings'
  
  ![User Settings](https://github.com/risksense/risksense_api_examples/blob/master/readme_images/user_settings_menu.png)

* In the user settings page that opens up, locate the second section on the page labeled 'API TOKENS'.  This is the 
section where you can create and revoke API tokens for your user.
  
  ![API TOKEN](https://github.com/risksense/risksense_api_examples/blob/master/readme_images/generate.PNG)

* Click the 'Generate' button to generate a new API token.  You will be required to give it a name.  This token
will only be displayed once, so copy and paste it to a safe location for storage.

This token can now be used to interact with the RiskSense REST API.  It will have the same permissions as the user 
that created it.  This means that it can access the same clients, networks, groups, tags, etc.
