# Visualisation tool for BCC trace

[![Build Status](https://travis-ci.org/Matyasch/tracerface.svg?branch=master)](https://travis-ci.org/Matyasch/tracerface)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Matyasch/tracerface.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Matyasch/tracerface/context:python)

An interactive web-app built with [dash][dash_docs] for call-graph visualisation in realtime, using [BCC][bcc_repo] trace.

![trace][trace_pic]

## Installation

Packages from iovisor are required to run as others may be outdated.
1. Install the `bcc-tools` package, by following the BCC [installation guide][bcc_install]
2. Install the `python3-bcc` package
3. Clone this repo
> It's important to install `bcc-tools` instead of `bpfcc-tools` as only the former supports python3

## Usage

Run `run.sh` with superuser privileges. The privileges are needed for bcc trace to access the kernel. Use the `--help` argument for more information about arguemnts.

Run the `run-tests.sh` script for tests. For integration tests too you have to run it with superuser privileges for the previous reasons.

## Features

### **Select what to trace on the GUI**

* Add binaries or built-in functions you wish to monitor.
* Set functions you wish to trace by managing functions of an application.
* Define traced parameters for a function by managing parameters.

### **Load setup from file**

You can add binaries, functions and parameters from a yaml file instead:

```yaml
/path/to/app1:
  func1: {}
  func2:
    1: '%s' # position and format of parameter
    3: '%d'
/path/to/app2:
  func3: {}
/path/to/app3: {} # need to set functions to trace in UI
```

If you want to trace built-in functions, you can write them as if they were functions of a binary, but on the binary level:

```yaml
/path/to/app:
  func: {}
do_sys_open: {} # built-in functions do not need path
```

### **Start tracing**
Click on the grey power button to start tracing. After it turns green, the functions are getting traced.

### **Load output of BCC trace run**

Create the interactive call-graph of a given bcc trace output

[dash_docs]: https://dash.plot.ly/
[bcc_repo]: https://github.com/iovisor/bcc
[bcc_install]: https://github.com/iovisor/bcc/blob/master/INSTALL.md#ubuntu---binary
[trace_pic]: https://github.com/Matyasch/tracerface/blob/master/assets/trace.gif
