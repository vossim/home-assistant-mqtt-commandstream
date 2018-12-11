# home-assistant-mqtt-commandstream
MQTT Commandstream plugin for home-assistant (receives commands from mqqt to call services in home-assistant)

This component is similar to the mqtt_statestream component (https://www.home-assistant.io/components/mqtt_statestream/), but works the other way around. It takes commands from MQTT and changes the state of your components (turning lights on or off for example).

## Configuration

Download `mqtt_commandstream.py` and put it in a new directory named `custom_components` in your home-assistant configuration directory (for example `home-assistant/.home-assistant/custom_components/mqtt_commandstream.py`.

To enable MQTT Commandstream in Home Assistant, add the following section to your configuration.yaml file:
```yaml


# Example configuration.yaml entry
mqtt_commandstream:
  base_topic: "ha-commands/#"
```

### Configuration Variables

#### base_topic
*(string)(Required)* Base topic used to listen to for commands

## Operation

When a command gets sent to the configured base topic over MQTT, this component will call the service for the command sent (turning on a light or switch for example).

The topic structure matches the structure of the mqtt_statestream component (https://www.home-assistant.io/components/mqtt_statestream/). The topic for each entity should be different and should be in the form base_topic/domain/entity/state.

For example, with the example configuration above, if you want an entity called ‘light.master_bedroom_dimmer’ to be turned on, publish a message with the payload "on" to homeassistant/light/master_bedroom_dimmer/state.

## Missing features
* Includes and excludes (filter components which you don't want to have controlled over MQTT)
* Handle other attributes besides state on or off
