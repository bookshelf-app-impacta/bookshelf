def user_to_json(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "displayName": user.display_name,
        "avatarUrl": user.avatar_url,
        "role": user.role,
        "isActive": user.is_active,
    }
