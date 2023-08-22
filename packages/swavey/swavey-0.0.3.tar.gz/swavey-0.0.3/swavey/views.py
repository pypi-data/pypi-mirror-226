from flask import jsonify
import requests
import json
from bs4 import BeautifulSoup
import random
from datetime import datetime

def get_user(user_page):
    url = "https://docs.google.com/forms/d/e/" + user_page + "/viewform"
    webpage = requests.get(url)

    type_dict = {0: "Short answer question", 1: "Detailed answer question", 2: "Multiple choice question", 3: "Drop-down question", 4: "Multiple selection question", 5: "Scale", 6: "???", 7: "multiple selection block", 8: "block", 9: "date", 10: "time"}
    swavey_type_dict = {10: "SAQ", 11: "LAQ", 20: "MCQ", 21: "MSQ", 22: "MLQ", 30: "File", 40: "DateTime", 41: "Date", 42: "Time", 50: "APIQ", 51: "Mail", 52: "Addr", 53: "Phone", 54: "Site", 90: "VV"}
    trans_type_dict = {0: 10, 1: 11, 2: 20, 3: 21, 4: 22, 5: 24, 6: 99, 7: 99, 8: 99, 9: 99, 10: 99}

    null = None
    script = json.loads(BeautifulSoup(webpage.content, "html.parser").find('script', attrs={'type': 'text/javascript'}).text[27:-1])

    block_list = []
    question_list = []
    option_list = []
    block_counter = 2
    first_block = True

    survey_id = int(str(random.randint(100000, 999999)) + str(random.randint(100000, 999999)))
    survey_title = BeautifulSoup(webpage.content, "html.parser").find('title').string
    survey_description = script[1][0]
    survey_datatime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i in range(0, len(script[1][1])):
        print("\ni =", i, script[1][1][i])

        if script[1][1][i][3] == 8:
            block_name = script[1][1][i][1]
            block_description = script[1][1][i][2]
            block_order = block_counter

            block_counter += 1
            blocks = [
                {
                    "block_id": block_order,
                    "block_name": block_name,
                    "block_description": block_description,
                    "block_questions": question_list
                }
            ]
            block_list.append(blocks)
            question_list = []

        elif script[1][1][i][3] == 0 or script[1][1][i][3] == 1:

            name = script[1][1][i][1]
            print("name:", name)

            qtype = trans_type_dict[script[1][1][i][3]]
            print("type:", qtype, type_dict[script[1][1][i][3]])
            print("No options")

            qid = random.randint(10000000, 99999999)

            required = True if script[1][1][i][4][0][2] == 1 else False
            print("required:", required)

            question = [
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "question_name": name,
                    "question_options": [],
                    "question_default": null,
                    "question_link": null,
                    "question_validation": null,
                    "question_required": required
                }
            ]
            question_list.append(question)

        elif script[1][1][i][3] == 9 or script[1][1][i][3] == 10 or script[1][1][i][3] == 5 or script[1][1][i][3] == 7:

            name = script[1][1][i][1]
            print("name:", name)

            qtype = trans_type_dict[script[1][1][i][3]]
            print("type:", qtype, type_dict[script[1][1][i][3]])
            print("No options")

            qid = random.randint(10000000, 99999999)

            required = True if script[1][1][i][4][0][2] == 1 else False
            print("required:", required)

            question = [
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "question_name": name,
                    "question_options": [],
                    "question_default": null,
                    "question_link": null,
                    "question_validation": null,
                    "question_required": required
                }
            ]
            question_list.append(question)

        else:

            qid = random.randint(10000000, 99999999)

            name = script[1][1][i][1]
            print("name:", name)

            qtype = trans_type_dict[script[1][1][i][3]]
            print("type:", qtype, type_dict[script[1][1][i][3]])

            required = True if script[1][1][i][4][0][2] == 1 else False
            print("required:", required)

            question = [
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "question_name": name,
                    "question_options": option_list,
                    "question_default": null,
                    "question_link": null,
                    "question_validation": null,
                    "question_required": required
                }
            ]
            question_list.append(question)
            option_list = []
            option_counter = 1

            for j in range(0, len(script[1][1][i][4][0][1])):
                choice = script[1][1][i][4][0][1][j][0]
                print("Choice", j + 1, ":", choice)

                option = [
                    {
                        "option_id": option_counter,
                        "option_name": choice,
                        "option_link": null
                    }
                ]
                option_list.append(option)
                option_counter += 1

    data = [
        {
            "_id": survey_id,
            "_title": survey_title,
            "_description": survey_description,
            "_datetime": survey_datatime,
            "survey_blocks": block_list
        }
    ]

    return jsonify(data)