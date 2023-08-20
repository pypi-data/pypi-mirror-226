import random

def rockgame():
    user_sr = 0
    pc_sr = 0
    c = True

    while c:
        choice = input("Enter a choice from -> (Rock,Paper,Scissors) , To Exit enter (X): ")
        rand = random.randrange(1,3)
        
        if choice == "X": 
            c = False
            print("____Game ended!____\n_Designed by AMMAR_")
        else:
            if rand == 1: 
                pc_choice="Rock"
            if rand == 2: 
                pc_choice="Paper"
            if rand == 3: 
                pc_choice="Scissors"

            if choice == "Rock" or choice == "Paper" or choice == "Scissors":
                print("You chosed ("+choice+"), computer chosed ("+pc_choice+").")
                if choice == pc_choice:
                    print("\nDraw YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
                elif choice == "Rock" and pc_choice == "Paper":
                    pc_sr+=1
                    print("Paper cover Rock! Computer scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(str(pc_sr))+"\n")
                elif choice == "Rock" and pc_choice == "Scissors":
                    user_sr+=1
                    print("Rock smash Sicssors! You scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
                elif choice == "Paper" and pc_choice == "Rock":
                    user_sr+=1
                    print("Paper cover Rock! You scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
                elif choice == "Paper" and pc_choice == "Scissors":
                    pc_sr+=1
                    print("Sicssors cut Paper! Computer scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
                elif choice == "Scissors" and pc_choice == "Rock":
                    pc_sr+=1
                    print("Rock smash Sicssors! Computer scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
                elif choice == "Scissors" and pc_choice == "Paper":
                    user_sr+=1
                    print("Sicssors cut Paper! You scored 1\n\n YOUR SCORE="+str(user_sr)+" , COMPUTER score="+str(pc_sr)+"\n")
                print("##################################")
            else:
                print("you enterd wrong choice")