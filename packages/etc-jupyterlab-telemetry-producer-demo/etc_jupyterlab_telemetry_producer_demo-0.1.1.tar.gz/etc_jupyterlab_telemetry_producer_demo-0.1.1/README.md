# ETC JupyterLab Telemetry Producer Demo

A JupyterLab extension that generates telemetry data when users click on a button.

This extension is composed of a Python package named `etc_jupyterlab_telemetry_producer_demo`
for the server extension and a NPM package named `etc_jupyterlab_telemetry_producer_demo`
for the frontend extension.


- [ETC JupyterLab Telemetry Producer Demo](#etc-jupyterlab-telemetry-producer-demo)
  - [Getting started](#getting-started)
    - [Requirements](#requirements)
    - [Install](#install)
    - [Uninstall](#uninstall)
  - [How to implement a custom telemetry producer extension](#how-to-implement-a-custom-telemetry-producer-extension)
    - [Implement the extension from scratch](#implement-the-extension-from-scratch)
    - [Implement the extension based on the demo extension](#implement-the-extension-based-on-the-demo-extension)
    - [Development Workflow](#development-workflow)
      - [Client Side](#client-side)
      - [Server Side](#server-side)
    - [Useful links](#useful-links)
    - [Development uninstall](#development-uninstall)
    - [Packaging the extension](#packaging-the-extension)
  - [How to utilize the telemetry router extension to export telemetry data](#how-to-utilize-the-telemetry-router-extension-to-export-telemetry-data)
    - [Overview](#overview)
    - [Router Configuration](#router-configuration)
      - [Syntax](#syntax)
      - [Configuration file name \& path](#configuration-file-name--path)
      - [Example](#example)
  - [(Optional) Event Producer](#optional-event-producer)
  - [(Optional) Producer Configuration](#optional-producer-configuration)
    - [Configuration file name \& path](#configuration-file-name--path-1)
    - [Recommended Syntax](#recommended-syntax)
  - [Troubleshoot](#troubleshoot)



## Getting started

### Requirements

- JupyterLab >= 4.0.0

### Install

To install the extension, execute:

```bash
pip install etc_jupyterlab_telemetry_producer_demo
```

The telemetry router extension is automatically installed when the telemetry producer is installed.

Users need to write their own router configuration file (or use the configuration example) and place it in the correct directory before starting Jupyter Lab with the telemetry system.

Examples of router configurations are [here](#router-configuration).

Examples of producer configurations are [here](#optional-producer-configuration)

### Uninstall

To remove the extension, execute:

```bash
pip uninstall etc_jupyterlab_telemetry_producer_demo
```

## How to implement a custom telemetry producer extension
Set up development environment
```
conda create -n telemetry-demo --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=18 copier=8 jinja2-time jupyter-packaging git

conda activate telemetry-demo
```
### Implement the extension from scratch
Initialize from the extension template
```
mkdir etc_jupyterlab_telemetry_producer_demo

cd etc_jupyterlab_telemetry_producer_demo

copier copy --UNSAFE https://github.com/jupyterlab/extension-template .
```

Add `telemetry-router` as a dependency in `pyproject.toml`.

```toml
dependencies = [
    "jupyter_server>=2.0.1,<3",
    "telemetry-router"
]
```
Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.
```bash
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable etc_jupyterlab_telemetry_producer_demo
# Rebuild extension Typescript source after making changes
jlpm build
```
You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```
### Implement the extension based on the demo extension

```bash
# Clone the repo to your local environment
git clone https://github.com/educational-technology-collective/etc_jupyterlab_telemetry_producer_demo
# Change directory to the etc_jupyterlab_telemetry_producer_demo directory
cd etc_jupyterlab_telemetry_producer_demo
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable etc_jupyterlab_telemetry_producer_demo
# Rebuild extension Typescript source after making changes
jlpm build
# Or watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```
### Development Workflow

#### Client Side

- Make changes to the TypeScript client extension.
- Refresh the browser.
- Observe the changes in the running application.

#### Server Side

- Make changes to the Python server extension.
- Stop the Jupyter server.
- Start the Jupyter server.
- Observe the changes in the running application.

### Useful links

https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html

https://jupyter-server.readthedocs.io/en/latest/operators/configuring-extensions.html

https://github.com/educational-technology-collective/telemetry-router

https://github.com/educational-technology-collective/telemetry-producer

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable etc_jupyterlab_telemetry_producer_demo
pip uninstall etc_jupyterlab_telemetry_producer_demo
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `etc_jupyterlab_telemetry_producer_demo` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)

## How to utilize the telemetry router extension to export telemetry data
### Overview
The telemetry-router extension helps to monitor notebook states and export telemetry data to the console, local file, or any remote endpoints.

The telemetry router extension provides two methods to the producer extension, `loadNotebookPanel` and `publishEvent`.

`loadNotebookPanel` should be called first when activating the producer extension, to associate the telemetry events with the correct notebook panel before exporting data.

`publishEvent` could be called whenever we want to publish the event and export telemetry data to the desired endpoints. The `publishEvent` method takes two arguments, `eventDetail: Object` and `logNotebookContent: Boolean`. 

There is generally no limitation on the structure of the `eventDetail` object, as long as the information is wrapped in a serializable javascript object. `logNotebookContent` is optional and should be a `Boolean` object. Only if it is provided and is `true`, the router will send out the entire notebook content along with the event data.

When `publishEvent` is called, the router checks if the notebook panel is loaded properly, and then insert the notebook session ID, notebook file path, and the notebook content (when `logNotebookContent` is `true`) into the data. Then, the router checks the type of each exporter, processes and sends out the data one by one. If `env` and `params` are provided in the configuration file when defining the desired exporter, the router would extract the environment variables and add the params to the exported data. Finally, the router will assemble the responses from the exporters in an array and print the response array in the console.

### Router Configuration
The telemetry router extension is driven by the configuration file. In this way, users can define exporters easily without touching the extension code.

The telemetry-router extension provides 3 types of default exporters, `console` exporter, `file` exporter and `remote` exporter.

`console` exporter logs data in the console.

`file` exporter logs data into the local file indicated by `path`.

`remote` exporter posts data to the remote endpoint indicated by `url`.

The extension would extract the environment variable for each of the keys presented in `env`, and add the result to the data when exporting.

The extension would add `params` directly to data when exporting. This feature is useful when users want to post data to lambda functions and wants to have additional parameters.

#### Syntax
`type` and `id` are required for all exporters. 

`path` is required for file exporters only. 

`url` is required for remote exporters only.

`env` and `params` are optional. 

When the extension is being activated, a syntax check will be done first. Missing required fields would prevent Jupyter Lab from starting.

#### Configuration file name & path
Jupyter Server expects the configuration file to be named after the extension’s name like so: **`jupyter_{extension name defined in application.py}_config.py`**. In our case, the configuration file name is jupyter_telemetry_router_config.py.

Jupyter Server looks for an extension’s config file in a set of specific paths. **The configuration file should be saved into one of the config directories provided by `jupyter --path`.**

For more details, see https://jupyter-server.readthedocs.io/en/latest/operators/configuring-extensions.html.


#### Example
```python
## in jupyter_telemetry_router_config.py 
c.TelemetryRouterApp.exporters = [
    {
        'type': 'console',
        'id': 'ConsoleExporter',
    },
    {
        'type': 'file',
        'id': 'FileExporter',
        'path': 'log',
    },
    {
        'type': 'remote',
        'id': 'S3Exporter',
        'url': 'https://telemetry.mentoracademy.org/telemetry-edtech-labs-si-umich-edu/dev/test-telemetry',
        'env': ['WORKSPACE_ID']
    },
    {
        'type': 'remote',
        'id': 'MongoDBLambdaExporter',
        'url': 'https://68ltdi5iij.execute-api.us-east-1.amazonaws.com/mongo',
        'params': {
            'mongo_cluster': 'mengyanclustertest.6b83fsy.mongodb.net',
            'mongo_db': 'telemetry',
            'mongo_collection': 'dev'
        }
    },
]
```

## (Optional) Event Producer

There is no specific restrictions on when and where the telemetry router should be invoked. However, when writing complex event producer libraries, we recommend developers write an event producer class for each event, implement a `listen()` class method, and call the producer's `listen()` method when the producer extension is being activated. Within the `listen()` method, you may write the logic of how the extension listens to Jupyter signals or DOM events and how to use the `telemetryRouter.publishEvent()` function to export telemetry data. 

For detailed examples, see https://github.com/educational-technology-collective/telemetry-producer/blob/main/src/events.ts and https://github.com/educational-technology-collective/telemetry-producer/blob/main/src/index.ts#L31.

## (Optional) Producer Configuration
Unlike the telemetry router extension, using a configuration file is not required when implementing telemetry producer extensions. 

In this telemetry producer demo extension, there is only one event and actually does not need to go through the configuration. 

However, writing code on top of the configuration file might be very useful when the event library is complex, and when the telemetry system is going to be deployed under different contexts with different needs of telemetry events.
### Configuration file name & path

Jupyter Server expects the configuration file to be named after the extension’s name like so: jupyter\_{extension name defined in `application.py`}\_config.py. In our case, the configuration file name is `jupyter_etc_jupyterlab_telemetry_producer_demo_config.py`.

Jupyter Server looks for an extension’s config file in a set of specific paths. Use `jupyter --paths` command to list these paths and place the configuration file in any of the paths.

For more details, see https://jupyter-server.readthedocs.io/en/latest/operators/configuring-extensions.html.

### Recommended Syntax
We recommend developers to use the following configuration syntax when writing their own telemetry producers.

`activateEvents`: required. An array of the ids of the events. Only valid event producers (1. has an id associated with the event producer class, and 2. the event id is included in `activatedEvents`) will be activated.

`logNotebookContentEvents`: optional. An array of the ids of the events. Only valid event producers (1. has an id associated with the event producer class, and 2. the event id is included in `logNotebookContentEvents`) will have the router export the entire notebook content along with the event data.


```python
## in jupyter_etc_jupyterlab_telemetry_producer_demo_config.py 

c.ETCJupyterLabTelemetryProducerDemoApp.activeEvents = [
    'ClickButtonEvent',
]

c.ETCJupyterLabTelemetryProducerDemoApp.logNotebookContentEvents = [
    'ClickButtonEvent',
]
```


## Troubleshoot
If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
````

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```
