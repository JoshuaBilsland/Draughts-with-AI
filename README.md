# Draughts-with-AI
This is my project for my NEA for A-level Computer Science. I had already started this project before making this repository but because of large breaks, due to other schoolwork, I needed to go over what I had done already. I have decided to use Git and GitHub so I can upload each file after reading back through it. From now on, I will be able to use Git to track changes over time and use commit messages to remind me about what I was doing when I last added to the project.

---

## The Project
My project is to make a draughts game, which is split into two halves. Some brief information can be seen below but full documents containing designs and further information will be attached when I have finished with them. I will also be carrying out testing at the end of the project, which will also be attached at a later date. 

### First Half - User Accounts
The first half of the project (and the part I will be working on first) is do with user accounts. This involves creating a database, tables, allowing users to make accounts, sign into those accounts, sign out of them, view the stats stored about their accounts, etc. Two 'account slot' objects will be created which store a dictionary of data from the database. This data will be things such as username, total number of games played against an AI, total number of games played against other players, total number of wins against AI, etc. The different subroutines that make up the program will be able to use the object's methods to retreive or edit the values stored. These changes to the slots will automattically be made to the database as well. For example, when a player finishes playing a game against the AI and wins, the total number of games played against the AI and the total number of wins against an AI will be incremented by 1 in the object's dictionary of data. Those same columns in the database will also be incremented by 1 for the account that is signed into the account slot object. 

### Second Half - The Game
The second half of the game is the draughts game itself. Users will be able to choose if they want to play against an AI or against another player. The game will be carried out and their account stats will be updated (in the slot object that their accounts are signed into, and then in the database) at the end of the game. The game will let user's choose the colour they want to be, choose the difficulty of the AI, etc. 
