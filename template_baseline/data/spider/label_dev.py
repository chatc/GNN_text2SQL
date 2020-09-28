import json
with open(r'D:\repo\research\result_explain\baseline\data\spider\dev.json','r') as file:
    dev_data = json.load(file)

with open(r'D:\repo\research\result_explain\baseline\data\spider\bert_run_true_1-step24100.infer', 'r') as file:
    rat_data = [json.loads(x)['beams'][0]['inferred_code'] for x in file]

new_dev = []
for old_dev, rat_query in zip(dev_data, rat_data):
    new_dev.append({'question_toks':old_dev['question_toks'], 'db_id':old_dev['db_id'], 'query':rat_query})

with open('dev_rat_template.json','w') as file:
    json.dump(new_dev, file)