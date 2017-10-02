import sys
import os
import pytest
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


def normalize(l):
    largest = max(l)
    for i in range(len(l)):
        l[i] = l[i] / largest
    return l


def get_lorentzians(xs_l, xs, ys, hwhm):
    ys_l = [0.0 for x in xs_l]
    for i in range(len(xs_l)):
        for j in range(len(xs)):
            ys_l[i] = ys_l[i] + ys[j] / (1 + (((xs_l[i] - xs[j]) / hwhm)**2.0))
    return normalize(ys_l)


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


def test_get_xy():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    xs, ys = extract_numbers(os.path.join(dir_path, 'example/xy.stick'))
    xs_l, ys_l = get_xy(xs, ys, 1000.0, 1010.0, 1.0, 8.0)
    xs_ref = [1000.0,
              1001.0,
              1002.0,
              1003.0,
              1004.0,
              1005.0,
              1006.0,
              1007.0,
              1008.0,
              1009.0,
              1010.0]
    ys_ref = [0.9254792082596345,
              0.9308467383851173,
              0.9427902142236957,
              0.959026667736806,
              0.9763696378531916,
              0.991143768020725,
              0.9998484853505051,
              1.0,
              0.9908763518591084,
              0.9737925731302556,
              0.9517298450973274]
    assert xs_l == pytest.approx(xs_ref)
    assert ys_l == pytest.approx(ys_ref)


if __name__ == '__main__':
    main()
