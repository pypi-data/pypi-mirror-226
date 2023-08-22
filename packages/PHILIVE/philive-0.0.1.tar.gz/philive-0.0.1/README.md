# LISPI Documentation

## Introduction

`lispi` (Learning Interactive Slides and PIthon) is a Python package that provides a convenient way to convert Jupyter notebooks into interactive slides. It allows users to create engaging presentations with interactive elements directly from the slides.

## Installation

### Install from GitHub files
To install `lispi` package, you can clone the repository from GitHub and modify it to your liking and install on your system. Open your terminal and run the following command:

```
git clone https://github.com/B7M/lispi.git
```
Navigate to the directory containing the repository and follow these steps:

Make the build file:

```
python -m build
```
Once the build file is created successfully, you will see a folder named `dist` in the directory which contains `.whl` and '.tar.gz'. The name of the file will be the {package name}-{version number}-{py3-none-any.whl}. At this point run `pip install dist/{the .whl file}` command to install the package, here is an example of installing the package with `version 0.0.10`:

```
pip install dist/lispi-0.0.10-py3-none-any.whl
```


### Install from PyPI
To install `lispi` package, you can use pip, the Python package installer. Open your terminal and run the following command:

```
pip install lispi
```
## Configuration

Lispi provides several configuration options to customize the output slides. You can pass these options as arguments when creating an instance of the `lispi` class or running lispi from command line. Here are the available configuration options:

- `audio`: Specify if you wish the output without audio (default: "un-mute"). If you wish to generate the output without audio, you can pass "-m" as the value for this argument.
- `AI_assistant`: Specify if the output file should include an AI assistant (default: "AI prompt is included"). If you wish to generate the output without AI assistant, you can pass "-p" as the value for this argument.

Example:

```bash
lispi original_example -m -p
```

```python
generator = lispi(
    audio="False",
    aI_assistant="False"
)
```

## Usage
Preparation:
- Open a Jupyter notebook in Jupyter Lab or Jupyter Notebook.
- Add a markdown cell at the top of the notebook.
- Use level 1 heading to specify the title of the presentation and level 2 heading to specify the author and additional information.
- Make sure each cell is labeled with the write Slide Type (e.g. Slide, Sub-Slide, Fragment, Skip, Notes, etc.). This step is very important as it will determine the slides and the audio files that will be generated.
- While preparing the slides you may wish to receive input from the user. Lispi allows you to receive input from the user as simple text or as executable code.
To do so, you should use `<div><!--Course_Text--></div>` in any slides you want to receive simple text. This HTML line will not be visible in the output slides. It will be server as a target for lispi. Similarly, to receive executable code, you can use `<div><!--Course_Code--></div>` in any slides you want to receive executable code. The package will automatically convert the input cells into interactive cells in the output slides.

We included an example notebook in the package to show you how to prepare your notebook for lispi. To access the example notebook after installing lispi `pip install lispi` in command line execute the following line `lispi original_example` this will generate a folder `output` which will contain the example notebook file. You can use this notebook to see how you can prepare your notebook for lispi. You can also use this notebook to test the package.
### Command Line Interface
To use lispi, in your terminal follow these steps:
After installing the package, you can use the `lispi` command to convert your Jupyter notebook into interactive slides. In your terminal, navigate to the folder containing the notebooks and run the following command:

```lispi```

Upon running the command, the package will prompt you with help text to show you how you can use it. Enter the name of the file press enter. The package will convert the Jupyter notebook into interactive slides and save the output HTML file in the output folder in the same directory as html file and audio file folder. If you wish to convert the notebook named `original_example.ipynb`, you will enter `original_example` and press enter. If you wish to convert the notebook without audio, you can enter `lispi -m original_example` and press enter.

### Python
If you want to use lispi in your Python code, you can import the package and use it as a library. To use lispi, in python follow these steps:

1. Import the `Gen` class from the package:

   ```python
   import lispi
   ```
   or 

   ```python
    from lispi import *
   ```

2. Create an instance of the `Interactive Slides Generator` class:

   ```python
   generator = lispi.Gen
   ```

3. Specify the Jupyter notebook file you want to convert:

   ```python
   notebook_file = "path/to/your/notebook.ipynb"
   ```

4. Generate the interactive slides:

   ```python
   generator(notebook_file)
   ```

5. The package will convert the Jupyter notebook into interactive slides and save the output HTML file in the output folder in the same directory as html file and audio file folder.



## Examples

Here is an example that comes with the package. To run the example, in your terminal or python code provide 'original_example' as the file name.

(with audio and AI assistant)
```bash 
lispi original_example -p
```
or

```bash
lispi -i original_example -p
```

(without audio and AI assistant)
```bash
lispi -m original_example
```
And in python code:

```python
import lispi

# Create an instance of the lispi class
generator = lispi.Gen

# Specify the example notebook file
notebook_file = "original_example"

# Generate the interactive slides
generator(notebook_file)
```

## Conclusion

Lispi package provides a convenient way to convert Jupyter notebooks into interactive slides. It allows users to create engaging presentations with interactive elements easily. By following the installation and usage instructions outlined in this documentation, you can leverage this package to generate interactive slides from your Jupyter notebooks effortlessly.
