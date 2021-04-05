# The Unknown-name game solver
This is a game i've played multiple times thats quite easy to play, but i find it impossible to solve..
What it's named i dont know and have not found out 

## Gameplay
It's game board is formed as a pluss sign with holes that can contain sticks.
In the initial board layout all holes without the center-most hole is fitted with a stick
like show'n here:
```
      I I I
      I I I
      I I I
I I I I I I I I I
I I I I O I I I I
I I I I I I I I I
      I I I
      I I I
      I I I
```
To play the game you take a stick and move it to a free hole, the stick can only be moved up/down or left/right and
MUST jump over another stick to get there. The stick you jumped over is then removed from the board resulting in a new free hole.
ex. here: 
```
input:  I I I I 0 I I I I
move:       |>>>^

output: I I O O I I I I I
```

This moving goes on until you only have ONE stick left on the board
And then the game ends.

## Soloving
I've never managed to solve this, but it SHOULD be possible to do. 

In the eager to getting this solved i've tried to create a game solver for this, 
As for now this is a non-optimized solover example that should be able to solve this. but as its not optimized it will take ages...
there are issues with it, and its not quite "testable"

Any input on bettering the performance of this is gladly welcome :)
