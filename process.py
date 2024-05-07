import csv
from statistics import mean
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from itertools import chain
from collections import Counter
from re import split


def recode_timestamp(timestamp: str) -> int:
    assert timestamp[-3:] == "MDT"
    return int(
        datetime.strptime(timestamp[:-4], "%Y/%m/%d %I:%M:%S %p")
        .replace(tzinfo=timezone(-timedelta(hours=6)))
        .timestamp()
    )


def recode_checkboxes(boxes_checked: str) -> float:
    codings = {"No": 0, "Neutral": 0.5, "Yes": 1}
    return mean([codings[box] for box in boxes_checked.split(";")])


assert recode_checkboxes("Yes;Neutral;No") == 0.5
assert recode_checkboxes("Yes") == 1
assert recode_checkboxes("No") == 0


def numerical_judgements_from_response_to_s_name(
    response: dict, group1: bool, s_name: str
):
    return {
        "s_name": s_name,
        "s_has_🥺": group1 == (s_name == "Wren"),
        "j_expressive": recode_checkboxes(response[s_name + " seems... [Expressive]"]),
        "j_annoying": recode_checkboxes(response[s_name + " seems... [Annoying]"]),
        "j_friendly": recode_checkboxes(response[s_name + " seems... [Friendly]"]),
        "j_cute": recode_checkboxes(response[s_name + " seems... [Cute]"]),
        "j_cisgender": recode_checkboxes(response[s_name + " seems... [Cisgender]"]),
        "j_feminine": recode_checkboxes(response[s_name + " seems... [Feminine]"]),
        "r_timestamp": recode_timestamp(response["Timestamp"]),
        "r_🥺_frequency": float(response['How often do you use the "🥺" emoji?']) / 4,
        "r_🥺_opinion": (
            float(response['As a ranking, how is your opinion of the "🥺" emoji?']) / 4
        ),
        "r_college_student": response["Are you a college student?"][0:3] == "Yes",
        "r_between_18_and_25yo": response["What is your age?"] == "18-25",
        "r_woman": response["What's your gender? (if you have one)"] == "Woman",
        "r_man": response["What's your gender? (if you have one)"] == "Man",
        "r_transgender": response["Are you transgender?"] == "Yes",
        "r_cisgender": response["Are you transgender?"] == "No",
    }


def numerical_judgements_from_response(response: dict, group1: bool) -> list:
    return [
        numerical_judgements_from_response_to_s_name(response, group1, s_name)
        for s_name in ["Wren", "Sage"]
    ]


def numerical_judgements():
    with (
        open(
            "./Processed Data/Numerical Judgements.csv",
            "w",
            encoding="utf-8",
            newline="",
        ) as numerical_judgements_csv,
        open(
            "./Original Data/Group 1 Impressions from Internet Messages.csv",
            "r",
            encoding="utf-8",
        ) as group1_csv,
        open(
            "./Original Data/Group 2 Impressions from Internet Messages.csv",
            "r",
            encoding="utf-8",
        ) as group2_csv,
    ):
        numerical_judgements_fieldnames = [
            "s_name",
            "s_has_🥺",
            "j_expressive",
            "j_annoying",
            "j_friendly",
            "j_cute",
            "j_cisgender",
            "j_feminine",
            "r_timestamp",
            "r_🥺_frequency",
            "r_🥺_opinion",
            "r_college_student",
            "r_between_18_and_25yo",
            "r_woman",
            "r_man",
            "r_transgender",
            "r_cisgender",
        ]
        numerical_judgements = csv.DictWriter(
            numerical_judgements_csv, fieldnames=numerical_judgements_fieldnames
        )
        group1 = csv.DictReader(group1_csv)
        group2 = csv.DictReader(group2_csv)
        numerical_judgements.writeheader()
        for group in [group1, group2]:
            for response in group:
                numerical_judgements.writerows(
                    numerical_judgements_from_response(response, group is group1)
                )


numerical_judgements()


def answers_to_field(original_fieldname: str, output_filename: str) -> list:
    with (
        open(
            "./Original Data/Group 1 Impressions from Internet Messages.csv",
            "r",
            encoding="utf-8",
        ) as group1_csv,
        open(
            "./Original Data/Group 2 Impressions from Internet Messages.csv",
            "r",
            encoding="utf-8",
        ) as group2_csv,
        open(
            f"./Processed Data/{output_filename}",
            "w",
            encoding="utf-8",
        ) as outfile,
    ):
        group1 = csv.DictReader(group1_csv)
        group2 = csv.DictReader(group2_csv)
        values = [response[original_fieldname] for response in chain(group1, group2)]
        for value in values:
            outfile.write(repr(value) + "\n")
        return values


names = lambda: answers_to_field('What do you call the "🥺" emoji?', "Names.txt")
meanings = lambda: answers_to_field('What does the "🥺" emoji mean? ', "Meanings.txt")


def analyse_responses(responseiterator):
    # return Counter(word for name in responseiterator() for word in split("\W", name.lower())).most_common(50)
    return len(
        [response for response in responseiterator() if "cute" in response.lower()]
    )


print(analyse_responses(names))
