#!/usr/bin/env python

import logging
import boto3
import requests
from datetime import datetime

domain = 'example.com'
subdomain = 'home'

def upsert(client, zone_id, rtype, value):
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes':[{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': fqdn,
                    'Type': rtype,
                    'TTL': 900,
                    'ResourceRecords':[{
                        'Value': value
                    }]
                }
            }]
        })


def main():
    my_matches = {'A': [], 'AAAA': []}
    updated = False

    client = boto3.client('route53')

    zone = client.list_hosted_zones_by_name(DNSName=domain)
    if len(zone['HostedZones']) != 1:
        logger.critical("Couldn't find configured domain in route53!")
        exit(1)
    zone_id = zone['HostedZones'][0]['Id']

    rrs = client.list_resource_record_sets(HostedZoneId=zone_id)
    for record in rrs['ResourceRecordSets']:
        if record['Name'] == fqdn and record['Type'] in ['A','AAAA']:
            my_matches[record['Type']] = map(lambda x: x['Value'], record['ResourceRecords'])

    try:
        ipv4 = requests.get('http://ipv4.icanhazip.com', timeout=15).text.rstrip()
        if ipv4 not in my_matches['A']:
            logger.info('Updating {0}: {1} -> {2}'.format(fqdn, my_matches['A'], ipv4))
            upsert(client, zone_id, 'A', ipv4)
            updated = True
    except:
        logger.warning('Couldn\'t detect your IPV4 address.')

    try:
        ipv6 = requests.get('http://ipv6.icanhazip.com', timeout=15).text.rstrip()
        if ipv6 not in my_matches['AAAA']:
            logger.info('Updating {0}: {1} -> {2}'.format(fqdn, my_matches['AAAA'], ipv6))
            upsert(client, zone_id, 'AAAA', ipv6)
            updated = True
    except:
        logger.warning('Couldn\'t detect your IPV6 address.')

    if updated:
        datestr = '"Last update {0}."'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M'))
        logger.info(datestr)
        upsert(client, zone_id, 'TXT', datestr)
    else:
        logger.info('"{0}" is current.'.format(fqdn))


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('dyndns53')
    logger.setLevel(logging.DEBUG)
    fqdn = '{0}.{1}.'.format(subdomain.strip('.'), domain.strip('.'))
    main()
