Please check out develop branch
```
git checkout -b develop origin/develop
```

Init database
```
from app import db
db.create_all()
```

# rest-api-development

CS5331 Assignment 1 Project Reference Repository

## Screenshots

Please replace the example screenshots with screenshots of your completed
project. Feel free to include more than one.

![Sample Screenshot](./img/samplescreenshot.png)

## Administration and Evaluation

Please fill out this section with details relevant to your team.

### Team Members

1.Cai Guoyuan Aaron
2.Jin Tianma
3.Rakkappan Lakshmanan
4.Sun Zelun

### Short Answer Questions

#### Question 1: Briefly describe the web technology stack used in your implementation.

Answer: 
Backend:

1. Python+Flask
2. Sqlite3
3. flask-sqlalchemy for database interaction / ORM
4. marshmallow-sqlalchemy for input validation
5. bcrypt for password hashing

Frontend:
1. JavaScript
2. HTML
3. Bootstrap 4

#### Question 2: Are there any security considerations your team thought about?

Answer: Please replace this sentence with your answer.

#### Question 3: Are there any improvements you would make to the API specification to improve the security of the web application?

Answer: Set timer for token expiry date

#### Question 4: Are there any additional features you would like to highlight?

Answer: Please replace this sentence with your answer.

#### Question 5: Is your web application vulnerable? If yes, how and why? If not, what measures did you take to secure it?

Answer: Please replace this sentence with your answer.

#### Feedback: Is there any other feedback you would like to give?

Answer: Please replace this sentence with your answer.

### Declaration

#### Please declare your individual contributions to the assignment:

1. Member 1 Name
    - Integrated feature x into component y
    - Implemented z
2. Member 2 Name
    - Wrote the front-end code
3. Member 3 Name
    - Designed the database schema
4. Member 4 Name
    - Implemented x

