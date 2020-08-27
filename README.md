![Kimaris Logo](https://github.com/felipeboffnunes/Kimaris/blob/master/images/logo.png?raw=true)
# Kimaris

Kimaris is a tool that aids in the selection, visualization, and analysis of primary studies for systematic reviews.

<h3>Google Scholar</h3>
Search anything on google scholar, copy the url link and paste it on Kimaris. It will create the article instances on the system, and links between cited papers.

<h3>3D Network Graph</h3>
Kimaris provides a 3D network graph of all the articles found. By clicking each node it is possible to see the papers that cited it. It is possible to enter inside a node element to see more information and analyse it. If a node has a red circle, it means it is citing the one connected to it. Central nodes will be citing only nodes without a red circle.

3D Network Graph| Source 
--|--
![](https://github.com/felipeboffnunes/Kimaris/blob/master/images/graph3d.gif?raw=true) | ```get_figure(nodes, links, sizes_, name, standard, source)``` 
By using the igraph library, the system determines the coordinates for each node and link. Subsequently, it creates one ```go.Scatter3d``` trace for the nodes and one for the lines. The traces are added to a ```go.Figure``` and the graph is plotted in a ```dcc.Graph``` from Dash. | [Code](https://github.com/felipeboffnunes/Kimaris/blob/master/system/components/data/graph.py)

## Contributing ##

### Setup the development environment ###

The Python version used on development is 3.7.6. We strongly recommend using the pyenv virtualenv to create the development environment.

Besides all application being developed on Python, there are some additional modules like *language-check* which requires your computer has the *LanguageTool* and *Java 1.8 JDK* installed. Newer versions do not work due to a version check on language-check install module. *Make sure you have Java 1.8 installed before proceeding with steps below.*


If you are not familiar with pyenv or either don't have it installed, take a look here.

1. Make sure that you have the Python 3.7.6 version installed on your computer. If you don't have it, you can use the pyenv to install it:

```
pyenv install 3.7.6
```

2. After Python is installed, you can create the virtual environment for the project using:

```
pyenv virtualenv 3.7.6 kimaris
```

3. After the virtual environment is created, you will use the following to activate it:

```
pyenv activate kimaris
```

4. Now you can install the project dependencies with the following:

```
pip install -r requirements.txt
```

5. To run Kimaris:

```
python main.py
```

