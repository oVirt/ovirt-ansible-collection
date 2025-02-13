#!/bin/bash

# This file is a part of the hosted-engine deployment process
# The goal is to add a temporary URI to the ovirt-engine-internal client, and return the original value on the second pass.

# KEYCLOAK_URL get from ENV: "https://{{ he_fqdn }}/ovirt-engine-auth"
# HOST_FQDN get from ENV: "{{ he_host_name }}"
# PASSWORD get from ENV: "{{ he_admin_password }}"

KEYCLOAK_REALM=ovirt-internal
KEYCLOAK_CLIENT_ID=ovirt-engine-internal
USERNAME="admin"
REDIRECT_URIS_TMPFILE=/tmp/keycloak_redirect_uris.tmp

TKN=$(curl --insecure --silent -X POST "${KEYCLOAK_URL}/realms/master/protocol/openid-connect/token" \
	--header "content-type: application/x-www-form-urlencoded" \
	--data-urlencode "client_id=admin-cli" \
	--data-urlencode "username=${USERNAME}" \
	--data-urlencode "password=${PASSWORD}" \
	--data-urlencode "grant_type=password" | jq --raw-output '.access_token' )

CLIENT_DATA=$(curl --insecure --silent -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients?clientId=${KEYCLOAK_CLIENT_ID}" \
	--header "Accept: application/json" \
	--header "Authorization: Bearer $TKN")

CLIENT_ID=$(echo $CLIENT_DATA | jq -r '.[0].id')

if [ -f "$REDIRECT_URIS_TMPFILE" ]; then
	# Second pass
	# Restore original redirectUris parameters
	NEW_URI=$(<$REDIRECT_URIS_TMPFILE)
	UPDATED_CLIENT_DATA=$(echo $CLIENT_DATA | jq --argjson new_uri "$NEW_URI" '.[0] | .redirectUris = $new_uri')
	rm -rf $REDIRECT_URIS_TMPFILE
else
	# First pass
	# Save original redirectUris parameters
	REDIRECT_URIS=$(echo $CLIENT_DATA | jq -r '.[0].redirectUris')
	echo "$REDIRECT_URIS" > $REDIRECT_URIS_TMPFILE

	# Add a temporary URI to redirectUris
	NEW_URI="https://${HOST_FQDN}:6900*"
	UPDATED_CLIENT_DATA=$(echo $CLIENT_DATA | jq --arg new_uri "$NEW_URI" '.[0] | .redirectUris += [$new_uri]')
fi

# Update client data
curl --insecure --silent --http1.0 -X PUT "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients/${CLIENT_ID}" \
  --header "Authorization: Bearer $TKN" \
  --header "Content-Type: application/json" \
  --data-raw "$UPDATED_CLIENT_DATA"
