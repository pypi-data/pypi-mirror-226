"""
Module containing functions to interact with the PagerDuty service.
Created by: Mauricio Ayales [mayales@snapfinance.com]
Created at: 2023-08-18
"""

import requests
import json
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
logging.getLogger().setLevel('INFO')

def create_pagerduty_incident(message, integration_key, source, href, component=None, custom_details={}, link_text='LOG_URL', client=None, severity='error'):
    """

    Args:
        message: A high-level, text summary message of the event. Will be used to construct an alert's description.
        integration_key: service key
        source: Specific human-readable unique identifier, such as a hostname, for the system having the problem.
        component: The part or component of the affected system that is broken.	"mysql", "presto"
        custom_details: Extra info in a json format
        link_text: name of the link
        href: link to log
        client: Airflow, AWS, etc...
        severity: How impacted the affected system is. {info, warning, error, critical}

    Returns:

    """
    url = 'https://events.pagerduty.com/v2/enqueue'
    headers = {'Content-type': 'application/json'}
    payload = {
        'routing_key': integration_key,
        'event_action': 'trigger',
        'payload': {
            'summary': message,
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'severity': severity,
            'component': component,
            'custom_details': custom_details,
        },
        'links': [{
            'href': href,
            'text': link_text
            }],
        'client': client,
    }

    return logging.info('There is no configuration integration key to create an incident.') if integration_key is None \
        else requests.post(url, headers=headers, data=json.dumps(payload))
