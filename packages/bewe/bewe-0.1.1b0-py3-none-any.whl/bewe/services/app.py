from bewe.services.crawler import secret_manager

print('Hello World!')
print('Exit')
name = 'projects/1066434757302/secrets/finmind_api/versions/1'
print('Token: ', secret_manager.get_secret_token(name))
