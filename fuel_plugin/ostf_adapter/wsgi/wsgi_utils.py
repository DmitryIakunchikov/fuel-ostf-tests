#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import requests
from pecan import conf

from fuel_plugin.ostf_adapter.storage import engine
from fuel_plugin.ostf_adapter.nose_plugin import nose_discovery


def discovery_check(cluster):
    nailgun_api_url = 'api/clusters/{}'.format(cluster)
    cluster_meta = _request_to_nailgun(nailgun_api_url)

    #at this moment we need following deployment
    #arguments for cluster. The main inconvinience
    #is that needed data is spreaded in cluster_meta
    #dict which leads to such hoodoo
    cluster_deployment_args = set(
        [
            cluster_meta['mode'],
            cluster_meta['release']['operating_system']
        ]
    )

    session = engine.get_session()
    with session.begin(subtransactions=True):
        test_set = request.session.query(TestSet)\
            .filter_by(cluster_id=cluster)\
            .first()

        if not test_set:
            cluster_data = {
                'cluster_id': cluster,
                'deployment_tags': cluster_deployment_args
            }
            nose_discovery.discovery(deployment_info=cluster_data)


def _request_to_nailgun(api_url):
    nailgun_url = 'http://{0}:{1}/{2}'.format(
        conf.nailgun.host,
        conf.nailgun.port,
        api_url
    )

    req_ses = requests.Session()
    req_ses.trust_env = False

    response = req_ses.get(nailgun_url)

    return response.json()