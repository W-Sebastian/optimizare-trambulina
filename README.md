# Structural Optimization in HyperStudy

The repository contains a HyperStudy project for driving the optimization process and two python files for computing and linking with the HyperStudy.

The HyperStudy project already contains results for two optimization processes, one with a genetic algorithm and the other with a multiobjective search. They both have around 4000 iterations.

## How to use

Open the `two_optimizations.hstudy` in Altair HyperStudy. The setup will be out of date but the two runs should be valid. `Optimization_genetic_4300i` contains the results for the genetic algorithm and the `Optimization_search` contains the results for the multiobjective search.

In order to run it there are some prerequisite steps that must be completed:

1. Install (if not already installed) Python 3.8 or later;
2. Open the project in HyperStudy;
3. Go to Edit -> Solver Scripts and change the path to python.exe for the script "Python_VEnv"; this lets HyperStudy know what executable to run on each iteration;
4. Go to Setup -> Define Models -> Solver Input Arguments and change the arguments to "path_to_hyperstudy.py ${file}" (example: "C:\repo\hyperstudy.py ${file}"; this step ensures that the python file is called with the input file as the first argument.

Now the setup is prepared for testing the model and then optimizing it.

## How it works

The python script expects an input file with arguments for the model. On each line, the file contains: the shell thickness, the core thickness, the plate length, the shell material and the core material. File example:

```
0.01000
0.09000
3.50000
Aluminium
DivinycellH100
```

The python scripts solves the model with these parameters and writes in output: dispalcement, maximum displacement, core stress, maximum core stress, shell stress, maximum shell stress, cost of materials and total mass. Example of output file:

```
12013148688.75901
294.19950
29.58165
0.24000
10296982.50000
40.00000
0.22
0.11025
```

In HyperStudy in the "Define Input Variables" and "Define Output Responses" these parameters are defined and optimization goals are added.
