# solarsystem
Numerical simulation of the solar system

## Usage

1. Create a conda environment with all the required packages using the following commands:

       conda env create --file environment.yml
       conda activate solarsystem

2. Add your paths:
   * Rename `.env.sample` file to `.env`
   * Within the new file, replace the dummy path with your local path to export the graphics

3. Make sure the PYTHONPATH variable is set to your working directory  
       Windows:

       set "PYTHONPATH=C:\path\to\folder\solarsystem"

4. Execute the main file

       python scripts/main.py
