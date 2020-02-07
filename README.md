# Visualisation tool for BCC trace
An interactive web-app tool built with [dash](https://dash.plot.ly/) for call-graph visualisation using the [BCC](https://github.com/iovisor/bcc) trace tool.

## Installation

Install ```python3-bcc``` package and clone this repo.

## Usage

Run ```run.sh``` with superuser privileges. The privileges are needed for bcc trace to access the kernel. Use the ```--help``` argument for more information.

For tests, run the ```run-tests.sh``` wrapper script. For integration tests too you have to run it with superuser privileges for the previous reasons.

### **Realtime tracing with UI**

* On the **Realtime** tab add the applications which contain the functions you wish to trace.
* Add functions to an added application with **Manage functions** after selecting. On the appearing window, add the functions you would like to trace.
* You can also define traced parameters for a function with **Manage parameters** after selecting it.
* When you are done setting up, turn on tracing with the power button.
* Once you are finished tracing, turn off tracing by clicking the power button again.

### **Realtime tracing with config file**

If you think using the UI takes too much time, you can load the applications, functions and parameters from a yaml file instead using the following format:

```yaml
app1:  # application
  - func1  # function we would like to trace
  - func2: # function with parameters
    - ’%s’  # list of parameters in order starting from the first one
    - ’%d’
app2:  # another app
  - func3
```
Check in the checkbox labeled with **Use config file instead** and then paste the path of the file into the appeared input box. Once you are done, start tracing.

### **Output analysis**

On the **Static** tab you can copy the output of a trace output to the given input box to draw the call-graph.

### **Play around**

Adjust coloring, search for functions and change the spacing of the graph as you wish with the help of the **Utilities** tab.

The elements of the graph are all clickable which makes a small information panel appear about the given element. Furthermore the elements are freely movable and you can zoom the graph in and out.
