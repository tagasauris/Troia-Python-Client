import sys
import csv
import pprint
import time

sys.path.append('../')
from troia_client import TroiaClient


def load_costs(path):
    cost = csv.reader(open(path + "/costs"), delimiter='\t')
    dictt = {}
    for c1, c2, cost_ in cost:
        el = dictt.get(c1, {})
        el[c2] = cost_
        dictt[c1] = el
    return [{'name':c, 'misclassification_cost':d} for c, d in dictt.iteritems()]


def load_correct(path):
    correct = csv.reader(open(path + "/correct"), delimiter='\t')
    return [x[-2:] for x in correct]

def load_input(path):
    return csv.reader(open(path + "/input"), delimiter='\t')
    
def load_evaldata(path):
    return csv.reader(open(path + "/eval"), delimiter='\t')


def load_all(path, prefix="testData_", suffix=".txt"):
    r = [list(csv.reader(open(path + s), delimiter='\t'))
            for s in ['/{}correct{}'.format(prefix, suffix), '/{}costs{}'.format(prefix, suffix), '/{}input{}'.format(prefix, suffix)]]
    r[0] = [x[-2:] for x in r[0]]
    return r


def transform_cost(cost):
    dictt = {}
    for c1, c2, cost_ in cost:
        el = dictt.get(c1, {})
        el[c2] = cost_
        dictt[c1] = el
    return dictt.items()


def test_all(dsas, gold_labels, cost, labels):

    ID = "test123"
    iter_per_iter = 10
    
    dsas.ping()
    dsas.reset(ID)

    cost = transform_cost(cost)

    print dsas.load_categories(cost, ID)
    print dsas.load_gold_labels(gold_labels, ID)
    print dsas.load_worker_assigned_labels(labels, ID)
#    print dsas.load_objects(['additional_obj1', 'additional_obj2'], ID)
    evaldata = load_evaldata("examples/porn")
    print dsas.load_evaluation_labels(evaldata, ID)
    dsas.compute_non_blocking(iter_per_iter, ID)
    while 'true' not in dsas.is_computed(ID):
        time.sleep(2)
#    print dsas.calculate_estimated_cost(ID)
#    print dsas.get_estimated_cost(ID, "additional_obj1", "porn")
#    print dsas.get_estimated_cost(ID, "additional_obj1", "notporn")
#    print dsas.get_estimated_cost(ID, "additional_obj2", "porn")
#    print dsas.get_estimated_cost(ID, "additional_obj2", "notporn")
#    print dsas.get_worker_cost(ID, None, "worker1")
    print dsas.print_worker_summary(False, ID)
    print dsas.majority_votes(ID)
#    print pprint.pprint(dsas.get_dawid_skene(ID))

    print dsas.calculate_evaluated_cost(ID)
    print dsas.get_evaluated_cost(ID, "porn")

if __name__ == "__main__":
    dsas = TroiaClient("http://localhost:8080/GetAnotherLabel/rest/", None)
    main_path = "examples/"
    
    data = load_all(main_path + sys.argv[1], "", "")
    
    test_all(dsas, *data)
