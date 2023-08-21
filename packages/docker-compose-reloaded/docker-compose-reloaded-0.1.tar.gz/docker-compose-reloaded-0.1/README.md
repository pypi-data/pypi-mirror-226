# docker-compose-reloaded
A python CLI tool to update stacks on event triggers like MQTT

> [!WARNING]  
> This project is just out of the oven and will introduce some breaking changes soon.

## Installation
The script can be installed via pip:
```bash
pip install docker-compose-reloaded
```

## Configuration

> [!NOTE]
> The default config path is `/etc/docker-compose-reloaded/config.json`.
> But you can change it with the `-f` option.

You can give it a quick start and use the [example config](./examples/mqtt.json),
which will restart some docker stacks if certain images are updated. The event
trigger in this exampel is an MQTT message to one of the subscribed topics.

### List of configuration options
| Option | Long Option | Description |
|--------|-------------|-------------|
| `-f`   | `--file`    | Config file path
| `-r`   | `--reload`  | Tims [s] to check for config changes


## Fire it up!
With the config present, you can just run
```bash
dcr run
```
or (if you have a custom config location)
```bash
dcr run -f /path/to/your/config.json
```