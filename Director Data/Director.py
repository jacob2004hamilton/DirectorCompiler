import requests
from termcolor import colored
import pyfiglet
import time
import difflib
import os
import json

def get_config():
    f = open("config.json",'r')
    data = json.load(f)
    f.close()
    return data

def subtitle(text, color=None):
    if color == None:
        color = CONFIG['subtitle_color']
    return("   "+colored(f"{text}", CONFIG['subtitle_color'], attrs=['underline'])+"\n")

def printf(media):
    print(colored(media, CONFIG['text_color']))

def output_title(font = ""):
    print(colored(pyfiglet.figlet_format("DIRECTOR"), CONFIG['title_color']))

def clear_screen(replace_title = True):
    os.system('cls' if os.name == 'nt' else 'clear')
    if replace_title == True:
        output_title()

def return_similar_movies(query):
    f = open("MovieList.txt", 'r')
    lines = f.readlines()
    f.close()
    results = []
    for line in lines:
        diff = difflib.SequenceMatcher(None, query.lower(), line.lower().replace("\n", "")).ratio()
        if diff > CONFIG['minimum_similarity_rating']:
            results.append(line.strip())
    return results

def return_similar_tv_shows(query):
    f = open("ShowList.txt", 'r')
    lines = f.readlines()
    f.close()
    results = []
    for line in lines:
        diff = difflib.SequenceMatcher(None, query.lower(), line.lower().replace("\n", "")).ratio()
        if diff > CONFIG['minimum_similarity_rating']:
            results.append(line.strip())
    return results

def print_list(arr):
    for i in range(0, len(arr)):
        printf(f"   {i+1}) {arr[i]}")
        if i == len(arr)-1:
            choice = input(colored("\n   Choice/BACK: ", CONFIG['text_color']))
            if choice.lower() == "back":
                home_screen()
            else:
                if int(choice) > len(arr) or int(choice) <= 0:
                    home_screen()
                else:
                    return arr[int(choice)-1]
        elif (i+1)%CONFIG['limit_search_result'] == 0:
            choice = input(colored("\n   Choice/MORE/BACK: ", CONFIG['text_color']))
            if choice.lower() == 'back':
                home_screen()
            if choice.lower() != 'more':
                if int(choice) > len(arr) or int(choice) <= 0:
                    home_screen()
                else:
                    return arr[int(choice)-1]
            else:
                print("\n")

def return_movie_direction(movie_name, number=0):
    f = open("MovieDirections.json",'r')
    data = json.load(f)
    f.close()
    return data[movie_name][number]

def get_number_of_links(movie_name):
    f = open("MovieDirections.json",'r')
    data = json.load(f)
    f.close()
    return len(data[movie_name])

def get_number_of_seasons(tv_show_name, season=None):
    if season != None:
        f = open("ShowDirections.json",'r')
        data = json.load(f)
        f.close()
        return len(data[tv_show_name][season-1])
    else:
        f = open("ShowDirections.json",'r')
        data = json.load(f)
        f.close()
        return len(data[tv_show_name])

def find_movie():
    try:
        clear_screen()
        print(subtitle("MOVIE SEARCH"))
        query = input(colored("   Movie: ", CONFIG['text_color']))
        similar_movies = return_similar_movies(query)
        if similar_movies == []:
            printf("   No matching movies.")
            input("")
            home_screen()
        else:
            clear_screen()
            print(subtitle("SEARCH RESULTS"))
            movie = print_list(similar_movies)
            number, max = 0, get_number_of_links(movie)
            while requests.get(return_movie_direction(movie, number)).status_code == 404:
                number += 1
                if number == max:
                    print("NO WORKING LINKS")
                    input("")
                    home_screen()
                    break

            os.system(f"{CONFIG['version']} {return_movie_direction(movie, number)}")
            input("")
            home_screen()
    except:
        home_screen()

def find_tv_show():
    try:
        clear_screen()
        print(subtitle("TV SHOW SEARCH"))
        query = input(colored("   TV Show: ", CONFIG['text_color']))
        similar_movies = return_similar_tv_shows(query)
        if similar_movies == []:
            printf("   No matching TV shows.")
            input("")
            home_screen()
        else:
            clear_screen()
            print(subtitle("SEARCH RESULTS"))
            tv_show = print_list(similar_movies)
            number_of_seasons = get_number_of_seasons(tv_show)
            clear_screen()
            print(subtitle(tv_show))
            for i in range(number_of_seasons):
                printf(f"   {i+1}) SEASON {i+1}")
            choice = input(colored("\n   Season: ", CONFIG['text_color']))
            if int(choice) > number_of_seasons or int(choice) < 1:
                home_screen()
            else:
                clear_screen()
                print(subtitle(f"SEASON {choice}"))
                number_of_episodes = get_number_of_seasons(tv_show, int(choice))
                f = open("ShowDirections.json", 'r')
                data = json.load(f)
                f.close()
                for i in range(0, number_of_episodes):
                    printf(f"   {i+1}) {data[tv_show][int(choice)-1][i][0]}")
                newchoice = input(colored("\n   Episode: ", CONFIG['text_color']))
                if int(newchoice) > number_of_episodes or int(newchoice) < 1:
                    home_screen()
                else:
                    os.system(f"{CONFIG['version']} {data[tv_show][int(choice)-1][int(newchoice)-1][1]}")
                    next_episode = input(colored("\n   Next Episode(y/n): ", CONFIG['text_color']))
                    while next_episode.lower() == "y":
                        newchoice = int(newchoice)+1
                        if newchoice <= number_of_episodes:
                            os.system(f"{CONFIG['version']} {data[tv_show][int(choice)-1][newchoice-1][1]}")
                        else:
                            home_screen()
                    home_screen()
    except:
        home_screen()


    
def update_lists():
    clear_screen()
    print(subtitle("UPDATE FILES"))
    printf("   To update the files/links, please replace the TXT and JSON files (Except config.json) with the fresh version from the GitHub repo.")
    printf("   If you have an issue and it persists after this, please follow the steps on the Request Content/Report Issues page.")
    input("")
    home_screen()

def request_content():
    clear_screen()
    print(subtitle("REQUEST CONTENT/REPORT ISSUE"))
    printf("   If you can't find the content you love, or the link doesn't work please update your files and try again in case it has been fixed.\n")
    printf("   If the problem persists or the content you want is still not there, please send an email to the link below:\n")
    printf(subtitle("directorrequests@gmail.com"))
    printf("   Thanks.")
    input("")
    home_screen()

def home_screen():
    clear_screen()
    print(subtitle("HOME - Disclaimer -> I do not stream any pirated content, I only share links to the streams, I do not own the streams."))
    printf("   1) Find Movie")
    printf("   2) Find TV Show")
    printf("   3) Update Lists")
    printf("   4) Request Content/Report Issues")
    printf("   5) Quit")
    choice = input(colored("\n   Choice: ", CONFIG['text_color']))
    if choice == '1':
        find_movie()
    elif choice == '2':
        find_tv_show()
    elif choice == '3':
        update_lists()
    elif choice == '4':
        request_content()
    elif choice == '5':
        clear_screen(False)
        exit()
    else:
        clear_screen()
        home_screen()

CONFIG = get_config()

if __name__ == "__main__":
    try:
        home_screen()
    except:
        pass
