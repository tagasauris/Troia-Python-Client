import sys
import optparse
import logging
import time
import random

sys.path.append('../')
from dsas import DSaS

logging.basicConfig()
log = logging.getLogger("DSaS_Performance")
log.setLevel(logging.INFO)


url = 'http://localhost:8080/GetAnotherLabel/rest/'

ID = "ExtraSecretTestingID_42"
GOLDS_RATIO = 839008. / 2318028. / 2.
labels = ["correct", "incorrect"]

DUMP_FREQ = 200



def build_progressbar(name, **kwargs):
    """Return configured :class:`ProgressBar` instance"""
    from progressbar import Counter, ProgressBar, Timer, Percentage, ETA
    widgets = [name, Percentage(), ' ', ETA(), ' ',
            Counter(), ' results(', Timer(), ')']
    return ProgressBar(widgets=widgets, **kwargs)


def gen_items(opts):
    workers = ['worker_'+str(i) for i in xrange(opts.workers)]
    objects = ['object_labels_can_be_long_so_this_one_is_'+str(i)
                                                for i in xrange(opts.objects)]
    golds = ['gold_object_labels_is_also_long_'+str(i)
                        for i in xrange(int(opts.objects * opts.gratio / 2.))]
    return workers, objects, golds

def run_simulation(opts):
    dsas = DSaS(url)
#    dsas.reset(opts.ID)
    dsas.load_categories(
        [(labels[i],{labels[i]:0., labels[1-i]:1.}) for i in xrange(2)], opts.ID)
    workers, objects, golds = gen_items(opts)
    start_time = time.time()
    for i in build_progressbar("Simulation iterations")(xrange(opts.it)):
        if (i+1)%DUMP_FREQ == 0:
            current = time.time()
            duration = current - start_time
            log.info("Average speed: %s (labels/sec)                        ",
                                            str(float(DUMP_FREQ)/ duration))
            start_time = current
            
        r = random.random()
        if r < opts.gratio:
            obj = random.choice(golds)
            dsas.load_gold_label(obj, labels[1], opts.ID)
        else:
            obj = random.choice(objects)
        dsas.load_worker_assigned_label(random.choice(workers),
                                        obj, random.choice(labels), opts.ID)
        


def parse_commandline(argv):
    parser = optparse.OptionParser()
    parser.add_option("-w", "--workers", dest="workers", type="int",
            default=3000, help="Number of workers taking part in simulation")
    parser.add_option("-i", "--iterations", dest="it", type="int",
                      default=100000, help="Number of iterations to perform")
    parser.add_option("-o", "--objects", dest="objects", type="int",
            default=50000, help="Number of objects")
    parser.add_option("--id", dest="ID", default=ID, help="DSaS ID")
    parser.add_option("-r", "--gold_ratio", dest="gratio", type="float",
                default=GOLDS_RATIO, help="Ratio of gold labels in simulation")
    
    opts, args = parser.parse_args(argv)
    if args:
        log.warn("Ignored params: %s", args)
    return opts


def main(argv):
    opts = parse_commandline(argv)
    log.info("Prepared simulation with settings: iterations:%s; workers:%s; "
             "objects:%s; golds:%s",
            opts.it, opts.workers, opts.objects, int(opts.objects*opts.gratio))
    run_simulation(opts)


if __name__ == "__main__":
    main(sys.argv[1:])
