from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import xpath
import time


def add_question():
    """Locates and clicks on add question button in browser"""

    try:
        add_question_button = driver.find_element_by_xpath(xpath.ADD_QUESTION_BUTTON)
    except NoSuchElementException:
        input("ERROR: Make sure to be on your Google form and do not interfere with the browser!\n")
        driver.close()
        exit(0)
    else:
        add_question_button.click()


def send_info(location, element, info):
    """Locates element in browser and sends information

    Gets element from list of elements and send information to that element

    Parameters
    ----------
    location : str
        Xpath location of the elements
    element : int
        Index of element in the location
    info : str
        Information to send to the element in the location
    """

    elements = driver.find_elements_by_xpath(location)
    # if first answer
    if element == -2:
        # click needed to clear answer box, .clear() not working...
        elements[element].click()
    elements[element].send_keys(info)
    # necessary time for google forms to finish entering the text
    time.sleep(0.5)


def fill_list() -> list:
    """Fills list in which questions are taken to fill Google form"""

    questions_list = []
    with open("questions.txt", "r", encoding="utf8") as file:
        for line in file:
            if '\n' in line:
                # avoids return
                questions_list.append(line[:-1])
            else:
                questions_list.append(line)
    return questions_list


########################################################################


def main_loop():
    print("Adding questions...\n")
    add_question()
    # necessary booleans to change input location
    new_question = True
    first_answer = False
    # questions counter to print while process is running
    questions_count = 0

    for info in questions:
        if not info:
            # adds a new question when blank line found
            add_question()
            new_question = True
            questions_count += 1
            print(str(questions_count) + " questions added")
        elif new_question:
            # adds info in question box
            send_info(xpath.QUESTION_BOX, -1, info)
            new_question = False
            first_answer = True
        elif first_answer:
            # adds info in first answer box
            send_info(xpath.ANSWER_BOX, -2, info)
            first_answer = False
        else:
            # adds info in the rest of the answer boxes
            send_info(xpath.ANSWER_BOX, -1, info)

    print(str(questions_count + 1) + " questions added\n")


if __name__ == "__main__":
    print("--------------------------------------------\n"
          "               TEXT TO FORMS\n"
          "--------------------------------------------\n"
          "Instructions:\n"
          "1. Login to your Google account\n"
          "   allow less secure apps if having problems:\n"
          "   https://myaccount.google.com/lesssecureapps\n"
          "2. Wait for the form to load\n"
          "   if there's no form loaded, click on new form\n"
          "3. Hit Enter\n"
          "\nMore info: https://github.com/oscaragl13/text-to-forms\n")

    try:
        driver = webdriver.Chrome()
        driver.get("https://docs.google.com/forms/")
        questions = fill_list()
    except WebDriverException:
        input("ERROR: Make sure to have chromedriver inside the root of the project, Chrome installed,\n"
              "both programs on the same version, and do not close the browser window.\n")
    except FileNotFoundError:
        input("ERROR: Make sure to have questions.txt inside the root of the project and add questions to it.\n")
    else:
        print(str(questions.count('') + 1) + " questions to add.")
        input("Hit Enter when you get to your Google form...\n")
        try:
            main_loop()
        except WebDriverException:
            print("ERROR: Try running the program again.\n")

    input("Process finished, press Enter to exit...")
