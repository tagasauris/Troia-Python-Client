import sys
import csv
import pprint

sys.path.append('../')
from dsas import DSaS


def load_costs(path):
    cost = csv.reader(open(path + "/costs"), delimiter='\t')
    dictt = {}
    for c1, c2, cost_ in cost:
        el = dictt.get(c1, {})
        el[c2] = cost_
        dictt[c1] = el
    return [{'name':c, 'prior':1., 'misclassification_cost':d}
                                                for c, d in dictt.iteritems()]


def load_correct(path):
    correct = csv.reader(open(path + "/correct"), delimiter='\t')
    correct = [x[-2:] for x in correct]
    print correct
    return [{"objectName": s, "correctCategory": v} for s, v in correct]


def load_input(path):
    inputt = csv.reader(open(path + "/input"), delimiter='\t')
    return [{'workerName':wn, 'objectName':on, 'categoryName':cn}
                                                    for wn, on, cn in inputt]


def load_all(path):
    r = [list(csv.reader(open(path + s), delimiter='\t'))
                            for s in ['/correct', '/costs', '/input']]
    r[0] = [x[-2:] for x in r[0]]
    return r


def transform_cost(cost):
    dictt = {}
    for c1, c2, cost_ in cost:
        el = dictt.get(c1, {})
        el[c2] = cost_
        dictt[c1] = el
    return dictt.items()


def test_all(dsas, correct, cost, inputt):

    ID = "123"
    dsas.reset(ID)

    cost = transform_cost(cost)

    dsas.load_categories(cost, ID)
    dsas.load_gold_labels(correct, ID)
    dsas.load_worker_assigned_labels(inputt, ID)
    dsas.compute_blocking(3, ID)
    print pprint.pprint(dsas.get_dawid_skene(ID))


dsas = DSaS("http://localhost:8080/GetAnotherLabel/rest/")
main_path = "examples/"

data = load_all(sys.argv[1])

test_all(dsas, *data)
