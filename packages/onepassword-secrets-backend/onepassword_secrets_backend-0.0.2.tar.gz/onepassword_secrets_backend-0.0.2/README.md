# onepassword_secrets_backend
Custom 1password secrets backend for airflow. Intended to store connections/variables/configs in 1password vaults.

Secrets should be stored in 1password as a plain note text!

### To use in airflow set the following environment variables:

`AIRFLOW__SECRETS__BACKEND`=onepassword_secrets_backend.OnePasswordSecretsBackend

`AIRFLOW__SECRETS__BACKEND_KWARGS` : kwargs for the Backend class, see class documentation for details

`OP_CONNECT_TOKEN` : one password connect server token

`OP_CONNECT_HOST` : one password connect server host