DJOSER = {
    # "LOGIN_FIELD": 'email',
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    'TOKEN_MODEL': None,       # To Delete User Must Set it to None
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    # 'ACTIVATION_URL':'auth/users/activation/{uid}/{token}',
    'ACTIVATION_URL': 'auth/activate/?uid={uid}&token={token}',

    'SERIALIZERS':{
        'user_create_password_retype': 'core.api.serializers.Djoser.UserCreateSerializer',
        # Note this api will apply to all patch's like put delete get ... when ever you define fields it will apply on all endpoints
        'user': 'core.api.serializers.Djoser.UserSerializer',
        #! Can change later
        'current_user': 'core.api.serializers.Djoser.UserSerializer',

        "activation": "core.api.serializers.Djoser.ActivationSerializer",

        "password_reset_confirm": "core.api.serializers.Djoser.PasswordResetConfirmSerializer",

        "password_reset_confirm_retype": "core.api.serializers.Djoser.PasswordResetConfirmRetypeSerializer",

        # Some things wrong with this checked everything
        "username_reset_confirm": "core.api.serializers.Djoser.UsernameResetConfirmSerializer",

        "username_reset_confirm_retype": "core.api.serializers.Djoser.UsernameResetConfirmRetypeSerializer",

        # 'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },

    'EMAIL': {
        'activation': 'core.api.serializers.Djoser.ActivationEmail' ,
        'password_reset': 'core.api.serializers.Djoser.PasswordResetEmail' ,
        'username_reset': 'core.api.serializers.Djoser.UsernameResetEmail'
    } ,

}