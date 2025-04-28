FROM quay.io/keycloak/keycloak:24.0.4

# Optional: if you want to keep using the version from your existing config, set ARG
ARG KC_VERSION=24.0.4

COPY docker/auth/base_realm.json /opt/keycloak/data/import/realm.json

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev", "--import-realm"]
