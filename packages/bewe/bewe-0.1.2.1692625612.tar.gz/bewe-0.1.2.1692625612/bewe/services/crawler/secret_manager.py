from google.cloud import secretmanager
from typing import Optional
import google_crc32c


def get_secret_token(name) -> Optional[str]:
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={'name': name})
    key = response.payload.data.decode('utf-8')

    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        raise ValueError('Data validation failed.')
    return key
