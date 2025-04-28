class PrimaryReplicaRouter:
    """
    Router directing:
    - all read operations to 'replica'
    - all write operations to 'default'
    """

    def db_for_read(self, model, **hints):
        """
        Reads go to replica.
        """
        return "replica"

    def db_for_write(self, model, **hints):
        """
        Writes go to default (primary).
        """
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between objects in the primary/replica.
        """
        db_list = ("default", "replica")
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure all migrations go to the primary (default) database.
        """
        return db == "default"
