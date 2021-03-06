from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class RackSwitchRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:rack-switch}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('anotherConfig'):
            # this unit's conversation has a port, so
            # it is part of the set of available units
            conv.set_state('{rack-switch}.available')

    @hook('{requires:rack-switch}-relation-{departed}')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{rack-switch}.available')

    def services(self):
        """
        Returns a list of available rack-switch services and their associated hosts
        and configs.
        The return value is a list of dicts of the following form::
            [
                {
                    'service_name': name_of_service,
                    'hosts': [
                        {
                            'hostname': address_of_host,
                            'anotherConfig': unit's config,
                        },
                        # ...
                    ],
                },
                # ...
            ]
        """
        services = {}
        for conv in self.conversations():
            service_name = conv.scope.split('/')[0]
            service = services.setdefault(service_name, {
                'service_name': service_name,
                'hosts': [],
            })
            host = conv.get_remote(
                'hostname') or conv.get_remote('private-address')
            port = conv.get_remote('anotherConfig')
            if host and port:
                service['hosts'].append({
                    'hostname': host,
                    'anotherConfig': port,
                })
        return [s for s in services.values() if s['hosts']]
