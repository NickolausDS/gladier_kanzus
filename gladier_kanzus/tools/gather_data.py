

def ssx_gather_data(data):
    import re
    import os
    import json
    import shutil
    from zipfile import ZipFile
    trigger_name = data['trigger_name']
    sample_metadata = trigger_name.split('/')[-4:]
    assert len(sample_metadata) == 4 and trigger_name.endswith('cbf'), (
        'Invalid sample path, must run with end path resembling: "S9/nsp10nsp16/K/Kaleidoscope_15_22016.cbf"'
        f'Got: {trigger_name}'
    )

    # Gather metadata from path names
    run_name, protein, _, trigger_file = sample_metadata
    match = re.match(r'(\w+)_(\d+)_\d+.cbf', trigger_file)
    if not match:
        raise ValueError(f'Invalid trigger file: {trigger_file}, must match "Kaleidoscope_15_22016.cbf"')
    exp_name, exp_number = match.groups()

    # Get processing and image dirs
    run_dir = os.path.dirname(trigger_name)
    # processing_dir = os.path.join(run_dir, f'{exp_name}_processing')
    processing_dir = run_dir
    upload_dir = os.path.join(run_dir, f'{exp_name}_images')
    beamline_file = os.path.join(run_dir, f'beamline_run{exp_number}.json')
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    shutil.copyfile(beamline_file, os.path.join(upload_dir, os.path.basename(beamline_file)))

    # Fetch the list of ints that 'hit'.
    int_indices = []
    int_filenames = []
    cbf_indices = []
    for filename in os.listdir(processing_dir):
        # match int-0-Kaleidoscope_15_05189.pickle
        int_match = re.match(r'int-(\d+)-(\w+)_(\d+)_(\d+).pickle', filename)
        if int_match:
            int_filenames.append(filename)
            int_number, exp_name, beamline_run, int_index = int_match.groups()
            int_indices.append(int(int_index))
        else:
            # match idx-Kaleidoscope_15_00001_datablock.json
            cbf_match = re.match(r'idx-\w+_\d+_(\d+)_datablock.json', filename)
            if cbf_match:
                cbf_index = int(cbf_match.groups()[0])
                cbf_indices.append(cbf_index)
    batch_info = {
        'cbf_files': len(cbf_indices),
        'cbf_file_range': {'from': min(cbf_indices), 'to': max(cbf_indices)},
        'total_number_of_int_files': len(int_indices)
    }

    # Create a zip of all the int files
    with ZipFile(os.path.join(upload_dir, 'ints.zip'), 'w') as zipObj:
        for int_filename in int_filenames:
            zipObj.write(os.path.join(processing_dir, int_filename))

    # Fetch beamline metadata
    with open(beamline_file, 'r') as fp:
        beamline_metadata = json.load(fp)
    protein = beamline_metadata.get('user_input', {}).get('prot_name') or protein

    metadata = {
        'processing_dir': processing_dir,
        'upload_dir': upload_dir,
        'plot_filename': os.path.join(upload_dir, 'composite.png'),
        'int_indices': sorted(int_indices),
        'metadata': {
            'chip': exp_name,
            'experiment_number': exp_number,
            'run_name': run_name,
            'protein': protein,
            'trigger_name': trigger_name,
            'batch_info': batch_info,
        }
    }
    metadata['metadata'].update(beamline_metadata)
    metadata['metadata'].update(data.get('metadata', {}))
    return metadata