# InfoSecProject

pip install -r requirements.txt
Run api.py and open index.html in a browser.

We build a webapp that can be used as a secret-safe for users.
Users can use a name and a password for a secret.
This secret will then be saved in a SQLlite DB and can then be retrieved from the users with the initial name and password.

After building the app we started looking on the procedures with a more information security centered view. We found two options to make the user data more safe.

1. It is easy to use sql injection to access the secrets of users without knowing their credentials
by simply using " ' OR 'x'='x " into the input fields the secrets will be revealed

We implemented a way to secure the app from this. Instead of concatenating the SQL query with strings and then executing it separtely we use the function of of SQLlite to form the query and simply add a tuple of our paramters into it.

c.execute("INSERT INTO user2 (id,name,secret) VALUES (1,?,?)",(name,secretEncrypted))

With this the a potential sql injection can be prevented since the sqllite function is only allowing the parameters without addiontal symbols.


2. The Database inlcuding our secrets could possibly attacked and the secrets could be revealed since we just inserted the secrets as text into the DB.
To prevent this we switched our approach of saving the passwords on the Database and started encrypting the secrets using the passwords. With this only ecrypted secrets were in the database which would then need the initial password to be decyrpted and therefore revealed. 

To compare the before and after version we included both in this repo: new--> api.py  and old --> old_api.py
