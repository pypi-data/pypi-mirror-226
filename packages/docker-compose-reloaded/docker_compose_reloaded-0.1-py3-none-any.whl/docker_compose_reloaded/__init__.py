from click import style
import click
import paho.mqtt.client as mqtt
import subprocess
import json
import threading
import json
import os
import time

config = {}

@click.group
def cli():
    """This script is meant to update your Docker stacks on event-based triggers.
    For info, see https://github.com/TheClockTwister/docker-compose-reloaded.
    """


@cli.command
@click.option("-f", "--file", help="Config file to use", default="/etc/config.json", type=str)
@click.option("-r", "--reload", help="Interval to reload config", default=5, type=int)
def run(file: str, reload: int):
    """Runs the watchdog in foreground."""

    print(f"Using config file {style(file, fg='yellow')}")
    global config
    
    def updateConfig():
        with open(file, "r") as config_file:
            global config
            config = json.load(config_file)

    def read_config():
        last_modified_time = 0
        while True:
            modified_time = os.path.getmtime(file)
            if modified_time != last_modified_time:
                last_modified_time = modified_time
                print("Config file changed. Reloading...")
                updateConfig()
            time.sleep(reload)

    # {"event": "update", "image": "debian:bullseye-slim"}
    def on_message(client, userdata, message):
        global config
        data = json.loads(message.payload.decode())
        for (composeFile, images) in config["triggers"].items():
            if data["image"] in images and data["event"] == "update":
                print(f"{style(data['image'], fg='green')} has changed, restarting {style(composeFile, fg='cyan')}...")
                subprocess.run(["docker", "compose", "-f", composeFile, "up", "-d", "--quiet-pull", "--pull", "always"])


    # read config and start config watcher for reload on changed config file
    updateConfig()
    threading.Thread(target=read_config, daemon=True).start()

    # Initialize MQTT client and subscribe to topics
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set(config["mqtt"]["username"], config["mqtt"]["password"])
    client.connect(config["mqtt"]["host"], config["mqtt"]["port"], 60)
    for topic in config["mqtt"]["topics"]:
        client.subscribe(topic)
        print(f"Subscribed to {style(topic, fg='yellow')}.")

    client.loop_forever()

if __name__ == "__main__":
    cli()
