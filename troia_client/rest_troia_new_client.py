import json
import requests


class TroiaNewClient(object):
    ''' Base class providing wrappers for all REST request

        :param base_url: address at which Troia server is running
        :param timeout: timeout on requests to Troia server. *None* or <= 0 value indicates disabled timeout.
        :note: Job ID can be often omitted. In such case it is taken some default ID
    '''

    PRIORITY = 1.
    ''' Default priority '''

    def __init__(self, base_url, idd="test", timeout=0.25):
        '''
        Initializes new client

        :param base_url: address at which Troia server is running
        :param timeout: timeout on requests to Troia server. *None* or <= 0 value indicates disabled timeout.
        '''
        self.url = base_url
        self.project_id = idd
        if not self.url.endswith('/'):
            self.url += '/'
        self.json_before = True
        if timeout <= 0.:
            self.timeout = None
        else:
            self.timeout = timeout
        
        self.put_job(idd)

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
        print req.status_code, req.content
        return json.loads(req.content)

    def _do_request_put(self, name, args=None, jsonify=True):
        if jsonify:
            args = self._jsonify(args)
        print "PUT", self.url + name, 'data = ', args
        req = requests.put(self.url + name, data=args, timeout=self.timeout)
        print req.status_code, req.content
        return json.loads(req.content)
    
    def _do_request_delete(self, name, args=None, jsonify=True):
        if jsonify:
            args = self._jsonify(args)
        print "DELETE ", self.url + name, 'data = ', args
        req = requests.delete(self.url + name, data=args, timeout=self.timeout)
        print req.status_code, req.content
        return json.loads(req.content)
    
    def _do_request_post(self, name, args=None, jsonify=True):
        if jsonify:
            args = self._jsonify(args)
        print "POST", self.url + name, 'data = ', args
        req = requests.post(self.url + name, data=args, timeout=self.timeout)
        print req.status_code, req.content
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
        
    def _create_cost(self, fromm, to, cost):
        return {
            'categoryFrom': fromm, 
            'categoryTo': to,
            'cost': cost}
        
    def _correct_label(self, obj, cat):
        return {
            'objectName': obj,
            'correctCategory': cat}

    def ping(self):
        return self._do_request_get("status/ping")
    
    def ping_db(self):
        return self._do_request_get("status/pingDB")

    def get_jobs(self):
        return self._do_request_get("jobs")
    
    def get_labels(self):
        return self._do_request_get("jobs/{}/labels".format(self.project_id))
    
    def get_label(self, label_id=1):
        return self._do_request_get("jobs/{}/labels/{}".format(self.project_id, label_id))
    
    def get_workers(self):
        return self._do_request_get("jobs/{}/workers".format(self.project_id))
    
    def get_worker(self, worker_id="worker1"):
        return self._do_request_get("jobs/{}/workers/{}".format(self.project_id, worker_id))
    
    def get_datums(self):
        return self._do_request_get("jobs/{}/datums".format(self.project_id))
    
    def get_datum(self, datum_id="http://google.com"):
        return self._do_request_get("jobs/{}/datums/{}".format(self.project_id, datum_id))
    
    
    def get_gold_datums(self):
        return self._do_request_get("jobs/{}/goldDatums".format(self.project_id))
    
    def put_gold_datums(self, labels=[['http://google.com', 'notporn']]):
        labels = [self._correct_label(obj, cat) for obj, cat in labels]
        return self._do_request_put("jobs/{}/goldDatums".format(self.project_id), {"labels": labels})
    
    
    def get_evaluation_datums(self):
        return self._do_request_get("jobs/{}/evaluationDatums".format(self.project_id))
    
    def get_evaluation_datum(self, evalutation_datum_id=1):
        return self._do_request_get("jobs/{}/evaluationDatums/{}".format(self.project_id, evalutation_datum_id))
    
    def get_predicted_labels(self, alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/datum".format(self.project_id, alg))
    
    def get_predicted_label(self, datum_id=1, alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/datum/{}".format(self.project_id, alg, datum_id))
    
    def get_predicted_label_cost(self, datum_id=1, alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/datum/{}/estimatedCost".format(self.project_id, alg, datum_id))
    
    def get_predicted_worker_cost(self, worker_id="worker1", alg="ds"):
        return self._do_request_get("jobs/{}/prediction/{}/workers/{}".format(self.project_id, alg, worker_id))
    
    def get_status(self, job_id=1):
        return self._do_request_get("jobs/{}/status/{}".format(self.project_id, job_id))
    
    
    def get_assigned_labels(self):
        return self._do_request_get("jobs/{}/assignedLabels".format(self.project_id))
    
    def put_assigned_labels(self, labels=[
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
        return self._do_request_put("jobs/{}/assignedLabels".format(self.project_id), {'labels': labels})
    
    
    def get_job(self):
        return self._do_request_get("jobs/{}".format(self.project_id))
    
    def put_job(self, idd):
        self.project_id = idd
        return self._do_request_put("jobs/", {"id": idd})
    
    def delete_job(self):
        return self._do_request_delete("jobs/", {"id": self.project_id})
    

    def get_cost_matrix(self):
        return self._do_request_get("jobs/{}/costs".format(self.project_id))
    
    def put_cost_matrix(self, cm=[
            ['porn', 'porn', 0],
            ['notporn', 'porn', 1],
            ['porn', 'notporn', 1],
            ['notporn', 'notporn', 0]]):
        costs = [self._create_cost(f, t, c) for f, t, c in cm]
        return self._do_request_put("jobs/{}/costs".format(self.project_id), {'costs': costs})
    

    def get_categories(self):
        return self._do_request_get("jobs/{}/categories".format(self.project_id))
    
    def put_categories(self, categories=['porn', 'notporn']):
        categories = [{'name': c, 'prior': 1. / len(categories), 'misclassification_cost': self._generate_miss_costs(categories, c)}
            for c in categories]
        return self._do_request_put("jobs/{}/categories".format(self.project_id), {'categories': categories})
    

    def post_compute(self):
        return self._do_request_post("jobs/{}/compute/".format(self.project_id), {'iterations': 20})
