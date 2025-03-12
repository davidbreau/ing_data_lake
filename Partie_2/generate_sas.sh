#!/bin/bash

source ../variables.sh
source ../.env

# Obtenir la date de début (maintenant)
start_date=$(date -u +"%Y-%m-%dT%H:%MZ")
# Obtenir la date d'expiration (dans 1 jour)
expiry_date=$(date -u -d "+1 day" +"%Y-%m-%dT%H:%MZ")

# Se connecter avec le SP secondaire pour accéder au Key Vault
az login --service-principal \
    --username $SP2_ID \
    --password $(az keyvault secret show --vault-name $KV_NAME --name $KV_SECRET_NAME --query "value" -o tsv) \
    --tenant $TENANT_ID \
    --output none

# Se connecter avec le SP principal pour le Data Lake
az login --service-principal \
    --username $SP1_ID \
    --password $(az keyvault secret show --vault-name $KV_NAME --name $KV_SECRET_NAME --query "value" -o tsv) \
    --tenant $TENANT_ID \
    --output none

# Générer une User Delegation Key
delegation_key=$(az storage blob user-delegation-key create \
    --account-name $ADLS_NAME \
    --auth-mode login \
    --start-time $start_date \
    --expiry-time $expiry_date \
    -o json)

# Générer le SAS token avec la User Delegation Key
sas_token=$(az storage container generate-sas \
    --account-name $ADLS_NAME \
    --name $CNTNR_NAME \
    --delegation-key "$delegation_key" \
    --permissions racwd \
    --start $start_date \
    --expiry $expiry_date \
    --auth-mode login \
    -o tsv)

echo "SAS Token généré avec succès :"
echo $sas_token

# Exemple d'URL complète pour accéder au conteneur avec le SAS
container_url="https://$ADLS_NAME.blob.core.windows.net/$CNTNR_NAME?$sas_token"
echo -e "\nURL complète du conteneur avec SAS :"
echo $container_url
