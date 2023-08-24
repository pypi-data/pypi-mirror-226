import random

#def rockgame():
user_sr = 0
pc_sr = 0
c = True

while c:
    choice = input("Enter a word from -> (rock,paper,scissors) , To Exit enter (x): ")
    rand = random.randrange(1,4)
    
    if choice == "x": 
        c = False
        if user_sr > pc_sr: print("|                                                               |\n\
|________________________*** YOU WIN ***________________________|\n\
|____________Your score "+str(pc_sr)+"______________Computer's score "+str(user_sr)+"_______|\n\
|__________________Designed by AMMAR ALHASHEMI__________________|\n\
|_______________________________________________________________|\n")
        elif pc_sr > user_sr: print("|                                                               |\n\
|____________________________YOU LOSE___________________________|\n\
|____________Your score "+str(pc_sr)+"______________Computer's score "+str(user_sr)+"_______|\n\
|__________________Designed by AMMAR ALHASHEMI__________________|\n\
|_______________________________________________________________|\n")
        else: print("|                                                               |\n\
|______________________________Draw_____________________________|\n\
|____________Your score "+str(pc_sr)+"______________Computer's score "+str(user_sr)+"_______|\n\
|__________________Designed by AMMAR ALHASHEMI__________________|\n\
|_______________________________________________________________|\n")
    else:
        if rand == 1: 
            pc_choice="rock"
        if rand == 2: 
            pc_choice="paper"
        if rand == 3: 
            pc_choice="scissors"

        if choice == "rock" or choice == "paper" or choice == "scissors":
            print("You chosed ("+choice+"), computer chosed ("+pc_choice+").")
            if choice == pc_choice:
                print("\nDraw YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
            elif choice == "rock" and pc_choice == "paper":
                pc_sr+=1
                print("paper cover rock! Computer scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(str(pc_sr))+"\n")
            elif choice == "rock" and pc_choice == "scissors":
                user_sr+=1
                print("rock smash Sicssors! You scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
            elif choice == "paper" and pc_choice == "rock":
                user_sr+=1
                print("paper cover rock! You scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
            elif choice == "paper" and pc_choice == "scissors":
                pc_sr+=1
                print("Sicssors cut paper! Computer scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
            elif choice == "scissors" and pc_choice == "rock":
                pc_sr+=1
                print("rock smash Sicssors! Computer scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
            elif choice == "scissors" and pc_choice == "paper":
                user_sr+=1
                print("Sicssors cut paper! You scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
            print("##################################")
        else:
            print("you enterd wrong choice")