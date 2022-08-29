from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.integrations.sqla_oauth2 import (
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.oauth2.rfc6749 import grants

from app import db
from app.core.user import User
from .model import OauthApplication, OauthToken, OauthAuthorizationCode


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        client = request.client
        auth_code = OauthAuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_uuid=request.user.uuid,
        )
        db.session.add(auth_code)
        db.session.commit()
        return auth_code

    def query_authorization_code(self, code, client):
        item = OauthAuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return User.get_from_uuid(authorization_code.user_uuid)


def query_client(client_id):
    return OauthApplication.query.filter_by(client_id=client_id).first()


def save_token(token_data, request):
    token = OauthToken(
        client_id=request.client.client_id,
        user_uuid=request.user.uuid,
        **token_data
    )
    db.session.add(token)
    db.session.commit()


authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)
require_oauth = ResourceProtector()


def config_oauth(app):
    authorization.init_app(app)

    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.RefreshTokenGrant)
    authorization.register_grant(AuthorizationCodeGrant)

    revocation_cls = create_revocation_endpoint(db.session, OauthToken)
    authorization.register_endpoint(revocation_cls)

    bearer_cls = create_bearer_token_validator(db.session, OauthToken)
    require_oauth.register_token_validator(bearer_cls())
