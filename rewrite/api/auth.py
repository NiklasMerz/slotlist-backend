import jwt
from datetime import datetime, timedelta
from django.conf import settings
from typing import Optional, Dict, Any
from api.models import User, Permission


def generate_jwt(user: User) -> str:
    """Generate a JWT token for a user"""
    permissions = list(Permission.objects.filter(user=user).values_list('permission', flat=True))
    
    payload = {
        'user': {
            'uid': str(user.uid),
            'nickname': user.nickname,
            'steam_id': user.steam_id,
            'community': {
                'uid': str(user.community.uid),
                'name': user.community.name,
                'tag': user.community.tag,
                'slug': user.community.slug
            } if user.community else None,
            'active': user.active
        },
        'permissions': permissions,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRES_IN),
        'iss': settings.JWT_ISSUER,
        'aud': settings.JWT_AUDIENCE,
        'sub': str(user.uid)
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def has_permission(permissions: list, required_permission: str) -> bool:
    """Check if a permission list contains the required permission (supports wildcards)"""
    if '*' in permissions:
        return True
    
    # Check exact match
    if required_permission in permissions:
        return True
    
    # Check wildcard patterns
    parts = required_permission.split('.')
    for perm in permissions:
        if perm.endswith('.*'):
            perm_parts = perm[:-2].split('.')
            if len(perm_parts) <= len(parts):
                if parts[:len(perm_parts)] == perm_parts:
                    return True
    
    return False


def parse_permissions(permissions: list) -> dict:
    """Parse a list of permissions into a nested dictionary"""
    parsed = {}
    for perm in permissions:
        parts = perm.split('.')
        current = parsed
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
    return parsed
