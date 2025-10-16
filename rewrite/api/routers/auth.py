from ninja import Router
from django.shortcuts import get_object_or_404
from api.models import User
from api.schemas import AuthResponseSchema, UserSchema
from api.auth import generate_jwt

router = Router()


@router.get('/steam/return', response=AuthResponseSchema)
def steam_auth_return(request, openid_identity: str):
    """
    Handle Steam OpenID authentication return
    This is a simplified version - production would need full OpenID validation
    """
    # Extract Steam ID from openid.identity
    steam_id = openid_identity.split('/')[-1]
    
    # Get or create user
    try:
        user = User.objects.get(steam_id=steam_id)
    except User.DoesNotExist:
        # Fetch user info from Steam API
        # This is a placeholder - real implementation needs Steam API call
        user = User.objects.create(
            steam_id=steam_id,
            nickname=f"User{steam_id[-6:]}",
            active=True
        )
    
    # Generate JWT
    token = generate_jwt(user)
    
    return {
        'token': token,
        'user': {
            'uid': user.uid,
            'nickname': user.nickname,
            'steam_id': user.steam_id,
            'community': None,
            'active': user.active
        }
    }


@router.post('/refresh', response=AuthResponseSchema)
def refresh_token(request):
    """Refresh JWT token"""
    user_data = request.auth.get('user')
    if not user_data:
        return 401, {'detail': 'Invalid token'}
    
    user = get_object_or_404(User, uid=user_data['uid'])
    token = generate_jwt(user)
    
    return {
        'token': token,
        'user': {
            'uid': user.uid,
            'nickname': user.nickname,
            'steam_id': user.steam_id,
            'community': None,
            'active': user.active
        }
    }
