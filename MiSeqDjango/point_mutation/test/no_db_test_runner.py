from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        print("Setting up no db")
        pass

    def teardown_databases(self, old_config, **kwargs):
        print("tearing down no db")
        pass