#!/usr/bin/env python
"""

Relearning some python with a task to generate raw bowling scores, that later will be used as input to find the overall score.  The raw scores will number of pins hit for a given throw, with X indicating the first throw knocked down all 10 pins, and / indicating the second throw knocked down the pins remaining from the first throw.  The number of pins will be random on each throw. 

"""

import random
import sys
import os
import math

def put_your_shoes_on():
    print ("Get your shoes on and get ready to bowl. ")

    bowler_name = str(input("Enter the name of the bowler:"))

    """ Initialize the scoring """

    scores_file_name = "bowling_scores_1.txt"        
    while True: 
        try:
            fscores = open(scores_file_name, "w+")
        except  IOError:
            print ("I can't open ", scores_file_name, "The end is nigh")
            return
        greeting = "Welcome to BAYSHORE BOWL " + bowler_name + "!"
        fscores.write(greeting)
        fscores.close()
        print(open(scores_file_name).read())
        break

    raw_scores = knock_down_pins(bowler_name)
#    print(raw_scores)

    
def knock_down_pins(bowler_name):

    """ Big loop to bowl this round """
    raw_scores = []
    score_this_frame = []
    frame = 0
    for frame in range(1, 10, 1):
        print("\n", bowler_name, " frame number: ", frame, sep="")
        first_throw = random.randint(0,10)
        pins_remaining_1 = 10 - first_throw
        print("First Throw:", first_throw, "pins.")
        if pins_remaining_1 == 0:
            print("You got a STRIKE!!!")
            score_this_frame = ["X", 10, 0]
            raw_scores.append(score_this_frame)
        else:
            if pins_remaining_1 == 10:
                print(":( Gutter Ball :(")
            second_throw = random.randint(0,pins_remaining_1)
            print("Second Throw", second_throw, "pins.")
            pins_remaining_2 = pins_remaining_1 - second_throw
            if pins_remaining_2 == 0:
                print("You got a Spare!")
                score_this_frame = ["/",first_throw, second_throw]
                raw_scores.append(score_this_frame)
            else:
                total_pins_down = first_throw + second_throw
                print("You knocked down a total of ", str(10 - pins_remaining_2), " pins this frame")
                score_this_frame = ["-",first_throw, second_throw]
                raw_scores.append(score_this_frame)
                
        print(raw_scores)
        print(keep_score(raw_scores))

    # End of first 9 frames

    frame = 10
    print("\n", bowler_name, " frame number: ", frame, sep="")
    first_throw = random.randint(0,10)
    pins_remaining_1 = 10 - first_throw
    print("First Throw:", first_throw, "pins.")
    if pins_remaining_1 == 0:
        print("You knocked them all down on the first throw of frame 10.  You get two more throws!")
        second_throw = random.randint(0,10)
        print("Second Throw:", second_throw, "pins")
        pins_remaining_2 = 10 - second_throw
        if pins_remaining_2 == 0:
            print("Wow, two strikes on the last frame, will it be 3?")
            third_throw = random.randint(0,10)
            print("Third Throw:", third_throw, "pins")
            pins_remaining_3 = 10 - third_throw
            if pins_remaining_3 == 0:
                print("OMG a Turkey on the last frame!!!")
                score_this_frame = [10,10,10]
                raw_scores.append(score_this_frame)
            else:
                score_this_frame = [10,10,third_throw]
                raw_scores.append(score_this_frame)
        else:
            third_throw = random.randint(0, pins_remaining_2)
            total_pins_last_two_throws = second_throw + third_throw
            print("Third Throw:", third_throw, "pins")
            score_this_frame = [10,second_throw,third_throw]
            raw_scores.append(score_this_frame)
    else:
        second_throw = random.randint(0, pins_remaining_1)
        pins_remaining_2 = pins_remaining_1 - second_throw
        print("Second Throw:", second_throw, "pins")
        if pins_remaining_2 == 0:
            print("Good, you got a spare on the last frame, so you get one more throw to add to your spare!")
            third_throw = random.randint(0,10)
            print("Third Throw:", third_throw, "pins")
            score_this_frame = [first_throw, second_throw, third_throw]
            raw_scores.append(score_this_frame)
        else:
            total_pins_last_frame = first_throw + second_throw
            score_this_frame = [first_throw, second_throw,0]
            raw_scores.append(score_this_frame)
    print(raw_scores)
    print(keep_score(raw_scores))
#   print(keep_score([['-', 8, 0], ['-', 6, 0], ['/', 8, 2], ['-', 2, 7], ['-', 4, 3], ['-', 4, 2], ['/', 5, 5], ['X', 10, 0]]))
#   print(keep_score([["X",10, 0], ["X",10, 0], ["X",10, 0], ["X",10, 0], ["X",10, 0], ["X",10, 0], ["X",10, 0], ["X",10, 0], ["X",10, 0], [10,10,10]]))
    return(raw_scores)

