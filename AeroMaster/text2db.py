import os
import re
import sys

import django

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AeroMaster.settings")  # Make sure "AeroMaster" is correct

# Initialize Django
django.setup()

from AeroMaster.models import Question  # ✅ CORRECT (Use the full project name)

'''
def insert_db():
    q1 = Question.objects.create(
        text="What is python?",
        option_a="A Python framework",
        option_b="A JavaScript library",
        option_c="A database",
        option_d="A programming language",
        correct_answer="A",
        subject="AIRCRAFT CONSTRUCTION, REPAIR, AND MODIFICATION"
    )
'''
with open("question_temp.txt", "r", encoding="utf-8") as file:
    text = file.read()

with open("answer_temp.txt", "r", encoding="utf-8") as file:
    ans = file.read()

ans_s = re.findall(r'\b[A-D]\b', ans)
question = re.split(r"\d+\.\s*", " ".join(text.splitlines()))[1:]

maxlen = 0
minlen = 10
for items in question:
    item = re.split(r"\s*[A-Z]\.\s*", items)
    maxlen = max(maxlen, len(item))
    minlen = min(minlen, len(item))

print(f"max: {maxlen}")
print(f"min: {minlen}")
print(f"size of question: {len(question)}")
print(f"size of answer: {len(ans_s)}")

if maxlen != minlen or len(question) != len(ans_s):
    print("Error: Question and answer count mismatch.\n recheck temp files.\n Exiting program.")
    sys.exit(1)

confirmation = input("would you like to proceed?[y/n]: ")
if confirmation == 'y':
    subject = input("Subject name? [aero, acrm, asd, eemle, math, power]: ")
    for index, items in enumerate(question):
        item = re.split(r"\s*[A-Z]\.\s*", items)
        q1 = Question.objects.create(
            text=item[0],
            option_a=item[1],
            option_b=item[2],
            option_c=item[3],
            option_d=item[4],
            correct_answer=ans_s[index],
            subject=subject
        )
