from onepasswordconnectsdk.client import new_client_from_environment
from airflow.secrets import BaseSecretsBackend


class OnePasswordSecretsBackend(BaseSecretsBackend):
    """
    Custom secrets backend for airflow. Intended to store connections/variables/configs in 1password vaults.
    Secrets should be stored as a plain note text.
    """

    def __init__(self,
                 vault: str,
                 connections_prefix: str = None,
                 variables_prefix: str = None,
                 config_prefix: str = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.vault = vault
        self.connection_prefix = connections_prefix
        self.variables_prefix = variables_prefix
        self.config_prefix = config_prefix

    @property
    def client(self):
        return new_client_from_environment()

    def get_conn_value(self, conn_id: str):
        if self.connection_prefix is None:
            return None

        secret_id = self.connection_prefix.rstrip('/') + '/' + conn_id
        return self._get_secret(secret_id)

    def get_variable(self, key: str):
        if self.variables_prefix is None:
            return None

        secret_id = self.variables_prefix.rstrip('/') + '/' + key
        return self._get_secret(secret_id)

    def get_config(self, key: str):
        if self.config_prefix is None:
            return None

        secret_id = self.config_prefix.rstrip('/') + '/' + key
        return self._get_secret(secret_id)

    def get_conn_uri(self, conn_id: str):
        return self.get_conn_value(conn_id)

    def _get_secret(self, secret_id: str):
        item = self.client.get_item(secret_id, self.vault)
        return item.fields[0].value

