import sys
from optparse import OptionParser, OptionGroup


def parse_input(argv):

    parser = OptionParser(usage='./%prog --xy=example/xy.stick > example/output')

    group = OptionGroup(parser, 'Basic options')
    group.add_option('--xy',
                     action='store',
                     default=None,
                     help='Input data (energies and intensities of some sort)')
    group.add_option('--min',
                     type='float',
                     action='store',
                     default=1000.0,
                     help='Min x value [default: %default]')
    group.add_option('--max',
                     type='float',
                     action='store',
                     default=1800.0,
                     help='Max x value [default: %default]')
    group.add_option('--step',
                     type='float',
                     action='store',
                     default=1.0,
                     help='Stepsize in units of x values [default: %default]')
    group.add_option('--hwhm',
                     type='float',
                     action='store',
                     default=8.0,
                     help='Lorentzian half-width at half-maximum in units of x values [default: %default]')
    parser.add_option_group(group)

    if len(argv) == 1:
        # user has given no arguments and we are not in a test subdir: print help and exit
        print(parser.format_help().strip())
        sys.exit()

    return parser.parse_args()

#-------------------------------------------------------------------------------

def normalize(l):
    largest = max(l)
    for i in range(len(l)):
        l[i] = l[i]/largest
    return l

#-------------------------------------------------------------------------------

def get_lorentzians(x_l, f_l, i_l, hwhm):

    y_l = []
    for i in range(len(x_l)):
        y_l.append(0.0)
    for i in range(len(x_l)):
        for j in range(len(f_l)):
            y_l[i] = y_l[i] + i_l[j]/(1 + (((x_l[i] - f_l[j])/hwhm)**2.0))

    return normalize(y_l)

#-------------------------------------------------------------------------------

def get_xy(xs, ys, x_min, x_max, x_step, hwhm):

    # create list of x values
    xs_l = []
    x = x_min
    xs_l.append(x)
    while True:
        x += x_step
        if x > x_max:
            break
        else:
           xs_l.append(x)

    ys_l = get_lorentzians(xs_l, xs, ys, hwhm)

    return xs_l, ys_l


def extract_numbers(file_name):
    xs = []
    ys = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            xs.append(float(line.split()[0]))
            ys.append(float(line.split()[1]))
    return xs, ys


def main():

    (options, args) = parse_input(sys.argv)

    xs, ys = extract_numbers(options.xy)
    xs_l, ys_l = get_xy(xs, ys, options.min, options.max, options.step, options.hwhm)

    # write lorentzians to stdout
    for (x, y) in zip(xs_l, ys_l):
        print('{0} {1}'.format(x, y))


if __name__ == '__main__':
    main()
