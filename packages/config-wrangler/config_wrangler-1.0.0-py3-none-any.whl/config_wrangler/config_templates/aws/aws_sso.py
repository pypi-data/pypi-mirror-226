def main():
    from time import time, sleep
    import webbrowser
    from boto3.session import Session

    ################
    # Config items
    # 1) SSO general
    sso_client_name = 'myssoapp'
    sso_client_type = 'public'
    start_url = 'https://d-1234567890.awsapps.com/start'
    # 2) Assume role details
    region = 'us-east-1'
    account_id = '1234567890'
    role_name = 'my_role'

    sso_session = Session()
    sso_oidc = sso_session.client('sso-oidc')
    client_creds = sso_oidc.register_client(
        clientName=sso_client_name,
        clientType=sso_client_type,
    )
    device_authorization = sso_oidc.start_device_authorization(
        clientId=client_creds['clientId'],
        clientSecret=client_creds['clientSecret'],
        startUrl=start_url,
    )
    url = device_authorization['verificationUriComplete']
    device_code = device_authorization['deviceCode']
    expires_in = device_authorization['expiresIn']
    interval = device_authorization['interval']
    webbrowser.open(url, autoraise=True)
    token = None

    # Try getting a token until complete or expired
    for n in range(1, expires_in // interval + 1):
        try:
            token = sso_oidc.create_token(
                grantType='urn:ietf:params:oauth:grant-type:device_code',
                deviceCode=device_code,
                clientId=client_creds['clientId'],
                clientSecret=client_creds['clientSecret'],
            )
            # Success, break from the loop
            break
        except sso_oidc.exceptions.AuthorizationPendingException:
            pass
        sleep(interval)

    if token is None:
        raise RuntimeError("Unable to complete authentication in time")

    access_token = token['accessToken']
    sso = sso_session.client('sso')
    account_roles = sso.list_account_roles(
        accessToken=access_token,
        accountId=account_id,
    )
    # {
    #     'nextToken': 'string',
    #     'roleList': [
    #         {
    #             'roleName': 'string',
    #             'accountId': 'string'
    #         },
    #     ]
    # }
    roles = account_roles['roleList']

    # TODO: Find the correct role by name / id
    # simplifying here for illustrative purposes
    role = roles[0]
    role_creds = sso.get_role_credentials(
        roleName=role['roleName'],
        accountId=account_id,
        accessToken=access_token,
    )
    session = Session(
        region_name=region,
        aws_access_key_id=role_creds['accessKeyId'],
        aws_secret_access_key=role_creds['secretAccessKey'],
        aws_session_token=role_creds['sessionToken'],
    )


if __name__ == '__main__':
    main()
