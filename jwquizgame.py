import os
import time
import pygame
import threading
from random import shuffle
from rich.progress import Progress
from rich.align import Align
from rich.console import Console
from rich.live import Live
from assets.config.data.quiz_data import data
from JasonColors import jfGreen, jReset, jBold, jfRed, jfCyan, jfYellow, jRGBGradient, jfBBlue, jUnderline

# This Module ^ is from my other project, JasonColors, which is a module I created to make it easier to add colors and styles to the terminal output, it also has a function for creating RGB gradients, which I use for the title and the player rankings in this game. If you want to add some style to your terminal projects, feel free to check it out thanks :D


class JwQuizGame():

    def __init__(self):
        

        self.running = True
        pygame.mixer.init()

        # list the sounds I want to play in the background, they will loop until the game ends
        self.background_sounds= ["assets/sounds/background_1.wav", "assets/sounds/background_2.wav", "assets/sounds/background_3.mp3"]
        threading.Thread(target=self.background_music_loop, daemon=True).start()

        # preload the correct and wrong answer sounds
        self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")

        # check the os type and clear its contents the appropriate way, then show the loading screen with a progress bar
        os.system('cls' if os.name == 'nt' else 'clear')
        progress = Progress()
        task = progress.add_task("Loading...", total=150)


        # set the title of the game with a gradient effect and center it, then wait for 1 second before starting the game
        self.intro = self.set_title(self.gradient_centerer("}---------------------------[ JW QUIZ GAME ]---------------------------{", (198,189,20), (20,198,105), True), 0,)
        print('\n')


        with Live(Align.center(progress), refresh_per_second=10):
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(0.05)

        # determine the number of players, it must be between 1 and 25, if the user enters an invalid number, it will ask them to enter a valid number until they do
        self.num_of_players = self.check_int(jfGreen("Enter the number of players: ")+jReset(), 1, 25)
        print('\n\n')

        # initialize the player scores as an empty dictionary, the keys will be the player names and the values will be their scores
        self.player_scores = {}
    
        # shuffle the card data, the card data is a list of the keys of the data dictionary, which contains the questions and answers, this will ensure that the questions are random each time the game is played :)
        self.card_data = list(data.keys())
        shuffle(self.card_data)
    
    def check_int(self, question, start=0, stop='0'):

        # this function checks if the user input is a valid integer within the specified range, it will keep asking the user to enter a valid number until they do, it returns the valid integer entered by the user
        while True:
            answer = input(question)
            if stop == '0' and (str(answer).isdigit()) and (int(answer) >= start): #unlimited Max range of digit
                return(int(answer))
            elif stop != '0' and (str(answer).isdigit()) and (int(answer) >= start) and (int(answer) <= stop): #limited digits for Max range
                return(int(answer))
            else:
                print(jBold(jfRed("Incorrect, Enter a valid number.")))

    
    def set_title(self, text, duration=1):
        self.terminal_width = os.get_terminal_size().columns
        print(text.center(self.terminal_width))
        time.sleep(duration)
                    

    def gradient_centerer(self, text, start_rgb, end_rgb, bold=False, underline=False):
        gradient = jRGBGradient(text, start_rgb, end_rgb, bold, underline)
        width = os.get_terminal_size().columns
        padding = (width - len(text)) // 2
        return " " * padding + gradient

    def name_players(self):

        # loop through the number of players and ask for their names, then store their names in the player_scores dictionary with a score of 0, this will allow us to keep track of each player's score throughout the game
        print(jBold(jfRed('-'*40)))
        for i in range(self.num_of_players):
            name_of_players = input(jfCyan(f"Enter Player {i+1}'s Nickname: ")+jfYellow())
            self.player_scores[name_of_players] = 0
        print(jBold(jfRed('-'*40)))
        print('\n\n')
        
    # this function takes an integer n and returns the appropriate suffix for that integer (e.g., 'st' for 1, 'nd' for 2, 'rd' for 3, and 'th' for all other numbers), this is used to display the player rankings in a more readable format cause why not
    def get_suffix(self, n):
        if 11 <= n % 100 <= 13:
            return 'th'
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

    def winner_calc(self):

        # main function to calculate the winner of the game, it sorts the player_scores dictionary by score in descending order and then prints the rankings with a gradient effect, the top 3 players will have a special icon and color, the rest will be displayed in white, after displaying the rankings, it stops the background music and plays a victory sound, then waits for the user to press enter before ending the game
        ranked = sorted(self.player_scores.items(), key=lambda item: item[1], reverse=True)
        print('\n')
        self.set_title(jBold(jfRed('-'*50)), 0)
        print('\n')
        for i, (names, scores) in enumerate(ranked, start=1):
            base_ranks = f"{i}{self.get_suffix(i)}: {names} with {scores} points"
            if i == 1:
                icon = '🏆🥇 '
                styled_ranks = self.gradient_centerer(icon + base_ranks, (204,110,10),(204,155,10),True)
            elif i == 2:
                icon = '🥈 '
                styled_ranks = self.gradient_centerer(icon + base_ranks, (117,114,106),(245,241,228),True)
            elif i == 3:
                icon = '🥉 '
                styled_ranks = self.gradient_centerer(icon + base_ranks, (115,66,33),(169,113,76),True)
            elif i == 4:
                icon = '⭐ '
                styled_ranks = self.gradient_centerer(icon + base_ranks, (55,31,175),(84,19,127),True)
            else:
                styled_ranks = self.gradient_centerer(base_ranks,(255,255,255,), (255,255,255), True)
            print(styled_ranks)

        print('\n')
        self.set_title(jBold(jfRed('-'*50)), 0)
        channel.stop()
        pygame.mixer.Sound("assets/sounds/final_win.wav").play(-1)
        input()
        
    def background_music_loop(self):
        while self.running:
            for sound_file in self.background_sounds:
                if not self.running:
                    return
                sound = pygame.mixer.Sound(sound_file)
                global channel
                channel = sound.play()
                sound.set_volume(0.25)
                while self.running and channel.get_busy():
                    pygame.time.delay(100)

    def shutdown(self):
        # this function is used to stop the background music and quit the mixer when the game ends, it sets the running variable to False, which will cause the background_music_loop to exit, then it stops any currently playing sounds and quits the mixer to free up resources because it seems like quitting the regular way dosent free up the resources for some reason, so this is a workaround to ensure that the mixer is properly shut down when the game ends
        self.running = False
        pygame.mixer.stop()
        pygame.mixer.quit()

    def main_game(self):
    
        self.name_players()
        question_counter = 0
        number_of_rounds = (int(len(data.keys())) // (self.num_of_players))
        print(jBold(jfRed('-'*40)))
        temp_number_of_rounds = self.check_int(jfGreen(f"How many rounds do you want to play? {jfBBlue('1')} - {jfBBlue(f'{number_of_rounds}(maximum): ')}")+jReset(), 1, number_of_rounds)
        number_of_rounds = temp_number_of_rounds
        print(jBold(jfRed('-'*40)))
        print('\n\n')

        
        for rounds in range(number_of_rounds):
            self.intro = self.set_title(self.gradient_centerer(f"}}---------------------------[ ROUND {rounds+1} / {number_of_rounds} ]---------------------------{{", (198,189,20), (20,198,105), True), 1,)
            
            # loop through the players and ask them the questions, each player will get a turn to answer a question, the questions are stored in the card_data list, which is shuffled at the beginning of the game to ensure randomness, each question has 10 hints, the player can use as many hints as they want, but the more hints they use, the less points they will get for that question, if they guess the answer correctly, they get points based on how many hints they used, if they guess incorrectly, they lose points and move on to the next hint, if they use all 10 hints without guessing correctly, they get 0 points for that question
            for player in self.player_scores:
                max_score = 10
                current_question = self.card_data[question_counter]
                print(jBold(jfRed('-'*40)))
                print(jBold(jfBBlue(f"{str(player).capitalize()}'s Turn: ")))
                print(jBold(jfRed('-'*40)))
                print('\n')
                print('            ', end='')
                print(jBold(jUnderline('?'+jReset())))

                # loop through the hints for the current question, the hints are stored in the data dictionary with the question key, the first element of the list is the answer, and the next 10 elements are the hints, if the player guesses the answer correctly, they get points based on how many hints they used, if they guess incorrectly, they lose points and move on to the next hint, if they use all 10 hints without guessing correctly, they get 0 points for that question
                for i in range(1, 11):
                    guess = input(jRGBGradient(f"{data[int(current_question)][i]}: ", (0,120,255),(255,80,80))+jfGreen())
                    if guess.lower() == str(data[int(current_question)][0]).lower():
                        self.player_scores[player] += max_score
                        question_counter += 1
                        print(jBold(jfGreen("\nCorrect!\n")))
                        self.correct_sound.play()
                        time.sleep(1)
                        break
                    print(jBold(jfRed("Incorrect, next hint..")))
                    max_score -= 1
                    self.wrong_sound.play()
                    
        self.winner_calc()


if __name__ == '__main__':
    JwQuizGame().main_game()