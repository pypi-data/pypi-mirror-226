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
        """
        supports retrieving secrets from plain text notes only!

        :param vault: vault to retrieve secrets from - must
        :param connections_prefix: prefix to look for connections (aka when trying to retrieve `conn_id`, will look in 1password for "connection_prefix/conn_id") , if None skip this backend when looking for connections
        :param variables_prefix: prefix to look for variables (aka when trying to retrieve `VARIABLE`, will look in 1password for "variables_prefix/VARIABLE") , if None skip this backend when looking for variables
        :param config_prefix: prefix to look for configurations (aka when trying to retrieve `config`, will look in 1password for "config_prefix/config") , if None skip this backend when looking for configurations
        :param kwargs:
        """
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

