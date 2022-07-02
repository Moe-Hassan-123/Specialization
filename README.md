# Specialization - CS50's Final Project
#### Video Demo: https://youtu.be/KKqSAOAaoq0
#### Description: A website That allows students From Egypt to choose their high school studying preferences.

Technologies used:

<div style="display:flex;gap:200px">
    <img src="images/HTML.png" alt="HTML" width="100"/>
    <img src="images/CSS.png" alt="CSS" width="100"/>
    <img src="images/JavaScript.png" alt="JavaScript" width="100"/>
    <img src="images/Python.png" alt="Python 3" width="100"/>
    <img src="images/Sqlite3.png" alt="Sqlite 3" width="100"/>
    <img src="images/Flask.png" alt="Flask" width="100"/>
</div>


The Idea Behind it:

    In Egypt Students entering grade 11 have to write on a paper what speciality of studying they want and go to school to give it to the headmaster,
    Then Teachers across the country would spend enormous amount of time and energy to list every student's preferences and their number and name.
    which as any sensible human knows, will cause a lot of problems as humans aren't perfect.

    So I with my newfound savvy programming skills decided to take on initiative and implemented a fully functional web site that allows students from all over Egypt to safely
    register with their national id so they can choose their studying specialities.

Functionality:

    - Adding Students to Database

    - Making Sure there are no duplicate Students in the database
        - it uses the national id to make sure that no duplication occurs andd gives error if user tries to register again

    - It has robust error checking to make sure that all data entererd is correct.
        - it uses Regular Expressions to check That national IDs are correct.
            - Please Note: it can be easily forged as i dont check against any database and only check for the syntax.
        - Regular Expressions are also used for passwords to make sure they are strong enough.
            - have a capital letter, small letter and a number and at least 8 charachters long.
        - Names are also checked using Regular Expressions to make sure that the user provided a right name.
            - The format is the same as The format on the ID card which is 3 Names in Arabic (Not English)
        - The app also checks if anyone tried to enter Data in grade or specialization using Developer tools

    - It Manipulates the database students.db Using Class Called student which has the following methods
        - Instance Function (Requires creating an instance as it takes self as an argument)
            - add
                - Adds the student to the database
        - Class Function (Doesn't Require creating an instance)
            - isexist
                - which checks if a student was already in the database and returns the id of the student if he does exist otherwise returns False
            - delete
                - Deletes a student from the database and returns a string stating whether or not the operation was succesful.

How it works:

    - helpers Folder :-
        - student.py where Most of the Functionality is in: 
            - it houses the student class which is used in 
                1- Validating the input
                2- Adding a student to the database
                3- Deleting a student From the database
                4- Checking if a student is in the database

        - myFunctions.py which houses 2 simple functions 
                1- fetch_as_dict
                    - used in student.py to fetch results of a database query in the form of dictionaries
                2- give_output
                    - used alot in student.py and app.py to output a message of either success or failure to the user
