# -*- coding: utf-8 -*-
import json
import unittest

from dsas import DSaS

class TestClient(unittest.TestCase):
    
    base_url = "http://localhost:8080/GetAnotherLabel/rest/"
    labels = [u"dog", "cat", "pig"]
    objects = [u"o_dog_0", u"o_dog_1", "o_cat_0", "o_pig_0", "o_pig_1"]
    prior = .314
    miss_class_cost = .141

    
    def _misclass_cost(self, label):
        d = dict([(x, self.miss_class_cost) for x in self.labels if x!=label])
        d[label] = 0.
        return d

    def _labels(self):
        return [(l, self._misclass_cost(l)) for l in self.labels]
    
    assigned_labels = [("worker"+str(i), objects[0], "dog") 
                                        for i in xrange(9)] +\
                    [("worker9", objects[0], "pig")]
    
    def setUp(self):
        self.dsas = DSaS(self.base_url)
        self.ID = "42"
        self.dsas.load_categories(self._labels(), self.ID)
    
    def tearDown(self):
        self.dsas.reset(self.ID)
    
    def testSetUp(self):
        self.assertTrue(self.dsas.exists(self.ID))
        self.assertFalse(self.dsas.exists(self.ID+"0"))
        
    def testPing(self):
        r = self.dsas.ping()
        prefix = "\"processing request at: "
        self.assertTrue(r.startswith(prefix))
        # I wanted to parse date but it its in some wired form so..
    
    def testReset(self):
        r = self.dsas.reset(self.ID)
        self.assertTrue(r.startswith("nullified the ds object"))
        self.assertFalse(self.dsas.exists(self.ID))
        
    def testExists(self):
        self.assertFalse(self.dsas.exists(self.ID+"0"))
        self.assertTrue(self.dsas.exists(self.ID))
    
    def testLoadCategories(self):
        ID=self.ID+"AnotherTestID"
        self.dsas.reset(ID)
        self.assertFalse(self.dsas.exists(ID))
        self.dsas.load_categories(self._labels(), ID)
        self.assertTrue(self.dsas.exists(ID))
        r = self.dsas.get_dawid_skene(ID)
        for k, v in r['categories'].iteritems():
            self.assertTrue(k in self.labels)
            self.assertEqual(v['name'], k)
            for n, c in v['misclassification_cost'].iteritems():
                print n, c ,k, v
                if n == k:
                    self.assertEqual(0., c)
                else:
                    self.assertEqual(self.miss_class_cost, c)
        self.dsas.reset(ID)
        
    
    def testLoadCosts(self):
        self.dsas.load_costs(
            [(u"dog","cat", 0.511)], self.ID)
        r = self.dsas.get_dawid_skene(self.ID)
        self.assertEqual(0.511,
                r['categories'][u'dog']['misclassification_cost']['cat'])

    def testAssignLabel(self):
        job = self.assigned_labels[0]
        self.dsas.load_worker_assigned_label(job[0], job[1], job[2], self.ID)
        r = self.dsas.get_dawid_skene(self.ID)
        resp = r['workers'][job[0]]['labels'][0]
        print job
        sorted(job)
        sorted(resp.values())
        self.assertEqual(sorted(job), sorted(resp.values()))

    def testAssignLabels(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        r = self.dsas.get_dawid_skene(self.ID)['workers']
        for job in self.assigned_labels:
            resp = r[job[0]]['labels'][0]
            self.assertEqual(sorted(job), sorted(resp.values()))
#            self.assertEqual(job, r[job['workerName']]['labels'][0])
    
    def testGoldLabel(self):
        item = (self.objects[0], u"dog")
        self.dsas.load_gold_label(item[0], item[1], self.ID)
        r = self.dsas.get_dawid_skene(self.ID)['objects']
        self.assertEqual(item[1], r[item[0]]["correctCategory"])
        self.assertTrue(r[item[0]]["isGold"])
        
    def testGoldLabels(self):
        gold_labels = [(self.objects[0], "dog"), (self.objects[-1], "pig")]
        self.dsas.load_gold_labels(gold_labels, self.ID)
        r = self.dsas.get_dawid_skene(self.ID)['objects']
        for item in gold_labels:
            self.assertTrue(r[item[0]]["isGold"])
            self.assertEqual(item[1], r[item[0]]["correctCategory"])
        
    def testMajorityVote(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        self.dsas.compute_blocking(3, self.ID)
        for _ in xrange(10):
            r = self.dsas.majority_vote(self.objects[0], self.ID)
            print r
#            self.assertEqual(self.objects[0].split("_")[1], r)
        self.fail()
    
    def testMajorityVotes(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        self.dsas.compute_blocking(3, self.ID)
        for _ in xrange(10):
            r = self.dsas.majority_votes(self.ID)
            print r
        self.fail()
    
    def testComputeBlocking(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        r1 = self.dsas.compute_blocking(1, self.ID)
        r3 = self.dsas.compute_blocking(3, self.ID)
        print r1, r3
        self.fail()
    
    def testPrintWorkerSummary(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        self.dsas.compute_blocking(10, self.ID)
        r = self.dsas.print_worker_summary(True, self.ID)
        self.assertEqual(10, r.count("Confusion Matrix:"))
        self.assertEqual(10, r.count("Number of Annotations: 1"))
        for l in self.assigned_labels:
            self.assertEqual(1, r.count("Worker: "+l[0]))
    
    def testPrintObjectsProbs(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        r = self.dsas.print_objects_probs([], self.ID)
        print r
        self.fail()

    def testObjectProbs(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        r = self.dsas.object_probs(self.objects[0], self.ID)
        from math import fsum
        self.assertAlmostEqual(1., fsum(r.values()), 10)
    
    def testPrintPriors(self):
        r = self.dsas.print_priors(self.ID)
        for l in r.splitlines():
            pass
            #self.assertIn(str(self.prior), l)
            # whe don't support priors
    
    def testClassPriors(self):
        r = self.dsas.class_priors(self.ID)
        r = json.loads(r)
        for _, v in r.iteritems():
            pass
            #self.assertEqual(self.prior, v)
            # whe don't support priors
    
    def testGetDawidSkene(self):
        self.dsas.load_worker_assigned_labels(self.assigned_labels, self.ID)
        self.dsas.compute_blocking(3, self.ID)
        gold_labels = [{"objectName":self.objects[0],"correctCategory":"dog"},
                    {"objectName":self.objects[-1],"correctCategory":"pig"},]
        self.dsas.load_gold_labels(gold_labels, self.ID)
        self.dsas.compute_blocking(3, self.ID)
        r = self.dsas.get_dawid_skene(self.ID)
        for k in ["workers", "objects", "id", "fixedPriors", "categories"]:
            self.assertTrue(k in r.keys())
        
        for l in self.assigned_labels:
            self.assertTrue(l[0] in r["workers"].keys())


if __name__ == '__main__':
    unittest.main()

