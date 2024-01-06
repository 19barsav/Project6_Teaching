"""
Project Solution for introductory course, Project 6

Created by Savvy Barnes
"""

import csv
from operator import itemgetter

TITLE = 1
CATEGORY = 3
YEAR = 5
RATING = 6
PAGES = 7

MENU = "\nWelcome to the Book Recommendation Engine\n\
        Choose one of below options:\n\
        1. Find a book with a title\n\
        2. Filter books by a certain criteria\n\
        3. Recommend a book \n\
        4. Quit the program\n\
        Enter option: "

INVALID_INPUT = "\nInvalid input"

CRITERIA_INPUT = "\nChoose the following criteria\n\
                 (3) Category\n\
                 (5) Year Published\n\
                 (6) Average Rating (or higher) \n\
                 (7) Page Number (within 50 pages) \n\
                 Enter criteria number: "

VALUE_INPUT = "\nEnter value: "

CATEGORY_INPUT = "\nEnter the desired category: "
RATING_INPUT = "\nEnter the desired rating: "
PAGE_INPUT = "\nEnter the desired page number: "
A_Z_INPUT = "\nEnter 1 for A-Z sorting, and 2 for Z-A sorting: "
KEYWORDS = "\nEnter keywords (space separated): "


def open_file():
    while True:
        try:
            filename = input("Enter file name: ")
            file_pointer = open(filename,  encoding='utf-8')
        except FileNotFoundError:
            print("\nError opening file. Please try again.")
        else:
            return file_pointer

def read_file(fp):
    csv_reader = csv.reader(fp)
    next(csv_reader)

    master_list = []
    for line in csv_reader:
        try:
            isbn13 = line[0]
            title = line[2]
            authors = line[4]
            categories = line[5].lower().split(",")

            description = line[7]
            year = line[8]
            rating = float(line[9])
            num_pages = int(line[10])
            rating_count = int(line[11])
            master_list.append((isbn13, title, authors, categories, description, year, rating, num_pages, rating_count))
        except:
            continue
    return master_list



def get_books_on_criterion(master_list, criteria, value):
    new_list = []
    if criteria == TITLE:
        value = value.lower()
        for book in master_list:
            if book[criteria].lower() == value:
                return book

    elif criteria == CATEGORY:
        value = value.lower()
        for book in master_list:
            if value in book[criteria]:
                new_list.append(book)
        return new_list

    elif criteria == YEAR:
        for book in master_list:
            value = value.lower()
            if book[criteria].lower() == value:
                new_list.append(book)
        return new_list

    elif criteria == RATING:
        for book in master_list:
            if book[criteria] >= value:
                new_list.append(book)
        return new_list

    elif criteria == PAGES:
        for book in master_list:
            if book[criteria] <= value + 50 and book[criteria] >= value - 50:
                new_list.append(book)
        return new_list


def get_books_by_criteria(master_list, category, rating, page_number):
    list1 = get_books_on_criterion(master_list, CATEGORY, category)
    list2 = get_books_on_criterion(list1, RATING, rating)
    return get_books_on_criterion(list2, PAGES, page_number)

def get_books_by_keyword(master_list, keywords):
    new_list = []
    for book in master_list:
        des = book[4].lower()
        for word in keywords:
            if word.lower() in des:
                new_list.append(book)
                break
    return new_list


def sort_authors(master_list, a_z=True):

    return sorted(master_list, key=itemgetter(4), reverse= not a_z)


def recommend_books(master_list, keywords, category, rating, page_number,  a_z):
    final_list = []
    list1 = get_books_by_criteria(master_list, category, rating, page_number)
    list2 = get_books_by_keyword(master_list, keywords)
    for book in list2:
        if book in list1:
            final_list.append(book)
    new_list = sort_authors(final_list, a_z)
    return new_list


def display_books(master_list):
    print("{:15s} {:35s} {:35s} {:6s} {:8s} {:15s} {:15s}".format("ISBN-13", "Title", "Authors", "Year", "Rating", "Number Pages", "Number Ratings"))
    for book in master_list:
        if len(book[1]) > 35 or len(book[2]) > 35:
            continue
        print("{:15s} {:35s} {:35s} {:6s} {:<8.2f} {:<15d} {:<15d}".format(book[0], book[1], book[2], book[5], book[6], book[7], book[8]))

def get_option():
    option = int(input(MENU))
    if 1 <= option <= 4:
        return option
    else:
        print(INVALID_INPUT)

def main():
    """This function takes no input. It calls the other helper functions and runs the program."""
    fp = open_file()
    master_list = read_file(fp)
    while True:
        user_option = get_option()
        if user_option == 4:
            break

        #   performing tasks for option 1
        elif user_option == 1:
            value = input("Input a book title: ")
            print("\nBook Details:")
            book = get_books_on_criterion(master_list, TITLE, value)
            display_books([book])

        #   performing tasks for option 2
        elif user_option == 2:

            criteria_option = int(input(CRITERIA_INPUT))
            while criteria_option != 7 and criteria_option != 6 and criteria_option != 5 and criteria_option != 3:
                print(INVALID_INPUT)
                criteria_option = int(input(CRITERIA_INPUT))

            value = input(VALUE_INPUT)

            # converting value option to integer if the criterion is RARITY
            if criteria_option == 6 or criteria_option == 7:
                while True:
                    try:
                        if criteria_option == 6:
                            value = float(value)
                            break
                        else:
                            value = int(value)
                            break
                    except ValueError:
                        print(INVALID_INPUT)
                        value = input(VALUE_INPUT)

            filtered_characters = get_books_on_criterion(master_list, criteria_option, value)
            sorted_books = sort_authors(filtered_characters, True)
            display_books(sorted_books[0:30])

        #   performing tasks for option 3
        elif user_option == 3:
            category = input(CATEGORY_INPUT)
            rating = input(RATING_INPUT)

            while True:
                try:
                    rating = float(rating)
                    break
                except ValueError:
                    print(INVALID_INPUT)
                    rating = input(RATING_INPUT)

            page = input(PAGE_INPUT)
            while True:
                try:
                    page = int(page)
                    break
                except ValueError:
                    print(INVALID_INPUT)
                    page = input(PAGE_INPUT)

            a_z = input(A_Z_INPUT)
            a_z = False if a_z == 1 else True

            keywords = input(KEYWORDS).split()
            all_filtered_books = recommend_books(master_list, keywords, category, rating, page, a_z)
            display_books(all_filtered_books)


# DO NOT CHANGE THESE TWO LINES
# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.
if __name__ == "__main__":
    main()
