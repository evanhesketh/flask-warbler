# Warbler
Social media application

Deployed at: https://evanhesketh-warbler.onrender.com/

**username: guest** <br>
**password: guestpw**

## Local setup
1. Create virtual environment and activate.

    ``` 
    python3 -m venv venv  
    source venv/bin/activate
    ```

2. Install dependencies.

    ```
    pip3 install -r requirements.txt
    ```

3. Run app, view at http://localhost:5000/ or http://localhost:5001/
    ```
    python3 -m flask run -p 5000 (or 5001 if on newer mac)
    ```
## Tests
To run tests in top level directory:
```
python3 -m unittest
```


