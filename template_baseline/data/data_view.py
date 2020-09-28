import json

start = 170
end = 200

data = json.load(open("better_pattern.json"))
for i, pattern in enumerate(data[start-1: end-1]):
    print(i+start, '.')
    print(json.dumps(pattern, indent=2))
    print('\n')
