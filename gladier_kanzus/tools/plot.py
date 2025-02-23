

def ssx_plot(data):
    """
    Plot the current list of ints so far. Data requires the following keys
        * xdim (int) X dimension for the plot
        * ydim (int) Y dimension for the plot
        * int_indices (list of ints) list of int 'hits' to light up on the plot
        * plot_name (path) full filename to save the plot
    """
    import numpy as np
    from matplotlib import pyplot as plt
    for dim in ('xdim', 'ydim'):
        if not isinstance(data.get(dim), int):
            raise ValueError(f'"{dim}" not provided as an integer: {data.get(dim)}')
    bad_ints = [int_index for int_index in data.get('int_indices', []) if not isinstance(int_index, int)]
    if bad_ints:
        raise ValueError(f'Got int indices which are not numbers: {bad_ints}')

    xdim, ydim = data['xdim'], data['ydim']
    lattice_counts = np.zeros(xdim*ydim, dtype=np.dtype(int))
    for index in data['int_indices']:
        lattice_counts[index] += 1
    lattice_counts = lattice_counts.reshape((ydim, xdim))
    # reverse the order of alternating rows
    lattice_counts[1::2, :] = lattice_counts[1::2, ::-1]

    # plot the lattice counts
    plt.figure(figsize=(xdim/10., ydim/10.))
    plt.axes([0, 0, 1, 1])  # Make the plot occupy the whole canvas
    plt.axis('off')
    plt.imshow(lattice_counts, cmap='hot', interpolation=None, vmax=4)
    plt.savefig(data['plot_filename'])
