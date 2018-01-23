#!/usr/bin/python
import networkx as nx
from z3 import *

G = nx.Graph()
G.add_nodes_from(['rbp', 'linksys', 'user-pc', 'external-system'])
G.add_edges_from([('rbp', 'linksys'),
                  ('user-pc', 'linksys'),
                  ('linksys', 'external-system')])

objectives = [('external-system', 'rbp', 'ssh'),
              ('user-pc', 'rbp', 'sftp')]

print(G.nodes.data())
s = Solver()

ALLOW_SSH_IN = {i: Bool('%s_allow_ssh_in' % i) for i in G.nodes}
ALLOW_SSH_OUT = {i: Bool('%s_allow_ssh_out' % i) for i in G.nodes}
SSH_SERVER = {i: Bool('%s_ssh_server' % i) for i in G.nodes}
SFTP_SERVER = {i: Bool('%s_sftp_server' % i) for i in G.nodes}


def ssh_route(src, dst):
    paths = []
    for path in nx.all_simple_paths(G, source=src, target=dst):
        # print(path)

        statements = []
        for i, node in enumerate(path):
            if i != 0:
                statements.append(ALLOW_SSH_IN[node] == True)
            if i != (len(path) - 1):
                statements.append(ALLOW_SSH_OUT[node] == True)

        paths.append(And([x for x in statements]))
    s.add(Or([x for x in paths]))
    s.add(SSH_SERVER[objective[1]])


def sftp_route(src, dst):
    ssh_route(src, dst)
    s.add(SFTP_SERVER[dst])


for objective in objectives:
    src = objective[0]
    dst = objective[1]
    protocol = objective[2]

    if protocol == 'sftp':
        sftp_route(src, dst)

    if protocol == 'ssh':
        ssh_route(src, dst)

print('')
print('Is there a satisfying solution?')
print(s.check())

print('')
print('What is it?')
print(s.model())

import unittest


class TestNothing(unittest.TestCase):
    def test_nothing(self):
        pass
