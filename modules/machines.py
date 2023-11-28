import XenAPI

    session = XenAPI.xapi_local()
    try:
        session.xenapi.login_with_password("root", "", "2.3", "My Widget v0.1")