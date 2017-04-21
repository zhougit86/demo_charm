from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class ServerStorageProvides(RelationBase):
    # Every unit connecting will get the same information
    scope = scopes.SERVICE

    # Use some template magic to declare our relation(s)
    @hook('{provides:server-storage}-relation-{joined,changed}')
    def changed(self):
        # Signify that the relationship is now available to our principal layer(s)
        self.set_state('{server-storage}.available')

    @hook('{provides:server-storage}-relation-{departed}')
    def departed(self):
        # Remove the state that our relationship is now available to our principal layer(s)
        self.remove_state('{server-storage}.available')

    # call this method when passed into methods decorated with
    # @when('{relation}.available')
    # to configure the relation data
    def configure(self, sth):
        relation_info = {
            'server': hookenv.unit_get('app-name'),
            'anotherConfig': sth
        }
        self.set_remote(**relation_info)
