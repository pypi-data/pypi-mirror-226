# This file should be saved into one of the config directories provided by `jupyter lab --path`.

c.TelemetryRouterApp.exporters = [
    {
        'type': 'console',
        'id': 'ConsoleExporter',
    },
    {
        'type': 'file',
        'id': 'FileExporter',
        'path': 'telemetry-log',
    },
    {
        'type': 'remote',
        'id': 'S3Exporter',
        'url': 'https://telemetry.mentoracademy.org/telemetry-edtech-labs-si-umich-edu/dev/test-telemetry',
        'env': ['WORKSPACE_ID']
    },
]