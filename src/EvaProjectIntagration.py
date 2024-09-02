import requests
from typing import List

class EvaProjectIntegration:
    """
    A class to interact with the EvaProject API for task management and user retrieval.

    Attributes:
        url (str): The base URL of the EvaProject API.
        token (str): The Bearer token for authentication.
        headers (dict): The headers to be used in API requests.
    """
    

    def __init__(self) -> None:
        """
        Initializes the EvaProjectIntegration instance with API URL and authentication token.
        """
        self.url = 'https://reu-im-g-v-plehanova.evateam.ru/api/'
        self.token = 'Bearer NnVwvpAZg0j8IiWRYxJD'
        self.headers = {
            'content-type': 'application/json',
            'Authorization': self.token
        }


    def create_task(self, task_name: str = "", list_name: str = 'Спринт 1', task_description: str = "") -> None:
        """
        Creates a new task in the EvaProject system.

        Args:
            task_name (str): The name of the task to be created.
            list_name (str): The name of the list where the task will be added.
            task_description (str): A description of the task.

        Returns:
            None: Prints the status code and task name.
        """
        method = 'POST'
        params = {
            'jsonrpc': '2.2',
            'method': 'CmfTask.create',
            'kwargs': {
                'name': task_name,
                'lists': [list_name],
                'text': f'<p>{task_description}</p>'
            }
        }
        
        result = requests.request(method, self.url, json=params, headers=self.headers)
        print(f"{result.status_code} - CmfTask.create - {task_name}")


    def get_users(self) -> List[str]:
        """
        Retrieves a list of users from the EvaProject system.

        Returns:
            list: A list of usernames (logins) of users who are local and not part of the system.
        """
        users = []
        
        method = 'POST'
        params = {
            'jsonrpc': '2.2',
            'method': 'CmfPerson.list',
            'kwargs': {'filter': [['user_local', '==', True], ['system', '==', False]]}
        }
        
        result = requests.request(method, self.url, json=params, headers=self.headers)
        response = result.json()
        
        for user in response.get('result', []):
            login = user.get('login')
            if login:
                users.append(login)
                
        return users
