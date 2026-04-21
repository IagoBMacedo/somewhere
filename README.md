\# Somewhere: A Procedurally Generated Driving Game

\#### Video Demo: https://www.youtube.com/watch?v=KhSC6wMVU0M



\#### Description: A 2D driving game where the player can control a car or a walking character through a procedurally generated city. The game features dynamic street scrolling, procedural building generation, and animated characters.



\## Features

\- Switch between driving a car and walking as a character

\- Animated car and player sprites

\- Procedural city buildings and scrolling streets

\- Car lights, wheel rotation, and character blinking animations

\- Keyboard controls for movement and interaction



\## How to Run



1\. Install Python 3

2\. Install Pygame:



```

pip install pygame

```



3\. Run:



```

python game.py

```



\## Controls



\- \*\*Move Forward / Accelerate:\*\* W

\- \*\*Move Backward / Brake:\*\* S

\- \*\*Move Left:\*\* A

\- \*\*Move Right:\*\* D

\- \*\*Enter / Exit Car:\*\* E

\- \*\*Toggle Car Lights:\*\* Q

\- \*\*Interact with Car:\*\* F



\## Motivation

I wanted to create a small game that combines animation systems, procedural generation, and interactive gameplay. The project allowed me to apply concepts learned in CS50 such as object-oriented programming, event handling, sprite animation, and modular code design.



The project also served as a way to explore how different game systems—such as environment generation, character animation, and player interaction—can work together in a cohesive structure.



\## Design Decisions



\### Object-Oriented Structure



As the project grew, it became clear that organizing the code into classes was essential. Initially, all logic was contained in a single file (`game.py`), which quickly became difficult to maintain. The project was later refactored into multiple files where each class is responsible for a specific system, such as cars, characters, terrain, and visual effects. This made the code significantly easier to read and extend.



\### Procedural Environment



Instead of manually placing buildings, the city environment is generated procedurally. This allows the game world to appear infinite while reusing a small number of assets. The buildings are generated based on window patterns, which ensures the structures remain visually consistent.



\### Animation Systems



Several small animation systems were implemented to improve visual feedback:



\- Rotating car wheels

\- Blinking characters

\- Car lights



Each animation runs independently from the main movement logic to keep the code modular and easy to adjust.



\### Frame-Independent Movement



Movement calculations use delta time (`dt`) so that object speeds remain consistent regardless of frame rate, ensuring the game behaves similarly on different hardware.





\## Challenges



The procedural buildings were hard to implement. Before the final version, I was trying to generate a random rectangle and then fill it with little squares (the windows). The buildings often looked weird because the math didn’t always match what I had in mind.



Everything became much easier once I realized I should reverse the process: first generate a random number of windows, and then build the rectangle around that structure. Designing from the inside out made the buildings look much more consistent.



Implementing blinking was also way harder than I expected. Because the character’s eye axis changes depending on movement and animation frame, I had to make sure blinking would not reset during animation while still dynamically following the character’s position.



To keep the code clean, I created a separate file just for blinking logic, while keeping the offsets inside the car and character classes. The `update\\\\\\\_blink` function runs once per frame and controls global blink timing, while `get\\\\\\\_eye\\\\\\\_draw\\\\\\\_rect` is executed dynamically depending on whether the player is in the car or on foot. This way, the blink pixel and offset are always positioned correctly.



Also, I learned that as the code grows, it becomes extremely important to keep things organized. I started writing the entire project in a single file, `game.py`, but as features were added, it quickly became messy and hard to manage. Refactoring the code into separate classes and files for each type of object made the project much cleaner and easier to maintain. This was one of the most important lessons I learned while building this game.

