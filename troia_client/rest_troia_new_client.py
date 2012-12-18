import json
import time
import requests


class TroiaNewClient(object):
    ''' Base class providing wrappers for all REST request

        :param base_url: address at which Troia server is running
        :param timeout: timeout on requests to Troia server. *None* or <= 0 value indicates disabled timeout.
        :note: Job ID can be often omitted. In such case it is taken some default ID
    '''

    PRIORITY = 1.
    ''' Default priority '''

    def __init__(self, base_url, timeout=0.25):
        '''
        Initializes new client

        :param base_url: address at which Troia server is running
        :param timeout: timeout on requests to Troia server. *None* or <= 0 value indicates disabled timeout.
        '''
        self.url = base_url
        if not self.url.endswith('/'):
            self.url += '/'
        self.json_before = True
        if timeout <= 0.:
            self.timeout = None
        else:
            self.timeout = timeout

    def _jsonify(self, args):
        args = args or {}
        if not self.json_before:
            return args
        new_args = {}
        for k, v in args.iteritems():
            new_args[k] = json.dumps(v) if k != "id" else v
        return new_args

    def _do_request_get(self, name, args=None, jsonify=True):
        if jsonify:
            args = self._jsonify(args)
        print "GET", self.url + name, 'data = ', args
        req = requests.get(self.url + name, params=args, timeout=self.timeout)
        print req.content
        return json.loads(req.content)

    def _do_request_put(self, name, args=None, jsonify=True):
        if jsonify:
            args = self._jsonify(args)
        print "PUT", self.url + name, 'data = ', args
        req = requests.put(self.url + name, data=args, timeout=self.timeout)
        print req.content
        return json.loads(req.content)
    
    def _do_request_delete(self, name, args=None, jsonify=True):
        if jsonify:
            args = self._jsonify(args)
        print "DELETE ", self.url + name, 'data = ', args
        req = requests.delete(self.url + name, data=args, timeout=self.timeout)
        print req.content
        return json.loads(req.content)

    def _generate_miss_costs(self, labels, label):
        d = dict([(x, 1.) for x in labels if x != label])
        d[label] = 0.
        return d
    
    def _create_assign_label(self, worker, objectn, category):
        return {
            'workerName': worker,
            'objectName': objectn,
            'categoryName': category
        }

    def ping(self):
        return self._do_request_get("status/ping")
    
    def ping_db(self):
        return self._do_request_get("status/pingDB")

    def exists(self, idd=None):
        return self._do_request_get("exists", {'id': idd})
    
    def get_jobs(self):
        return self._do_request_get("jobs")
    
    def get_labels(self, idd):
        return self._do_request_get("jobs/{}/labels".format(idd))
    
    def get_label(self, idd, label_id=1):
        return self._do_request_get("jobs/{}/labels/{}".format(idd, label_id))
    
    def get_workers(self, idd):
        return self._do_request_get("jobs/{}/workers".format(idd))
    
    def get_worker(self, idd, worker_id="worker1"):
        return self._do_request_get("jobs/{}/workers/{}".format(idd, worker_id))
    
    def get_datums(self, idd):
        return self._do_request_get("jobs/{}/datums".format(idd))
    
    def get_datum(self, idd, datum_id="http://google.com"):
        return self._do_request_get("jobs/{}/datums/{}".format(idd, datum_id))
    
    def get_gold_datums(self, idd):
        return self._do_request_get("jobs/{}/goldDatums".format(idd))
    
    def get_evaluation_datums(self, idd):
        return self._do_request_get("jobs/{}/evaluationDatums".format(idd))
    
    def get_evaluation_datum(self, idd, evalutation_datum_id=1):
        return self._do_request_get("jobs/{}/evaluationDatums/{}".format(idd, evalutation_datum_id))
    
    def get_predicted_labels(self, idd, alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/datum".format(idd, alg))
    
    def get_predicted_label(self, idd, datum_id=1, alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/datum/{}".format(idd, alg, datum_id))
    
    def get_predicted_label_cost(self, idd, datum_id=1, alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/datum/{}/estimatedCost".format(idd, alg, datum_id))
    
    def get_predicted_worker_cost(self, idd, worker_id="worker1", alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/workers/{}".format(idd, alg, worker_id))
    
    def get_status(self, idd, job_id=1):
        return self._do_request_get("jobs/{}/status/{}".format(idd, job_id))
    
    
    def get_assigned_labels(self, idd):
        return self._do_request_get("jobs/{}/assignedLabels".format(idd))
    
    def put_assigned_labels(self, idd, labels=[
         ['worker1', 'http://sunnyfun.com', 'porn'],
         ['worker1', 'http://sex-mission.com', 'porn'],
         ['worker1', 'http://google.com', 'porn'],
         ['worker1', 'http://youporn.com', 'porn'],
         ['worker1', 'http://yahoo.com', 'porn'],
         ['worker2', 'http://sunnyfun.com', 'notporn'],
         ['worker2', 'http://sex-mission.com', 'porn'],
         ['worker2', 'http://google.com', 'notporn'],
         ['worker2', 'http://youporn.com', 'porn'],
         ['worker2', 'http://yahoo.com', 'porn'],
         ['worker3', 'http://sunnyfun.com', 'notporn'],
         ['worker3', 'http://sex-mission.com', 'porn'],
         ['worker3', 'http://google.com', 'notporn'],
         ['worker3', 'http://youporn.com', 'porn'],
         ['worker3', 'http://yahoo.com', 'notporn'],
         ['worker4', 'http://sunnyfun.com', 'notporn'],
         ['worker4', 'http://sex-mission.com', 'porn'],
         ['worker4', 'http://google.com', 'notporn'],
         ['worker4', 'http://youporn.com', 'porn'],
         ['worker4', 'http://yahoo.com', 'notporn'],
         ['worker5', 'http://sunnyfun.com', 'porn'],
         ['worker5', 'http://sex-mission.com', 'notporn'],
         ['worker5', 'http://google.com', 'porn'],
         ['worker5', 'http://youporn.com', 'notporn'],
         ['worker5', 'http://yahoo.com', 'porn']]):
        labels = [self._create_assign_label(w, o, c) for w, o, c in labels]
        return self._do_request_put("jobs/{}/assignedLabels".format(idd), {'labels': labels})
    
    
    def get_job(self, idd):
        return self._do_request_get("jobs/{}".format(idd))
    
    def put_job(self, idd=None):
        return self._do_request_put("jobs/", {"id": idd})
    
    def delete_job(self, idd):
        return self._do_request_delete("jobs/", {"id": idd})
    
    # TODO:
    def get_cost_matrix(self, idd):
        return self._do_request_get("jobs/{}/costMatrix".format(idd))
    
    def put_cost_matrix(self, idd, cm=None):
        return self._do_request_put("jobs/{}/costMatrix".format(idd), {'costMatrix': cm})
    
    
    def put_votes(self, idd, votes=None):
        return self._do_request_put("jobs/{}/votes".format(idd), {'votes': votes})
    
    
    def get_categories(self, idd):
        return self._do_request_get("jobs/{}/categories".format(idd))
    
    def put_categories(self, idd, categories=['porn', 'notporn']):
        categories = [{'name': c, 'prior': 1. / len(categories), 'misclassification_cost': self._generate_miss_costs(categories, c)}
            for c in categories]
        return self._do_request_put("jobs/{}/categories".format(idd), {'categories': categories})
    
    
    def put_calculate(self, idd, alg="ds"):
        return self._do_request_put("jobs/{}/prediction/{}/calculate".format(idd, alg), {})
    
    def put_reset(self, idd):
        return self._do_request_put("jobs/{}/reset".format(idd))

