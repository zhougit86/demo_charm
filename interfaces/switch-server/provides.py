from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class SwitchServerProvides(RelationBase):
    # Every unit connecting will get the same information
    scope = scopes.GLOBAL

    # Use some template magic to declare our relation(s)
    @hook('{provides:switch-server}-relation-{joined,changed}')
    def changed(self):
        # Signify that the relationship is now available to our principal
        # layer(s)
        self.set_state('{switch-server}.available')

    @hook('{provides:switch-server}-relation-{departed}')
    def departed(self):
        # Remove the state that our relationship is now available to our
        # principal layer(s)
        self.remove_state('{switch-server}.available')

    # call this method when passed into methods decorated with
    # @when('{relation}.available')
    # to configure the relation data
    def configure(self, sth):
        relation_info = {
            'switch': hookenv.unit_get('app-name'),
            'anotherConfig': sth
        }
        self.set_remote(**relation_info)
