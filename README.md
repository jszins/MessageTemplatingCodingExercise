# MessageTemplatingCodingExercise
## Instructions: 
```
To run, download or clone the repo and change to the directory in a terminal.
Type 'python3 Main.py' to start the program. Follow on-screen instructions 
to create either a pre-templated message or create a new message template based on JSON data. 
```
## Overview of Design:
```
My decisions on the design of this exercise were predicated on OOP principles. I wanted to create
classes that would encapsulate all of the JSON data provided to me: Guest.py, Reservation.py, Message.py, and Company.py
```
```
I wanted to avoid a bloated Main program, so I created the class MessageService, and the file JsonOperations; MessageService helps to do
this as it takes all the user input through the use of helper functions, while JsonOperations loads all of the JSON provided into dictionaries used by helper functions. Python doesn't have proper private functions, but the functions meant to be private are prefixed with an underscore, and will be hidden from internal documentation. My focus was to use objects to do the work I wanted to get done.
```
## Language:
```
I've been preparing my Python skills a lot since looking formally for a career, since it's more flexible than C# (which is my second best language). It made sense then, since it's the language I'm using the most.
```
## Verification:
```
Not only did I walk through each step as myself, I tried to walk through each step as someone that isn't as well-versed as a developer and think about what kind of errors they made. I also try to make it a habit to use try/except blocks where I can, and whenever there's an input I expect, to test that input to make sure it conforms.
```
## What more would I like to do:
```
I'd like to make it more truly dynamic, or at least give the user more ways to enter in that information. I'd also like to add tests, as well as better exception handling to print more helpful messages. I would've liked to include a GUI, but it made sense to create a console application for what I needed. Finally, I would've liked to include a way to save message templates for future use. 
```