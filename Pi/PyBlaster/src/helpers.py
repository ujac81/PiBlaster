"""helpers.py -- supporting routines for PyBlaster project

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""



suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def seconds_to_minutes(nsecs):
    if nsecs == 0:
        return ""
    return "%d:%02d" % (int(nsecs / 60), nsecs % 60)

