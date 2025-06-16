from ThreadSniffer import ThreadSniffer
from ThreadAnalyzer import ThreadAnalyzer
from Queue import Queue
from DataStat import Data


shared_queue = Queue()
shared_data = Data()
thread_sniffer = ThreadSniffer(shared_queue)
thread_analyzer = ThreadAnalyzer(shared_queue,shared_data)
print(2)
thread_sniffer.start()
thread_analyzer.start()