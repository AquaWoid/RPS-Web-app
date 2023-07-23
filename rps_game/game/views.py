from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import GameScore
from .forms import RegistrationForm
import random



#Login View
def user_login_view(request):

    #Checking if the request method is POST
    if request.method == "POST":
        action = request.POST.get("action")

        #If the request action is "login" we ask for the username and password for further authentification using the authenticate function
        if action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            #If the ause if authenticated we proceed to the game
            if user is not None:
                login(request, user)
                return redirect("game:game")  
            #Else an error message is thrown
            else:
                return render(request, "login/login.html", {"error_message": "Invalid username or password"})

        #Registering using the default Registration Form
        elif action == "register":
            registration_form = RegistrationForm(request.POST)
            print(registration_form.data)
            if registration_form.is_valid():
                print("Reg valid")
                registration_form.save()
                return render(request, "login/login.html", {"success_message": "Successfully registered your account"})
            else:
                print("Registration invalid")

            return render(request, "login/login.html", {"registration_form": registration_form})

    else:
        registration_form = RegistrationForm()
        return render(request, "login/login.html", {"registration_form": registration_form})


#View of the main game
def game_view(request):

    #Declaring a user instance and the choices for the game. I had to get the user like this otherwise i would get instance errors.
    user_instance = User.objects.get(pk = request.user.pk)
    choices = ["Rock", "Paper", "Scissors"]


    if request.method == "POST":

        #Simple game logic which is pretty much self explanatory when being looked at
        user_choice = request.POST.get("user_choice")
        computer_choice = random.choice(choices)
        
        user_wins = False

        if(user_choice == "Rock" and computer_choice == "Scissors"):
            user_wins = True
        if(user_choice == "Paper" and computer_choice == "Rock"):
            user_wins = True
        if(user_choice == "Scissors" and computer_choice == "Paper"):
            user_wins = True            
            

        if user_wins == True:

            #Debug Prints
            print("Player Won")
            print(f"Username :{request.user} User type = {type(request.user)}")

            #Here i also had to get the Score objects like this, otherwise Django would throw type errors at me
            try:
                user_score = GameScore.objects.get(user=user_instance)
            except:
                user_score = GameScore.objects.create(user=user_instance)

            #Saving the scores to the database
            user_score.score += 1
            user_score.total_wins += 1

            if user_score.score > user_score.highest_streak:
                user_score.highest_streak = user_score.score

            user_score.save()



            #Returning all score results to the frontend
            return render(request, "game/game.html", {"result_message": "Player Won", "current_score" : str(user_score.score), "highest_streak" : str(user_score.highest_streak)
                                                      , "total_wins" : str(user_score.total_wins)})
       
       #Same procedure in case the player loses the game
        else:


            try:
                user_score = GameScore.objects.get(user=user_instance)
            except:
                user_score = GameScore.objects.create(user=user_instance)

            if user_score.highest_streak < user_score.score:
                user_score.highest_streak = user_score.score

            user_score.score = 0
            user_score.save()
            print("Player Lost")
            return render(request, "game/game.html", {"result_message": "Player Lost", "current_score" : str(user_score.score), "highest_streak" : str(user_score.highest_streak)
                                                      , "total_wins" : str(user_score.total_wins)})         


    #Another reference to the score class for displaying outside of the game
    user_score = GameScore.objects.get_or_create(user=request.user)[0]

    return render(request, "game/game.html", {"result_message": "Player Won", "current_score" : str(user_score.score), "highest_streak" : str(user_score.highest_streak)
     , "total_wins" : str(user_score.total_wins)})     


#Simple highscore tracking, displaying the top 10 results
def highscore_view(request):
    highest_streak_users = GameScore.objects.order_by("-highest_streak")[:10]
    total_wins_users = GameScore.objects.order_by("-total_wins")[:10]
    return render(request, "highscore/highscore.html", {"highest_streak_users": highest_streak_users, "total_wins_users": total_wins_users})