import sys
import time


class Tools(object):

    def __init__(self):
        pass

    def show_process_bar(self, current_value, max_value):
        count = int((current_value + 1) / max_value * 40)
        sys.stdout.write('{0}{1}{2}\r'.format('Progress: [', '#' * count, '=' * (40 - count) + str(current_value + 1) + '/' + str(max_value) + ']'))
        sys.stdout.flush()
        if current_value + 1 == max_value:
            print('Progress: [' + '#' * 40 + str(current_value + 1) + '/' + str(max_value) + ']')

    def log(self, current_value, max_value, string):
        pass


#tools = Tools()
'''
for i in range(300):
    tools.show_process_bar(i, 300)
    time.sleep(0.01)
'''
#tools