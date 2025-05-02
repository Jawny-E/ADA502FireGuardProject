FROM quay.io/keycloak/keycloak:26.1.4

# Optional: if you want to keep using the version from your existing config, set ARG
ARG KC_VERSION=26.1.4

COPY docker/auth/fireguardRealm.json /opt/keycloak/data/import/realm.json

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev", "--import-realm"]
