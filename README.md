# risksense_api_examples

## Generating an API token

Log in to RiskSense.  If you are a multi-client, user, select one of your clients (it doesn't matter which one).
* On the top right corner of the window, click the three vertical dots to open the menu.
* Select 'User Settings'
* In the user settings page that opens up, locate the second section on the page labeled 'API TOKENS'.  This is the 
section where you can create and revoke API tokens for your user.
* Click the 'Generate' button to generate a new API token.  You will be required to give it a name.  This token
will only be displayed once, so copy and paste it to a safe location for storage.

This token can now be used to interact with the RiskSense REST API.  It will have the same permissions as the user 
that created it.  This means that it can access the same clients, networks, groups, tags, etc.