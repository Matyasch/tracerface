# Visualisation tool for BCC trace

[![Build Status](https://travis-ci.org/m-sch/tracerface.svg?branch=master)](https://travis-ci.org/m-sch/tracerface)
[![Python](https://img.shields.io/lgtm/grade/python/g/m-sch/tracerface.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/m-sch/tracerface/context:python)

An interactive web-app built with [dash][dash_docs] for call-graph visualisation in realtime, using [BCC][bcc_repo] trace.

![trace][trace_pic]

## Installation

Packages from iovisor are required to run as others may be outdated.
1. Get to the point where you can install iovisor packages, by following their [installation guide][bcc_install]
2. Install the ```python3-bcc``` package
3. Clone this repo

## Usage

Run ```run.sh``` with superuser privileges. The privileges are needed for bcc trace to access the kernel. Use the ```--help``` argument for more information about arguemnts.

For tests, run the ```run-tests.sh``` wrapper script. For integration tests too you have to run it with superuser privileges for the previous reasons.

### **Select what to trace on the GUI**

* Add the applications you wish to monitor on the **Realtime** tab.
* Add functions you wish to trace selecting an added binary under **Manage applications** and then clicking on **Manage functions**.
* You can also define traced parameters for a function by clicking the  **Manage parameters** button.

### **Or load from a file**

You can add applications, functions and parameters from a yaml file instead in the following format:

```yaml
app1:
  func1: {}
  func2:
    1: '%s'
    3: '%d'
app2:
  func3: {}
```

Check in the checkbox labeled with **Use config file instead** and then paste the path of the file into the appeared input box. Once you are done, start tracing.

### **Start tracing**
Click on the grey power button to start tracing. After it has turned green, run the application(s) and watch as the call-graph gets drawn on the screen.

### **Output analysis**

On the **Static** tab you can copy the output of a trace output to the given input box to draw the call-graph.

[dash_docs]: https://dash.plot.ly/
[bcc_repo]: https://github.com/iovisor/bcc
[bcc_install]: https://github.com/iovisor/bcc/blob/master/INSTALL.md#ubuntu---binary
[trace_pic]: https://github.com/m-sch/tracerface/blob/master/assets/trace.gif
