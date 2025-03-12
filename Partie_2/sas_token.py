from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, generate_container_sas
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_sp_principal_secret():
    """Récupère le secret du SP Principal depuis Key Vault en utilisant le SP Secondaire"""
    # Authentification avec le SP Secondaire
    credential = ClientSecretCredential(
        tenant_id=os.getenv('TENANT_ID'),
        client_id=os.getenv('SP2_ID'),
        client_secret=os.getenv('SP_PASSWORD')
    )
    
    # Client Key Vault
    keyvault_url = f"https://{os.getenv('KV_NAME')}.vault.azure.net/"
    secret_client = SecretClient(vault_url=keyvault_url, credential=credential)
    
    # Récupérer le secret du SP Principal
    return secret_client.get_secret(os.getenv('KV_SECRET_NAME')).value

def generate_sas_token(expiry_hours=1):
    """Génère un SAS Token en utilisant le SP Principal"""
    # Récupérer le secret du SP Principal
    sp_principal_secret = get_sp_principal_secret()
    
    # Authentification avec le SP Principal
    credential = ClientSecretCredential(
        tenant_id=os.getenv('TENANT_ID'),
        client_id=os.getenv('SP1_ID'),
        client_secret=sp_principal_secret
    )
    
    # Client Blob Storage
    account_url = f"https://{os.getenv('ADLS_NAME')}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url, credential=credential)
    
    # Générer User Delegation Key
    start_time = datetime.utcnow()
    expiry_time = start_time + timedelta(hours=expiry_hours)
    
    user_delegation_key = blob_service_client.get_user_delegation_key(
        key_start_time=start_time,
        key_expiry_time=expiry_time
    )
    
    # Générer SAS Token
    sas_token = generate_container_sas(
        account_name=os.getenv('ADLS_NAME'),
        container_name=os.getenv('CNTNR_NAME'),
        user_delegation_key=user_delegation_key,
        permission="racwd",  # read, add, create, write, delete
        expiry=expiry_time,
        start=start_time
    )
    
    return sas_token

if __name__ == "__main__":
    try:
        # Générer le SAS Token
        sas = generate_sas_token()
        
        # Construire l'URL complète
        container_url = f"https://{os.getenv('ADLS_NAME')}.blob.core.windows.net/{os.getenv('CNTNR_NAME')}?{sas}"
        
        print("\nSAS Token généré avec succès!")
        print("\nURL complète du conteneur avec SAS:")
        print(container_url)
        
    except Exception as e:
        print(f"\nErreur lors de la génération du SAS token: {str(e)}")
