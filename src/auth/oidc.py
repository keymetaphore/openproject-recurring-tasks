from authlib.integrations.starlette_client import OAuth
from settings import OIDC_CLIENT_ID, OIDC_CLIENT_SECRET, OIDC_ISSUER_URL

oauth = OAuth()
oauth.register(
    name="oidc",
    client_id=OIDC_CLIENT_ID,
    client_secret=OIDC_CLIENT_SECRET,
    server_metadata_url=f"{OIDC_ISSUER_URL}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)
