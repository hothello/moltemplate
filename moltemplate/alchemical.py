#!/usr/bin/env python3

# Author: Otello M Roscioni (https://orcid.org/0000-0001-7815-6636)
# License: MIT License  (See LICENSE.md)
# Copyright (c) 2025
"""
Perform an alchemical transformation.

Before the remove_duplicate_atoms.py script is invoked in Moltemplate.sh,
look for specific atom
"""
g_program_name = __file__.split('/')[-1]  # ='alchemical.py'
g_date_str = '2025-12-21'
g_version_str = '0.1.0'

import sys
import re


def transform_data_atoms_template(template_path='Data Atoms.template', output_path='Data Atoms', assignments_path='ttree_assignments.txt'):
    """
    Replace the variables in the 'Data Atoms.template' using the assignments in 'ttree_assignments.txt',
    and write the result into 'Data Atoms'.
    """
    # Load variable bindings from ttree_assignments.txt
    var_bindings = {}
    try:
        with open(assignments_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) > 1:
                    var_bindings[parts[0]] = parts[1]
                    print(f"Substituting variable {parts[0]} with value {parts[1]}")
    
    except FileNotFoundError:
        sys.stderr.write(f'Warning: {assignments_path} not found. No variable substitution performed.\n')
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Substitute variables
    for var_name, value in var_bindings.items():
        text = text.replace(var_name, value)
    
    # Write the rendered text
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


def load_type_mappings(in_alchemical_path):
    """
    The content of the mapping file is based on the LAMMPS set command, as in:
    
    set atom mol1[2]/C1 type @atom:OPLSAA/99
    """
    mappings = []  # list of (pattern_str, type_value)
    with open(in_alchemical_path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()
            if len(parts) < 5:
                continue
            if parts[0] != 'set' or parts[1] != 'atom':
                continue

            key = parts[2]
            val = parts[4]
            mappings.append((key, val))
    return mappings


def make_regex_from_key(key):
    # Examples of keys: mol1[2]/C1, mol1[*]/C1, mol1[0][*]/C1, mol1[*][*]/C1, etc.
    # Replace every literal "[*]" token with a regex that matches a numeric index
    # while escaping all other characters.
    parts = key.split('[*]')
    if len(parts) == 1:
        key_regex = re.escape(key)
    else:
        pieces = []
        for i, part in enumerate(parts):
            pieces.append(re.escape(part))
            if i != len(parts) - 1:
                pieces.append(r'\[\d+\]')
        key_regex = ''.join(pieces)

    pattern = r'^\$/atom:' + key_regex + r'\b'
    return re.compile(pattern)


def update_data_atoms(data_atoms_path, mappings):

    # compile regexes
    compiled = [(make_regex_from_key(k), v) for k, v in mappings]

    out_lines = []
    changed = 0
    with open(data_atoms_path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n')
            new_line = line
            for rx, val in compiled:
                if rx.search(line):
                    parts = line.split()
                    if len(parts) >= 3:
                        parts[2] = val
                        new_line = ' '.join(parts)
                        changed += 1
                    break
            out_lines.append(new_line)

    if changed:
        with open(data_atoms_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(out_lines) + '\n')

    return changed


def main():

    in_path = sys.argv[1]
    data_path = sys.argv[2]

    mappings = load_type_mappings(in_path)
    if not mappings:
        print('Alchemical transformation failed\nNo mappings found in', in_path)
        sys.exit(0)

    changed = update_data_atoms(data_path, mappings)
    print(f'Alchemical transformation\nUpdated {changed} lines in {data_path}\n')
    
    # override the Data Atoms file.
    transform_data_atoms_template()

if __name__ == '__main__':
    main()

