// import { NotebookPanel } from '@jupyterlab/notebook';
// // import { Cell, ICellModel } from '@jupyterlab/cells';
// import { ITelemetryRouter } from 'telemetry-router';
// // import { requestAPI } from './handler';

// class ClickButtonEventProducer {
//   static id: string = 'ClickButtonEvent';

//   listen(
//     notebookPanel: NotebookPanel,
//     router: ITelemetryRouter,
//     logNotebookContentEvent: boolean
//   ) {
//     const demoButton = document.getElementById(
//       'etc-jupyterlab-telemetry-producer-demo-button'
//     );
//     demoButton?.addEventListener('click', async () => {
//       const event = {
//         eventName: ClickButtonEventProducer.id,
//         eventTime: Date.now()
//       };
//       await router.publishEvent(event, logNotebookContentEvent);
//       window.alert('Telemetry data sent');
//     });
//   }
// }

// export const producerCollection = [ClickButtonEventProducer];
