from fastapi import APIRouter, Depends, HTTPException, Request, status
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User, OauthAccount
from app.services.auth_service import create_user_tokens
from app.core.config import settings

router = APIRouter()
oauth = OAuth()

if settings.GOOGLE_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
    oauth.register(
        name='google',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        client_kwargs={'scope': 'openid email profile'}
    )


if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='github',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )


@router.get("/{provider}/login")
async def oauth_login(provider: str, request: Request):
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider {provider} not found"
        )
    redirect_url = request.url_for('oauth_callback', provider=provider)
    return await client.authorize_redirect(request, redirect_url)


@router.egt("/{provider}/callback/")
async def oauth_callback(provider: str, request: Request, db: AsyncSession = Depends(get_db)):
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider {provider} not found"
        )
    try:
        token = await client.authorize_access_token(request)
    except OAuthError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

    if provider == 'google':
        user_info = await client.parse_id_token(request, token)
        email = user_info.get('email')
        name = user_info.get('name')
        provider_user_id = user_info.get('sub')
    elif provider == 'github':
        res = await client.get('user', token=token)
        user_info = res.json()
        email_res = await client.get('user/emails', token=token)
        email = email_res.json()
        primary_email = next((e['email'] for e in email if e['primary']), None)
        email = primary_email
        name = user_info.get('name') or user_info.get('login')
        provider_user_id = str(user_info.get('id'))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported provider"
        )

    # Check if the OAuth account already exists
    result = await db.execute(select(OauthAccount).where(
        OauthAccount.provider == provider,
        OauthAccount.provider_user_id == provider_user_id
    ))
    oauth_account = result.scalars().first()