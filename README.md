# Warbler
Social media application where users can register to post messages, follow other users, like other user's posts, and get a personalized feed of posts from followed users

Deployed at: https://evanhesketh-warbler.onrender.com/

**username: guest** <br>
**password: guestpw**

## Local setup
1. Create virtual environment and activate

    ``` 
    python3 -m venv venv  
    source venv/bin/activate
    ```

2. Install dependencies

    ```
    pip3 install -r requirements.txt
    ```
3. Create a new PostgreSQL database
   ```
   createdb warbler
   ```
4. Create a file named .env and add:
   ```
   SECRET_KEY=*choose a secret key*
   DATABASE_URL=postgresql:///warbler
   ```
5. Seed the database
   ```
   python3 seed.py
   ```

7. Run app, view at http://localhost:5000/ or http://localhost:5001/
    ```
    python3 -m flask run -p 5000 (or 5001 if on newer mac)
    ```
## Tests
Create a new PostgreSQL database for testing:
```
createdb warbler_test
```

To run tests in top level directory:
```
python3 -m unittest
```


