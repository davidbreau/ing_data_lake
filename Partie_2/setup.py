import os, subprocess
from dotenv import load_dotenv

# Charger les variables depuis .env (secrets)
load_dotenv()

subprocess.run(f'source ../variables.sh', shell=True, executable='/bin/bash')

    # .env secrets
tenant_id = os.getenv('TENANT_ID')
sp_secondary_id = os.getenv('SP2_ID')  # ID du SP Keyvault
sp_secondary_secret = os.getenv('SP_PASSWORD')  # Secret du SP Keyvault
secret_name = os.getenv('KV_SECRET_NAME')

    # .sh variables
keyvault_name = os.getenv('KV_NAME')
storage_account_name = os.getenv('ADLS_NAME')
container_name = os.getenv('CNTNR_NAME')
sp_principal_id = os.getenv('SP1_ID')  # ID du SP Data Lake

    # URLs
keyvault_url = f"https://{keyvault_name}.vault.azure.net/"