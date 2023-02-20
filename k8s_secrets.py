import os
import google.auth
from google.auth.transport.requests import Request
from hvac import Client

def get_vault_client():
    # Get Vault connection settings from Kubernetes environment variables
    try:
        vault_addr = os.environ['VAULT_ADDR']
        vault_role = os.environ['VAULT_ROLE']
        vault_mount = os.environ['VAULT_MOUNT']
        vault_path = os.environ['VAULT_PATH']
    except KeyError as e:
        raise Exception(f"Missing required environment variable: {e}")

    # Authenticate to GCP using the default service account
    try:
        creds, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    except Exception as e:
        raise Exception("Failed to obtain GCP credentials: {}".format(e))

    # Fetch a token for the Vault role
    if not creds.valid:
        try:
            creds.refresh(Request())
        except Exception as e:
            raise Exception("Failed to refresh GCP credentials: {}".format(e))

    vault_token = creds.token

    # Initialize a new Vault client
    client = Client(url=vault_addr, token=vault_token)

    # Authenticate to Vault using the GCP auth method
    try:
        client.auth.gcp.login(role=vault_role, mount_point=vault_mount)
    except Exception as e:
        raise Exception("Failed to authenticate to Vault using GCP auth method: {}".format(e))

    return client, vault_path

def fetch_secret(secret_key):
    # Fetch a secret from Vault
    client, vault_path = get_vault_client()
    try:
        response = client.secrets.kv.v2.read_secret_version(path=vault_path)
    except Exception as e:
        raise Exception("Failed to fetch secret from Vault: {}".format(e))

    # Extract the secret value from the response
    try:
        secret_value = response['data']['data'][secret_key]
    except KeyError as e:
        raise Exception(f"Secret key '{secret_key}' not found in Vault response: {e}")

    return secret_value

# Example usage:
try:
    my_secret = fetch_secret('my-secret-key')
    print("Secret value: {}".format(my_secret))
except Exception as e:
    print("Failed to fetch secret: {}".format(e))
