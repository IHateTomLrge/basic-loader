from client import create_clients, get_cookies


def bot(url):
    client, user_agent = create_clients()

    # Without cookies
    productPage = client.get(url)
    print("Without cookies, status code: ", end="")
    print(productPage.status_code)
    # 503, Service Unavailable


    # Call cookies generator
    cookies = get_cookies(url, user_agent, max_retry=10) # product url you wanna acces, user_agent generated calling the client generator, max_retry in seconds
    if not cookies:
        return
    
    # For each cookie in all loaded cookies -> set the cookie into the client
    for cookie in cookies:
        client.cookies.set(name=cookie.get('name'), value=cookie.get('value'), expires=cookie.get('expires'), domain=cookie.get('domain'))

    # Retry getting product page using cookies we passed in the client
    productPage = client.get(url)
    print("With generated cookies, status code: ", end="")
    print(productPage.status_code)
    # 200, OK

bot("https://www.titoloshop.com/eu_en/air-jordan-13-retro-red-flint-dj5982-600.html")
