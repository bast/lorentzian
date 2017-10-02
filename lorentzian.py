import sys
import os
import pytest
import click


def normalize(l):
    largest = max(l)
    for i in range(len(l)):
        l[i] = l[i] / largest
    return l


def get_lorentzians(xs_l, xs, ys, hwhm):
    ys_l = [0.0 for _ in xs_l]
    for i, x_l in enumerate(xs_l):
        for j, x in enumerate(xs):
            ys_l[i] = ys_l[i] + ys[j] / (1 + (((x_l - x) / hwhm)**2.0))
    return normalize(ys_l)


def get_xy(xs, ys, x_min, x_max, x_step, hwhm):

    if x_min is None:
        x_min = min(xs)
    if x_max is None:
        x_max = max(xs)

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


@click.command()
@click.option('--xy', help='Input data (energies and intensities of some sort).')
@click.option('--x-min', type=float, help='Min x value.')
@click.option('--x-max', type=float, help='Max x value.')
@click.option('--x-step', default=1.0, help='Stepsize in units of x values.')
@click.option('--hwhm', default=8.0, help='Lorentzian half-width at half-maximum in units of x values.')
def main(xy, x_min, x_max, x_step, hwhm):

    xs, ys = extract_numbers(xy)
    xs_l, ys_l = get_xy(xs, ys, x_min, x_max, x_step, hwhm)

    # write lorentzians to stdout
    for (x, y) in zip(xs_l, ys_l):
        print('{0} {1}'.format(x, y))


def test_get_xy():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    xs, ys = extract_numbers(os.path.join(dir_path, 'example/1.xy'))
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
