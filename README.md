# Blinking Vortex Simulation
This is a simulation of the Aref blinking vortex flow, a Hamiltonian 
system with one degree of freedom, written in Python. For more information 
on the theoretical background of this simulation, see the associated PDF 
[here](chaotic_mixing.pdf).

![ChaoticMixing](resources/Figure_1.png)

## Dependencies

This simulation uses matplotlib, numpy and opencv for simulation and video 
generation.

```shell
pip install -r requirements.txt
```

## Usage

```shell
python main.py --help
usage: main.py [-h] [-n N] [--mu MU] [--output OUTPUT] [--fps FPS] [--plot] [--duration DURATION]

A simulation of the Aref blinking vortex flow

optional arguments:
  -h, --help           show this help message and exit
  -n N                 The number of particles to simulate. Output density resolutionwill improve with larger numbers
  --mu MU              The simulation parameter. See documentation for description
  --output OUTPUT      The output file for the simulation video. If none is specified, no video will be generated.
  --fps FPS            The FPS of the generated video. Higher FPS will take longer to simulate
  --plot               Whether to show the mixing rate plot.
  --duration DURATION  The number of cycles to run the simulation.

```