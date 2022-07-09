# Chess-Player
This Python Program takes chess steps as input and plays chess from both sides following those steps. The inputed steps needs to follow the chess notation rules.

This Program can work on any chess platform like (lichess.org)[https://lichess.org/], (Chess.com)[https://www.chess.com/], etc.

# Disclaimer
I DO NOT promote any kind of cheating in any way. This project is completely for learning experience and is not meant to be misused for cheating on any chess platforms/competitions.

# Technologies Used
### Programming Language
Python

### Python Modules
1. Pyautogui

2. OpenCV-Python

3. Numpy

# How to run it
1. Install Python 3
2. Install required python modules by entering below command in Terminal
```bash
pip install pyautogui opencv-python numpy
```
3. Open a web browser and go to your desired chess website. Now, open a new incognito tab in that browser and open the same chess website in it.
4. Select the option to Play with Friend and create a match and join the match from another window (as it is the only way you can control both sides of game) 
5. Arrange both the windows side by side as shown below.

![image](https://user-images.githubusercontent.com/77500668/178124186-5d42f6e6-2dde-4791-8193-afe9587b65d8.png)

6. Now, Take screenshot of the chess board for the white player and save the image in res folder as "white_board.png". Your image should look something like this.

      ![image](https://user-images.githubusercontent.com/77500668/178124237-9c969a5e-4c9c-4893-8fba-d46d2e7a4581.png)
  
7. Do the same for black player chess board and save the image in res folder as "black_board.png". Your image should look like this
  
      ![image](https://user-images.githubusercontent.com/77500668/178124220-bb98cb60-d2c8-47b9-96b0-2b4cd33ea643.png)

8. Finally, we are ready to run the program. Now, enter the chess steps (following chess notations) in "input.txt"

   Example Input:
   ```
   1. e4 e5 2. Nf3 Nf6 3. Nxe5 d6 4. Nf3 Nxe4 5. d4 d5 6. Bd3 Bd6 7. 0-0 0-0 8. c4 c6 9. Re1 Bf5 10. Qb3 Qd7 11. Nc3 Nxc3 12. Bxf5 Qxf5 13. bxc3 b6 14. cxd5 cxd5 15. Qb5 Qd7 16. a4 Qxb5 17. axb5 a5 18. Nh4 (diagram) g6 19. g4 Nd7 20. Ng2 Rfc8 21. Bf4 Bxf4 22. Nxf4 Rxc3 23. Nxd5 Rd3 24. Re7 Nf8 25. Nf6+ Kg7 26. Ne8+ Kg8 27. d5 a4 28. Nf6+ Kg7 29. g5 a3 30. Ne8+ Kg8 31. Nf6+ Kg7 32. Ne8+ Kg8
   ```
   Kindly note that each step should be space seperated from each other and there should be space between the step counting and the steps.
   You can find such more input [here](https://thechesspedia.net/world-championship-matches/)
   
9. Now go ahead and run the "play.py" file. There is a 5 second buffer time for you to minimize all other windows or switch to the workspace in which your chess windows are setuped.

# Limitations & Bugs
1. The bot fails in case of Pawn Promotion

