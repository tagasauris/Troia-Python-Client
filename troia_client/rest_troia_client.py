import json

import requests


class TroiaClient(object):

    PRIORITY = 1.

    def __init__(self, base_url, timeout=0.25):
        self.url = base_url
        if not self.url.endswith('/'):
            self.url += '/'
        self.json_before = True
        if timeout <= 0.:
            self.timeout = None
        else:
            self.timeout = timeout

    def jsonify(self, args):
        args = args or {}
        if not self.json_before:
            return args
        new_args = {}
        for k, v in args.iteritems():
            new_args[k] = json.dumps(v)
        return new_args

    def _do_request_get(self, name, args=None):
        args = self.jsonify(args)
        req = requests.get(self.url + name, params=args, timeout=self.timeout)
        return req.content

    def _do_request_post(self, name, args=None):
        args = self.jsonify(args)
        req = requests.post(self.url + name, data=args, timeout=self.timeout)
        return req.content

    def ping(self):
        return self._do_request_get("ping")

    def reset(self, idd=None):
        return self._do_request_get("reset", {'id': idd})

    def exists(self, idd=None):
        r = self._do_request_get("exists", {'id': idd})
        return r.lower() in ['true', 't']

    def _generate_miss_costs(self, labels, label):
        d = dict([(x, 1.) for x in labels if x != label])
        d[label] = 0.
        return d

    def load_categories_def_costs(self, categories, idd=None):
        categories = [{'name':c, 'prior':self.PRIORITY,
             'misclassification_cost':self._generate_miss_costs(categories, c)}
                                                for c in categories]
        return self._do_request_post("loadCategories",
                                {'id': idd, 'categories': categories})

    def load_categories(self, categories, idd=None):
        '''costs should be iterable with iterables in form:
        (name, dict-misclassification_cost { class_ : cost })
        priority is not used in this version
        '''
        categories = [
            {'name':c, 'prior':self.PRIORITY, 'misclassification_cost':d}
                                                for c, d in categories]
        return self._do_request_post("loadCategories",
                                {'id': idd, 'categories': categories})

    def load_costs(self, costs, idd=None):
        return self._do_request_post("loadCosts",
                                {'id': idd, 'costs': costs})

    def _create_assign_label(self, worker, objectn, category):
        return {'workerName': worker, 'objectName': objectn,
                                            'categoryName': category}

    def load_worker_assigned_label(self, worker, objectn, category, idd=None):
        data = self._create_assign_label(worker, objectn, category)
        return self._do_request_post("loadWorkerAssignedLabel",
                                        {'id': idd, 'data': data})

    def load_worker_assigned_labels(self, data, idd=None):
        data = [self._create_assign_label(w, o, c) for w, o, c in data]
        return self._do_request_post("loadWorkerAssignedLabels",
                                        {'id': idd, 'data': data})

    def _create_gold_label(self, objectn, category):
        return {"objectName": objectn, "correctCategory": category}

    def load_gold_label(self, objectn, category, idd=None):
        data = self._create_gold_label(objectn, category)
        return self._do_request_post("loadGoldLabel", {'id': idd, 'data': data})

    def load_gold_labels(self, data, idd=None):
        data = [self._create_gold_label(on, c) for on, c in data]
        return self._do_request_post("loadGoldLabels",
                                         {'id': idd, 'data': data})

    def majority_vote(self, objectName, idd=None):
        return self._do_request_get("majorityVote",
                                        {'id': idd, 'objectName': objectName})

    def majority_votes(self, idd=None):
        return json.loads(self._do_request_get("majorityVotes", {'id': idd}))

    def compute_blocking(self, iterations, idd=None):
        return self._do_request_get("computeBlocking",
                                        {'id': idd, 'iterations': iterations})

    def print_worker_summary(self, verbose, idd=None):
        return self._do_request_get("printWorkerSummary",
                                        {'id': idd, 'verbose': verbose})

    def print_objects_probs(self, entropy, idd=None):
        return self._do_request_get("printObjectsProbs",
                                        {'id': idd, 'entropy': entropy})

    def object_probs(self, obj, idd=None):
        return json.loads(
                self._do_request_get("objectProbs", {'id': idd, 'object': obj}))

    def print_priors(self, idd=None):
        return self._do_request_get("printPriors", {'id': idd})

    def class_priors(self, idd=None):
        return self._do_request_get("classPriors", {'id': idd})

    def get_dawid_skene(self, idd=None):
        return json.loads(self._do_request_get("getDawidSkene", {'id': idd}))
