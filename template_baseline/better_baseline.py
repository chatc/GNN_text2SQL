import json
import random
from util_for_baseline import *

template_path = './data/better_pattern.json' # change to new template if needed
question_template_path = './data/better_question_template.txt'
result_path = "./data/results_on_spider_dev.txt" # place to restore result
sql_component_path = "./data/sql_components.json"


def SQL_to_text(query, table, tempaltes_pqd, gold_template, sql_component):
    # extract slots in query
    pattern, *dicts = strip_query_full_dict(query, table)
    tu_pattern = tune_pattern(pattern) # reorder the slots

    # map the slots with different orders
    mapping = {tu_token: token for token, tu_token in
               zip(pattern.split(' '), tune_pattern(pattern, omit_distinct=False).split(' '))}

    # fill in the slots
    # dicts:value_dict, column_dict, table_dict, sql_component_dict, \
    #            columns_lemed_stemed, select_clauses, column_nl_dict, table_map
    name_dict = {**dicts[0], **dicts[1], **dicts[2], **dicts[3]}
    try:
        target_question_template = gold_template[[x[0] for x in tempaltes_pqd].index(tu_pattern)].split(' ')
    except:
        raise RuntimeError('error: template not found on:{}'.format(tu_pattern))

    # for debugging
    if len(target_question_template)<3:
        return 'not finish'

    # replace select clauses
    select_clauses = dicts[-3]
    for i, clause in enumerate(select_clauses):
        sym = "{{SELECT{}}}".format(i)
        cleaned_clause = clean_select(clause, [dicts[2][x] for x in dicts[-1][sym]])
        try:
            pos = target_question_template.index(sym)
        except:
            raise RuntimeError('error: select clause replacement failure:{}'.format(tu_pattern))
        target_question_template = target_question_template[:pos] + \
                                   cleaned_clause + target_question_template[pos + 1:]

    # use original column
    original_column_name = dicts[-2]
    for col, val in original_column_name.items():
        name_dict[col] = val

    restored_question = []
    for token in target_question_template:
        if '{' in token and '}' in token:
            start = token.index('{')
            end = token.index('}') + 1
            if "SELECT" in token:
                restored_question.append('select')
            else:
                try:
                    token_core = token[start:end]
                    if 'OLD' in token:
                        key = token_core[:-4] + '}'
                    else:
                        key = mapping[token_core]
                    token_value = token[:start] + name_dict[key] + token[end:]
                except:
                    raise RuntimeError("error:{}, {}, {}".format(token, mapping, name_dict))
                record = 0
                for sym in ['AGG', 'OP', "SC"]:
                    if sym in token:
                        restored_question.append(sql_component[sym][token_value][0])
                        record = 1
                        break
                if record == 0:
                    restored_question.append(token_value)
        else:
            restored_question.append(token)

    return ' '.join(restored_question)


if __name__ == '__main__':
    # load data
    training_data, dev_data, tables = read_in_all_data()
    test_qq_pairs = get_all_question_query_pairs(dev_data) # test on train set

    # [[tempalte(str), [question(str)]]]
    tempaltes_pqd = json.load(open(template_path, 'r'))

    # load other dataset
    gold_template = [line.strip() for line in open(question_template_path)] + ["Find {SELECT0}"]*300
    sql_component = json.load(open(sql_component_path))

    # matching start
    with open(result_path, 'w') as file:
        for eid, (question, query, bd_id) in enumerate(test_qq_pairs):
            table = tables[bd_id]
            if eid % 500 == 0:
                print("processing eid: ", eid)
            try:
                restored_question = SQL_to_text(query, table, tempaltes_pqd, gold_template, sql_component)
            except Exception as e:
                print(e)
                continue

            file.write("recovered: " + restored_question+'\n')
            file.write("original: " + ' '.join(question) + '\n\n')



