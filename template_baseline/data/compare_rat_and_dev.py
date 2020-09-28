import json
with open('better_pattern.json') as file:
    dev_pattern = json.load(file)

with open('better_pattern_rat.json') as file:
    rat_pattern = json.load(file)

question_pattern_dict = {}
for pattern in dev_pattern:
    for x in pattern[1]:
        question_pattern_dict[x['question']] = [pattern[0]]

for pattern in rat_pattern:
    for x in pattern[1]:
        question_pattern_dict[x['question']] += [pattern[0]]

count = 0
for question, pattern in question_pattern_dict.items():
    if pattern[0] != pattern[1]:
        print(pattern[0], question)
        count += 1
print('total:', count, 'rate', 1 - count/1034)
...