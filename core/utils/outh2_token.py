import requests


def get_access_token():
    url = 'https://test.salesforce.com/services/oauth2/token'

    # Definir los parámetros de la solicitud
    params = {
        'grant_type': 'password',
        'client_id': '3MVG9Oe7T3Ol0ea5PBiRyQ1rXlHK1OlMsdtlPESeFhgaOQOWyN2JFgxXnHzNpAvv_NNv3IGuveoDv1sn5.geW',
        'client_secret': '51E210B3DA47C7178709C639128C7E3C46CBE80581C912356AE3F7CDB5E0C4F8',
        'username': 'integrationuser@nagarro.com.qa',
        'password': 'crowley@123'
    }

    # Realizar la solicitud POST
    response = requests.post(url, params=params, verify=True)

    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener el token de la respuesta JSON
        token = response.json().get('access_token')
        return token
    else:
        print(f"Error al obtener el token: {response.status_code} - {response.text}")
        return None


# Ejemplo de uso
if __name__ == "__main__":
    token = get_access_token()
    if token:
        print(f"Bearer Token: {token}")
