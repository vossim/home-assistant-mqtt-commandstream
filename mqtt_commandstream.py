import voluptuous as vol

from homeassistant.const import (CONF_DOMAINS, CONF_ENTITIES, CONF_EXCLUDE,
                                 CONF_INCLUDE, MATCH_ALL, ATTR_DOMAIN, ATTR_SERVICE,
                                 ATTR_SERVICE_DATA, EVENT_CALL_SERVICE)
from homeassistant.core import EventOrigin, callback
from homeassistant.components.mqtt import valid_subscribe_topic
from homeassistant.helpers.entityfilter import generate_filter
from homeassistant.helpers.event import async_track_state_change
from homeassistant.helpers.json import JSONEncoder
from homeassistant.loader import bind_hass
import homeassistant.helpers.config_validation as cv

CONF_BASE_TOPIC = 'base_topic'
DEPENDENCIES = ['mqtt']
DOMAIN = 'mqtt_commandstream'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_BASE_TOPIC): valid_subscribe_topic,
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    conf = config.get(DOMAIN, {})
    base_topic = conf.get(CONF_BASE_TOPIC)

    @bind_hass
    @callback
    def _event_receiver(topic, payload, qos):
        tosplit = topic[len(base_topic)-1:]
        if (tosplit.startswith("/")): tosplit = tosplit[1:]
        splitted = tosplit.split("/")
        if (len(splitted) >= 3):
            domain = splitted[0]
            entity = splitted[1]
            field = splitted[2]
            if (field == "state"):
                service = "turn_on" if (payload == "on") else "turn_off"
                service_data = {'entity_id': domain + "." + entity}
                hass.async_create_task(
                    hass.services.async_call(domain, service, service_data))
    await hass.components.mqtt.async_subscribe(base_topic, _event_receiver)

    return True
