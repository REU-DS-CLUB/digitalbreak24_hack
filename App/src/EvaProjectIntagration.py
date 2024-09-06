import requests
import Levenshtein
import logging
from typing import List, Dict, Union


class EvaProjectIntegration:
    """
    A class to interact with the EvaProject API for task management and user retrieval.

    Attributes:
        url (str): The base URL of the EvaProject API.
        token (str): The Bearer token for authentication.
        headers (dict): The headers to be used in API requests.
    """

    def __init__(self, logging_flag: int = 0) -> None:
        """
        Initializes the EvaProjectIntegration instance with API URL and authentication token.
        """
        self.url = 'https://reu-im-g-v-plehanova.evateam.ru/api/'
        self.token = 'Bearer NnVwvpAZg0j8IiWRYxJD'
        self.headers = {
            'content-type': 'application/json',
            'Authorization': self.token
        }
        
        # Настройка конфигурации для логирования
        if logging_flag: 
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', force=True)

    def create_task(self, task_name: str = "", list_name: str = 'Спринт 1', 
                    task_description: str = "", responsible_name: str = "") -> None:
        """
        Creates a new task in the EvaProject system.

        Args:
            task_name (str): The name of the task to be created.
            list_name (str): The name of the list where the task will be added.
            task_description (str): A description of the task.
            responsible_name (str): The name of the responsible person for the task.

        Returns:
            None: Prints the status code, task name, and response from the API.
        """
        responsible_flag = 1 if len(responsible_name) > 0 else 0
        
        if responsible_flag:
            responsible_id = self.get_user_id_by_name(responsible_name)  # Find nearest user by Levenshtein distance between names
            
            if len(responsible_id) < 1:  # Case when user list is empty; get_user_id_by_name() will return ""
                responsible_flag = 0
        
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
        
        if responsible_flag:
            params["kwargs"].update({'responsible': {'id': responsible_id}})
        
        result = requests.request(method, self.url, json=params, headers=self.headers)
        
        logging.debug(f"Статус по CmfTask.create {task_name}: {result.status_code}")
        logging.debug(f"Ответ от API: {result.json()}")

    def get_user_id_by_name(self, name: str) -> str:
        """
        Finds the user ID based on the closest match to the given name using Levenshtein distance.

        Args:
            name (str): The name of the user to search for.

        Returns:
            str: The ID of the closest matching user. Returns an empty string if no match is found.
        """
        users = self.get_users()
        best_user_id = ""
        best_user_name = ""
        min_sim_measure = float("inf")
        
        for user in users:
            sim_measure = Levenshtein.distance(name, user["name"])

            if sim_measure < min_sim_measure:
                min_sim_measure = sim_measure
                best_user_id = user["id"]
                best_user_name = user["name"]
                
        logging.debug(f"Ближайший найденный пользователь по {name}: {best_user_name}")
                
        return best_user_id

    def get_users(self) -> List[Dict[str, Union[str, int]]]:
        """
        Retrieves a list of users from the EvaProject system.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of dictionaries containing user details 
            including login, name, and ID.
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
        
        for user in response['result']:
            login = user['login']
            if login:
                users.append({"login": user["login"], "name": user["name"], "id": user["id"]})
                
        return users
