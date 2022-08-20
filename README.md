# Specialization
#### Description: A website That allows students From Egypt to choose their high school studying preferences.


Technologies used:

<div style="display:flex;gap:200px">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" alt="CSS" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" alt="JavaScript" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python 3" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" alt="Sqlite 3" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" alt="Flask" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" alt="Git" height="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" height="50">
</div>



The Idea Behind it:

    In Egypt Students entering grade 11 have to write on a paper what speciality of studying they want and go to school to give it to the headmaster,
    Then Teachers across the country would spend enormous amount of time and energy to list every student's preferences and their number and name.
    which will cause a lot of problems as humans aren't perfect.

    I decided to take on initiative and implement a fully functional web site that allows students from all over Egypt to safely register with their national id so they can choose their studying specialities.

Functionality:

    - Adding Students to Database

    - Making Sure there are no duplicate Students in the database
        - it uses the national id to make sure that no duplication occurs andd gives error if user tries to register again

    - It has robust error checking to make sure that all data entererd is correct.
        - it uses Regular Expressions to check That national IDs are correct.
            - Please Note: it can be easily forged as i dont check against any database and only check for the syntax.
        - Regular Expressions are also used for passwords to make sure they are strong enough.
            - have a number and at least 8 charachters long.
        - Names are also checked using Regular Expressions to make sure that the user provided a right name.
            - The format is the same as The format on the ID card which is 3 Names in Arabic.
        - The app also protects against anyone trying to enter forged Data in grade or specialization using Developer tools.

    - It Manipulates the sqlite3 database Using Class Called student which has the following methods
        - Instance Function (Requires creating an instance as it takes self as an argument)
            - add
                - Adds the constructed student instance to the database.
        - Class Function (Doesn't Require creating an instance)
            
            Depends on the user id stored in the session which resemples the student's unique id in the database which allows for blazingly fast retrivals of data.

            - isexist
                - which checks if a student was already in the database and returns the id of the student if he does exist otherwise returns False
            - delete
                - Deletes a student from the database and returns a string stating whether or not the operation was succesful.
            - edit
                - edits the specified student'data with the new data provided.
            - fetch
                - graps the user's (name, grade, specialization) from the database
            - fetch_name
                - graps the user's name from the database

How it works:

    - helpers folder which has 2 files:
        - student.py where Most of the Functionality is in: 
            - it houses the student class which is used in 
                1- Validating the user's input.
                2- Adding a student to the dataase.
                3- Deleting a student From the database.
                4- Checking if a student is in the database.
                    side note:
                        O(N) Algoraithm which can be slow when number of student grows
                        a better Algoraithm would be binary search but that would require
                        storing the national ids as plain text or any reversable form which
                        can be a security problem.
                5- Graps User's Data from the database.

        - myFunctions.py which houses 2 simple functions 
                1- fetch_as_dict
                    - used in student.py to fetch results of a database query in the form of dictionaries
                2- give_output
                    - used alot in student.py and app.py to output a message of either success or failure to the user
                3- login_required
                    - wrapper function to make sure a student is logged before visiting a specific page.
                4- translate
                    - translates the single letter alphanumerics represnting the student's data to Arabic readable text understandable by humans.
