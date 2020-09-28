from util_for_baseline import *


if __name__ == '__main__':
    # In[5]:

    training_data, dev_data, tables = read_in_all_data()

    train_qq_pairs = get_all_question_query_pairs(training_data)
    dev_qq_pairs = get_all_question_query_pairs(dev_data)

    # In[6]:

    print("Training question-query pair count: {}".format(len(train_qq_pairs)))
    print("Dev question-query pair count: {}".format(len(dev_qq_pairs)))

    # pqd: pattern question dictionary
    train_pdq, detailed_train_pdq = get_pattern_question(train_qq_pairs, tables)
    tot = 0
    for i, pattern in enumerate(detailed_train_pdq):
        tot += len(pattern[1])
        print(i+1, pattern[0], len(pattern[1]), tot/8659)
    json.dump(detailed_train_pdq, open(SAVE_PATH, 'w'), indent=2)
