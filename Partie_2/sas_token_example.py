import os
from dotenv import load_dotenv
from utils.sas_generator import SASGenerator

# Charger les variables d'environnement
load_dotenv()

# Configuration
tenant_id = os.getenv('TENANT_ID')
sp_secondary_id = os.getenv('SP2_ID')  # ID du SP Keyvault
sp_secondary_secret = os.getenv('SP_PASSWORD')  # Secret du SP Keyvault
keyvault_url = f"https://{os.getenv('KV_NAME')}.vault.azure.net/"
secret_name = os.getenv('KV_SECRET_NAME')
storage_account_name = os.getenv('ADLS_NAME')
container_name = os.getenv('CNTNR_NAME')
sp_principal_id = os.getenv('SP1_ID')  # ID du SP Data Lake

def main():
    # Créer une instance du générateur de SAS
    sas_gen = SASGenerator(
        tenant_id=tenant_id,
        sp_secondary_id=sp_secondary_id,
        sp_secondary_secret=sp_secondary_secret,
        keyvault_url=keyvault_url,
        secret_name=secret_name
    )
    
    try:
        # Générer le SAS token
        sas_token = sas_gen.generate_sas_token(
            storage_account_name=storage_account_name,
            container_name=container_name,
            sp_principal_id=sp_principal_id,
            permissions="racwd",  # read, add, create, write, delete
            expiry_days=1
        )
        
        # Construire l'URL complète
        container_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}?{sas_token}"
        
        print("SAS Token généré avec succès!")
        print("\nURL complète du conteneur avec SAS:")
        print(container_url)
        
    except Exception as e:
        print(f"Erreur lors de la génération du SAS token: {str(e)}")

if __name__ == "__main__":
    main()
