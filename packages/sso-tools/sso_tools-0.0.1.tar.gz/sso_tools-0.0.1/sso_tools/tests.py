from main import OAuth2


client_id = "NpMMpDkj4vLyiirPSauUmWupENl38pjbZeNwUjIq"
client_secret = (
    "h83p6XozvOAbCDWB75ktwHrpfTbTf7jaM41Xmkto4ZpN07NTgovdcilY2XIawtDF2bcsg"
    "6G1qFvCdAZe33WAcPVF5dVRxJLqDyEkUxxJJaWvgIUGogycX6tKCOri0YLv"
)
redirect_uri = "http://localhost:8000/111"
server_host = "http://localhost:8000"
oauth2 = OAuth2(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    server_host=server_host,
)

# 인증 URL
print(oauth2.get_authorization_url())

# 토큰 발급
code = "z0yBA81p6yuBgQuYzXjN3rIZvkdvgp"
state = "QTdNUEc2WDNQTEdYRDFURlJVUldNNFU1MzI2NUo3Q0c1WElRIVA1RElKMFZKWEg3MkZENDhXT1BGRklZMk5HWDY3WEs%3D"
token = oauth2.get_token(code, state)
print("access_token : ", token.access_token)
print("refresh_token : ", token.refresh_token)
print(token.__dict__)
