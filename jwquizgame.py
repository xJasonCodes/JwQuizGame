import os
import time
import pygame
import threading
from JasonColors import jfGreen, jReset, jBold, jfRed, jfCyan, jfYellow, jRGBGradient, jfBBlue, jUnderline
from random import shuffle
from rich.progress import Progress
from rich.align import Align
from rich.console import Console
from rich.live import Live
from assets.config.data.quiz_data import data


class JwQuizGame():

    def __init__(self):
        

        self.running = True
        pygame.mixer.init()
        self.background_sounds= ["assets/sounds/background_1.wav", "assets/sounds/background_2.wav", "assets/sounds/background_3.mp3"]
        threading.Thread(target=self.background_music_loop, daemon=True).start()

        self.correct_sound = pygame.mixer.Sound("assets/sounds/correct.wav")
        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.wav")

        os.system('cls' if os.name == 'nt' else 'clear')
        progress = Progress()
        task = progress.add_task("Loading...", total=150)



        self.intro = self.set_title(self.gradient_centerer("}---------------------------[ JW QUIZ GAME ]---------------------------{", (198,189,20), (20,198,105), True), 0,)
        print('\n')


        with Live(Align.center(progress), refresh_per_second=10):
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(0.05)

        self.num_of_players = self.check_int(jfGreen("Enter the number of players: ")+jReset(), 1, 25)
        print('\n\n')
        self.player_scores = {}
    

        self.card_data = list(data.keys())
        shuffle(self.card_data)
    
    def check_int(self, question, start=0, stop='0'):
        while True:
            answer = input(question) #main question
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
        print(jBold(jfRed('-'*40)))
        for i in range(self.num_of_players):
            name_of_players = input(jfCyan(f"Enter Player {i+1}'s Nickname: ")+jfYellow())
            self.player_scores[name_of_players] = 0
        print(jBold(jfRed('-'*40)))
        print('\n\n')
        
            
    def get_suffix(self, n):
        if 11 <= n % 100 <= 13:
            return 'th'
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

    def winner_calc(self):

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
            for player in self.player_scores:
                max_score = 10
                current_question = self.card_data[question_counter]
                #print('\n')
                print(jBold(jfRed('-'*40)))
                #print(jRGBGradient(f"{str(player).capitalize()}'s Turn: ", (0,120,255),(255,80,80),True))
                print(jBold(jfBBlue(f"{str(player).capitalize()}'s Turn: ")))
                print(jBold(jfRed('-'*40)))
                print('\n')
                print('            ', end='')
                print(jBold(jUnderline('?'+jReset())))
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

# try: 
#     # JwQuizGame().gradient_centerer(
#     #         "GOODBYE!",
#     #         (255,80,80),
#     #         (0,120,255),
#     #         bold=True,
#     #         underline=True
#     #     )
#     TheGame = JwQuizGame()
#     TheGame.main_game()
# except KeyboardInterrupt:
#     print("\n\n")
#     print(jBold(jfRed('-' * 40)))

#     try:
#         print("GOODBYE")
        #JwQuizGame().set_title("GOODBYE!", 0)
        #TheGame.
        # JwQuizGame().gradient_centerer(
        #     "GOODBYE!",
        #     (255,80,80),
        #     (0,120,255),
        #     bold=True,
        #     underline=True
        # ),
        # 0