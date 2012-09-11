import pprint

from troia_client import TroiaClient


TROIA_SERVER_URL = 'http://localhost:8080/GetAnotherLabel/rest/'
TIMEOUT = None  # We don't want to use timeout
TUTORIAL_JOB_ID = 'TUTORIAL_PYTHON_CLIENT'


ITERATIONS = 5

# porn/not-porn data in Python data structures

COST_MATRIX = [
    ('porn', {
        'porn':     0.,
        'notporn':  1.,
    }),
    ('notporn', {
        'notporn':  0.,
        'porn':     1.,
    }),
]

GOLD_SAMPLES = [
    ('url1', 'notporn'),
    ('url2', 'porn'),
]


WORKERS_LABELS = [
    ('worker1', 'url1', 'porn'),
    ('worker1', 'url2', 'porn'),
    ('worker1', 'url3', 'porn'),
    ('worker1', 'url4', 'porn'),
    ('worker1', 'url5', 'porn'),
    ('worker2', 'url1', 'notporn'),
    ('worker2', 'url2', 'porn'),
    ('worker2', 'url3', 'notporn'),
    ('worker2', 'url4', 'porn'),
    ('worker2', 'url5', 'porn'),
    ('worker3', 'url1', 'notporn'),
    ('worker3', 'url2', 'porn'),
    ('worker3', 'url3', 'notporn'),
    ('worker3', 'url4', 'porn'),
    ('worker3', 'url5', 'notporn'),
    ('worker4', 'url1', 'notporn'),
    ('worker4', 'url2', 'porn'),
    ('worker4', 'url3', 'notporn'),
    ('worker4', 'url4', 'porn'),
    ('worker4', 'url5', 'notporn'),
    ('worker5', 'url1', 'porn'),
    ('worker5', 'url2', 'notporn'),
    ('worker5', 'url3', 'porn'),
    ('worker5', 'url4', 'notporn'),
    ('worker5', 'url5', 'porn'),
]



def run_troia_on_data(cost_matrix, gold_samples, workers_labels):
    troia_client = TroiaClient(TROIA_SERVER_URL, TIMEOUT)
    # we create client instance

    ID = TUTORIAL_JOB_ID

    troia_client.reset(ID)
    # just to make sure that we don't interfere with some old data

    troia_client.load_categories(cost_matrix, ID)
    # we send cost matrix that contains all labels / categories

    troia_client.load_gold_labels(gold_samples, ID)
    # send samples for which we know correct label
    # we could also do this that way:
    # for object_id, label in gold_samples:
    #     troia_client.load_gold_label(object_id, label, ID)

    troia_client.load_worker_assigned_labels(workers_labels, ID)
    # send labels that worker assigned to objects
    # we could also do this that way:
    # for worker, object_id, label in workers_labels:
    #     troia_client.load_worker_assigned_label(worker, object_id, label, ID)

    troia_client.compute_blocking(ITERATIONS, ID)
    # we start actual calculations

    results = troia_client.get_dawid_skene(ID)
    # we collect results and stats

    # pprint.pprint(results)
    # and just print them with some formatting

    objects_data = results['objects'].items()
    # extracting data related to objects

    object_label_probabilities = [(object_id, params['categoryProbability'])
        for object_id, params in objects_data]
    # we extract label distributions for objects
    print "Object label probabilities:"
    pprint.pprint(sorted(object_label_probabilities))
    # and we print them

    # extracting data related to workers
    workers_summary = str(troia_client.print_worker_summary(True, ID))
    print
    print "Workers summary:"
    print workers_summary


def main():
    run_troia_on_data(COST_MATRIX, GOLD_SAMPLES, WORKERS_LABELS)


if __name__ == '__main__':
    main()