def keep_score(raw_scores):
    # print(raw_)
    # print(score_by_frame)
            

    """ Input the raw_scores and print out the running score each frame and total """

    last_recorded_score = 0
    score_by_frame = [0] * 10
    scoring_string = ""
    last_frame = []
    if len(raw_scores) == 10:
        last_frame = raw_scores.pop()
    for frame, score in enumerate(raw_scores):   
        # print(frame, score)
        # print("Total pins knocked down this frame", sum(score))
        # first we determine what we got in this frame for use in the coming deferred scoring logic...
        if score[0] == "-":
            if frame == 0:
                score_by_frame[frame] = sum(score[1:])
                last_recorded_score = score_by_frame[frame]
            else:
                if raw_scores[frame-1][0] == "-":
                    score_by_frame[frame] = score_by_frame[frame-1] + sum(score[1:])
                    last_recorded_score = score_by_frame[frame]
                elif raw_scores[frame-1][0] == "/":
                    score_by_frame[frame-1] = last_recorded_score + 10 + score[1]
                    last_recorded_score = score_by_frame[frame-1]
                    score_by_frame[frame] = last_recorded_score + sum(score[1:])
                    last_recorded_score = score_by_frame[frame]
                else:
                    score_by_frame[frame-1] = last_recorded_score + 10 + sum(score[1:])
                    last_recorded_score = score_by_frame[frame-1]
                    score_by_frame[frame] = last_recorded_score + sum(score[1:])
                    last_recorded_score = score_by_frame[frame]
            scoring_string = "Your current score is: " + str(last_recorded_score)
        elif score[0] == "X":
            if frame == 0:
                scoring_string = "You got a strike on the first frame!!!  Only 11 more for a perfect game!"
            else:
                if raw_scores[frame-1][0] == "X":
                    if frame == 1:
                        scoring_string = "You got a strike on the first 2 frames!!!  Only 10 more for a perfect game!"
                    else:
                        if raw_scores[frame-2][0] == "X":
                            score_by_frame[frame-2] = last_recorded_score + 30
                            last_recorded_score = score_by_frame[frame-2]
                            print("Gobble, Gobble, Gobble...you got a Turkey - 3 strikes in a row.")                
                    scoring_string = "You are working on two strikes!!!.  Your last recorded score was: " + str(last_recorded_score)
                elif raw_scores[frame-1][0] == "/":
                    score_by_frame[frame-1] = last_recorded_score + 20
                    last_recorded_score = score_by_frame[frame-1]
                    scoring_string = "You are working on a strike!  Your last record score was: " + str(last_recorded_score)
                else:
                    scoring_string = "You are working on a strike!  Your last record score was: " + str(last_recorded_score)
        else:
            if frame == 0:
                scoring_string = "You got a spare in the first frame!"
            else:
                if raw_scores[frame-1][0] == "X":
                    score_by_frame[frame-1] = last_recorded_score + 20
                    last_recorded_score = score_by_frame[frame-1]
                    scoring_string = "Your last recorded score is: " + str(last_recorded_score) + ". Your last frame was a spare!"
                elif raw_scores[frame-1][0] == "/":
                    score_by_frame[frame-1] = last_recorded_score + 10 + score[1]
                    last_recorded_score = score_by_frame[frame-1]
                    scoring_string = "Your last recorded score is: " + str(last_recorded_score) + ". Your last frame was a spare!"
                else:
                    scoring_string = "You are working on a spare.  Your last record score was: " + str(last_recorded_score)

    if last_frame != []:
        frame = 9
        if raw_scores[8][0] == "X":
            if raw_scores[7][0] == "X":
                score_by_frame[7] = last_recorded_score + 20 + last_frame[0]
                last_recorded_score = score_by_frame[7]
            score_by_frame[8] = last_recorded_score + 10 + sum(last_frame[:2])
            last_recorded_score = score_by_frame[8]
        elif raw_scores[8][0] == "/":
            score_by_frame[8] = last_recorded_score + 10 + last_frame[0]
            last_recorded_score = score_by_frame[8]
        if sum(last_frame[:2]) < 10:
            score_by_frame[9] = last_recorded_score + sum(last_frame[:2])
            last_recorded_score = score_by_frame[9]
        elif last_frame[0] == 10:
            if last_frame[1] == 10:
                if last_frame[2] == 10:
                    score_by_frame[9] = last_recorded_score + 30
                    last_recorded_score = score_by_frame[9]
                else:
                    score_by_frame[9] = last_recorded_score + 20 + last_frame[2]
                    last_recorded_score = score_by_frame[9]
            else:
                score_by_frame[9] = last_recorded_score + 10 + sum(last_frame[1:3])
                last_recorded_score = score_by_frame[9]
        else:
            score_by_frame[9] = last_recorded_score + 10 + last_frame[2]
            last_recorded_score = score_by_frame[9]
        scoring_string = "\n" + "Your final Score is: " + str(last_recorded_score)
        raw_scores.append(last_frame)
    print(score_by_frame)
    return(scoring_string)           

put_your_shoes_on()