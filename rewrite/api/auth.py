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


def parse_permissions(permissions: list) -> dict:
    """
    Parse a list of permissions into a nested dictionary/tree structure.
    Matches the legacy parsePermissions function.
    
    Example: ['admin.user', 'community.test.leader'] becomes:
    {
        'admin': {'user': {}},
        'community': {'test': {'leader': {}}}
    }
    """
    parsed = {}
    for perm in permissions:
        parts = perm.lower().split('.')
        current = parsed
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
    return parsed


def find_permission(permission_tree: dict, target_permission: str or list) -> bool:
    """
    Recursively check for permission in permission tree.
    Matches the legacy findPermission function with wildcard support.
    
    Args:
        permission_tree: Parsed permission tree
        target_permission: Permission to check for (string or list of parts)
    
    Returns:
        bool: Whether the permission was found
    """
    if not permission_tree or not isinstance(permission_tree, dict) or len(permission_tree) == 0:
        return False
    
    # Convert string to list of parts
    if isinstance(target_permission, str):
        target_permission = target_permission.lower().split('.')
    
    # If we've consumed all parts, permission is found
    if len(target_permission) == 0:
        return True
    
    # Get the next part to check
    perm_part = target_permission[0]
    remaining_parts = target_permission[1:]
    
    # Check each key in the current tree level
    for current_key, next_tree in permission_tree.items():
        # Wildcard matches everything
        if current_key == '*':
            return True
        
        # Exact match or continue down the tree
        if current_key == perm_part:
            if len(remaining_parts) == 0:
                return True
            return find_permission(next_tree, remaining_parts)
    
    return False


def has_permission(permissions: list, target_permissions: str or list) -> bool:
    """
    Check if a permission list contains the required permission(s).
    Matches the legacy hasPermission function with full wildcard and admin.superadmin support.
    
    Args:
        permissions: List of permission strings the user has
        target_permissions: Permission(s) to check for (string or list of strings)
    
    Returns:
        bool: Whether the user has at least one of the target permissions
    """
    if not permissions:
        return False
    
    # Parse permissions into tree structure
    parsed_permissions = parse_permissions(permissions)
    
    # Check for global admin permissions
    if '*' in parsed_permissions or find_permission(parsed_permissions, 'admin.superadmin'):
        return True
    
    # Check target permissions
    if isinstance(target_permissions, list):
        # Check if user has ANY of the target permissions
        return any(find_permission(parsed_permissions, target_perm) for target_perm in target_permissions)
    else:
        # Check single permission
        return find_permission(parsed_permissions, target_permissions)
