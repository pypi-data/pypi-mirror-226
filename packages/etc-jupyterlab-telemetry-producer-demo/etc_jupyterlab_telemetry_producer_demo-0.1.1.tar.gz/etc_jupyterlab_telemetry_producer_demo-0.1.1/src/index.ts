import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { NotebookPanel, INotebookTracker } from '@jupyterlab/notebook';
import { Widget } from '@lumino/widgets';
import { ITelemetryRouter } from 'telemetry-router';
// import { producerCollection } from './events';

import { requestAPI } from './handler';

const PLUGIN_ID = 'etc_jupyterlab_telemetry_producer_demo:plugin';

const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description:
    'A JupyterLab extension that generates telemetry data when users click on a button.',
  autoStart: true,
  requires: [ITelemetryRouter, INotebookTracker],
  activate: async (
    app: JupyterFrontEnd,
    telemetryRouter: ITelemetryRouter,
    notebookTracker: INotebookTracker
  ) => {
    const version = await requestAPI<string>('version');
    console.log(`${PLUGIN_ID}: ${version}`);

    // const config = await requestAPI<any>('config');

    const button = document.createElement('button');
    const buttonText = document.createTextNode('Click me');
    button.appendChild(buttonText);
    button.id = 'etc-jupyterlab-telemetry-producer-demo-button';

    const node = document.createElement('div');
    node.appendChild(button);

    notebookTracker.widgetAdded.connect(
      async (_, notebookPanel: NotebookPanel) => {
        notebookPanel.toolbar.insertAfter(
          'restart-and-run',
          'telemetry-producer-demo-button',
          new Widget({ node: node })
        );
        await notebookPanel.sessionContext.ready; // wait until session id is created
        await telemetryRouter.loadNotebookPanel(notebookPanel);
        node.addEventListener('click', async () => {
          const event = {
            eventName: 'ClickButtonEvent',
            eventTime: Date.now()
          };
          await telemetryRouter.publishEvent(event, true);
          window.alert('Telemetry data sent');
        });
        // producerCollection.forEach(producer => {
        //   if (config.activeEvents.includes(producer.id)) {
        //     new producer().listen(
        //       notebookPanel,
        //       telemetryRouter,
        //       config.logNotebookContentEvents.includes(producer.id)
        //     );
        //   }
        // });
      }
    );
  }
};

export default plugin;
