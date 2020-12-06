Ethylene, Benzene mixture
==============
A mixture of two small organic molecules using the *OPLSAA* force field.  In this example, the ethylene molecules were initially arranged in a rectangular lattice.  The benzene molecules were also arranged in a lattice, and were shifted to avoid overlap with the ethylene molecules.  *(Alternatively, you can create a single lattice and specify the number of ethelene and benzene molecules you want in it using moltemplate's "new random([],[])" command, which is explained in the manual.  This gives you more control over the concentration of each ingredient.  You can also use PACKMOL to create random mixtures of molecules.)*

#### Images

<img src="images/ethylene.jpg" width=110> <img src="images/plus.svg" height=80> <img src="images/benzene.jpg" width=110> <img src="images/rightarrow.svg" height=80> <img src="images/ethylene+benzene_t=0_LR.jpg" width=150> <img src="images/rightarrow.svg" height=80> <img src="images/ethylene+benzene_50bar_t=100000_LR.jpg" width=150>

The number of molecules, positions, and simulation box size can be controlled by editing the [system.lt file](moltemplate_files/system.lt).  The simulation contitions can be controlled by editing the [run.in.npt file](run.in.npt).


## Instructions

1) To build the files which LAMMPS needs, follow the instructions in:
[README_setup.sh](README_setup.sh)

2) To run LAMMPS with these files, follow these instructions:
[README_run.sh](README_run.sh)

(The instructions in "README_remove_irrelevant_info.sh" are optional.  *(If you notice a problem with this example, please [report it](../README.md).*)


### Customizing atomic charges

In most moltemplate examples, atomic charges (if present) are listed in
the 4th column of the "Data Atoms" section of each molecule's definition.
However *in moltemplate's implementation of OPLSAA,*
the atomic charges are determined by their @atom types
*(according to a lookup table located at the beginning of the
["oplsaa.lt" file](../../../moltemplate/force_fields/oplsaa.lt) file)*.
**This can be overridden.**
See [here](../README.md#Customizing-atomic-charges-for-OPLSAA-molecules)
for instructions how to customize atomic charges.