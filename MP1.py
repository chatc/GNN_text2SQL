import json
import networkx as nx
from pyvis.network import Network

DATA_PATH = "./nl2code,output_from=true,fs=2,emb=bert,cvlink/enc/val.jsonl"
CLASS_PATH = "./template_baseline/data/better_pattern.json"


def load_preprocessed_data(path):
    data = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data


def load_template_class(path):
    with open(path,'r', encoding='utf-8') as file:
        data = json.load(file)
    simplified_data = [(x[0],[y['question'] for y in x[1]]) for x in data]
    return simplified_data


def plot(nx_graph, head):
    nt = Network(notebook=False, height="750px", width="100%", heading=head)

    nt.from_nx(nx_graph)
    nt.show("nx.html")


def add_edge_question_to_columns(G, sample, ind1, ind2, group):
    for ind, type in sample[ind1][ind2].items():
        u = 'q' + ind.split(',')[0]
        v = 'c' + ind.split(',')[1]
        G.add_edge(u, v, group=group, title=ind2)


def get_question_graph_dict(data):
    question_graph_dict = {}
    for i, sample in enumerate(data):
        G = nx.Graph()
        # add all the nodes
        for i, q_token in enumerate(sample['question']):
            G.add_node('q{}'.format(i), title=q_token, group=0)
        for i, c_token in enumerate(sample['columns']):
            larger = str(i) in sample['primary_keys']
            G.add_node('c{}'.format(i), title=c_token, group=1, size=25 if larger else 10)
        for i, t_token in enumerate(sample['tables']):
            G.add_node('t{}'.format(i), title=t_token, group=2)

        # add all the edges
        # add edges between question and schemas
        add_edge_question_to_columns(G, sample, 'sc_link', 'q_col_match', 0)
        add_edge_question_to_columns(G, sample, 'sc_link', 'q_tab_match', 0)
        add_edge_question_to_columns(G, sample, 'cv_link', 'num_date_match', 0)
        add_edge_question_to_columns(G, sample, 'cv_link', 'cell_match', 0)

        # add edges inner schemas
        for u, v in sample['column_to_table'].items():
            u = 'c{}'.format(u)
            v = 't{}'.format(v)
            G.add_edge(u, v, title='column_to_table', group=1)
        for u, v in sample['foreign_keys'].items():
            u = 'c{}'.format(u)
            v = 'c{}'.format(v)
            G.add_edge(u, v, title='foreign_keys', group=2)
        for u, tables in sample['foreign_keys_tables'].items():
            u = 't{}'.format(u)
            for v in tables:
                v = 't{}'.format(v)
                G.add_edge(u, v, title='foreign_key_tables', group=3)

        # # show title
        # for node in G.nodes():
        #     node['title'] = node['']
        question_graph_dict[sample['raw_question']] = G
    return question_graph_dict


if __name__ == '__main__':
    data = load_preprocessed_data(DATA_PATH)
    # data: [{'question':[tokens], -> q_1, ... , q_n, group: 0
    # 'columns':[[*,<type: text>], [token1,..,token_n, <type:xxx>] -> c_1, ... , c_m, group: 1
    # 'tables': [[token1, token2...]] -> t_1, ..., t_k, group: 2

    # 'sc_link':{'q_col_match':{'u,v':'CPM'}, 'q_tab_match':{'u,v':'TEM'}}, -> group: 0
    # 'cv_link':{'num_date_match':{'u,v':'NUMBER'}, 'cell_match':{'u,v':"CELL"}] -> group: 0
    # 'column_to_table' : {i:j(int)} -> group: 2
    # 'table_to_columns' : {i:j(int)} -> group: 2
    # 'foreign_keys': { i(colunm): j(column)} -> group: 3
    # 'foreign_key_tables': { table: [tables]} -> group: 4
    # 'primary_keys': [column_names] -> group: 5

    template_class = load_template_class(CLASS_PATH)
    question_graph_dict = get_question_graph_dict(data)

    # plot the graph in different class
    for question in template_class[0][1]:
        if question in question_graph_dict.keys():
            plot(question_graph_dict[question], template_class[0][0])
            break

    for question in template_class[36][1]:
        if question in question_graph_dict.keys():
            plot(question_graph_dict[question], template_class[39][0])
            break