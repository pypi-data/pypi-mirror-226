import requests


class Authentication:
    """
    This class handles all the authentication operations.
    """

    def __init__(self, email, password, base_url = "http://localhost:2728/"):
        """
        Initilizes the authentication object.

        Args:
            svid (str): The svid of the user.
            password (str): The password of the user.
        """
        self.email = email
        self.password = password
        self.base_url = base_url
        if not base_url.endswith("/"):
            self.base_url = base_url+"/"


    def signup(self):
        """
        Signs up a new user.

        Returns:
            dict: The response from the API.
        """
        url = self.base_url+"signup"
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = requests.post(url, json=data)
        return response.json()

    def signin(self):
        """
        Signs in a user.

        Returns:
            dict: The response from the API.
        """
        url = self.base_url+"signin"
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = requests.post(url, json=data)
        return response.json()


class Tree:
    """
    This class handles all the tree operations.
    """

    def __init__(self, svid, password, tree_name, tree_password, url="http://localhost:2728/tree"):
        """
        Initilizes the tree object.

        Args:
            svid (str): The svid of the user.
            password (str): The password of the user.
            tree_name (str): The name of the tree.
            tree_password (str): The password of the tree.
        """
        self.svid = svid
        self.password = password
        self.tree_name = tree_name
        self.tree_password = tree_password
        self.url = url

    def plant_tree(self):
        """
        Plants a new tree.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "type": "plant_tree",
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
        }
        response = requests.post(url, json=data)
        return response.json()

    def tree(self, path):
        """
        Gets the tree information at the specified path.

        Args:
            path (str): The path to the tree.

        Returns:
            dict: The response from the API.
        """
        url = "http://localhost:2728/tree"
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "tree",
            "path": path,
        }
        response = requests.post(url, json=data)
        return response.json()

    def add_branch(self, path, branch):
        """
        Adds a new branch to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            branch (str): The name of the branch.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "add_branch",
            "path": path,
            "branch": branch,
        }
        response = requests.post(url, json=data)
        return response.json()

    def remove_branch(self, path, branch):
        """
        Removes a new branch to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            branch (str): The name of the branch.

        Returns:
            dict: The response from the API."""
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "remove_branch",
            "path": path,
            "branch": branch,
        }
        response = requests.post(url, json=data)
        return response.json()

    def add_leaf(self, path, leaf, data):
        """
        Adds a new leaf to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            leaf (str): The name of the leaf.
            data (str): The data to be stored in the leaf.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "add_leaf",
            "path": path,
            "leaf": leaf,
            "data": data,
        }
        response = requests.post(url, json=data)
        return response.json()

    def remove_leaf(self, path, leaf):
        """
        Removes a leaf from the tree at the specified path.

        Args:
            path (str): The path to the tree.
            leaf (str): The name of the leaf.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "remove_leaf",
            "path": path,
            "leaf": leaf,
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_leaf(self, path, leaf):
        """
        Gets the data stored in the leaf at the specified path.

        Args:
            path (str): The path to the tree.
            leaf (str): The name of the leaf.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "get_leaf",
            "path": path,
            "leaf": leaf,
        }
        response = requests.post(url, json=data)
        return response.json()

    def add_fruit(self, path, fruit):
        """
        Adds a new leaf to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            fruit (str): The name of the fruit.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "add_fruit",
            "path": path,
            "fruit": fruit,
        }
        response = requests.post(url, json=data)
        return response.json()

    def execute_query(self, path, fruit, query):
        """
        Adds a new leaf to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            fruit (str): The name of the leaf.
            query (str): Query to be executed.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "execute_query",
            "path": path,
            "fruit": fruit,
            "query": query,
        }
        response = requests.post(url, json=data)
        return response.json()

    def add_flower(self, path, flower, b64):
        """
        Adds a new leaf to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            flower (str): The name of the flower.
            b64 (str): The base64 data to be stored in the flower.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "add_flower",
            "path": path,
            "flower": flower,
            "b64": b64,
        }
        response = requests.post(url, json=data)
        return response.json()

    def remove_flower(self, path, flower):
        """
        Adds a new leaf to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            flower (str): The name of the flower.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "remove_leaf",
            "path": path,
            "flower": flower,
        }
        response = requests.post(url, json=data)
        return response.json()

    def download_flower(self, path, flower):
        """
        Adds a new leaf to the tree at the specified path.

        Args:
            path (str): The path to the tree.
            flower (str): The name of the flower.

        Returns:
            dict: The response from the API.
        """
        url = self.url
        data = {
            "svid": self.svid,
            "password": self.password,
            "tree_name": self.tree_name,
            "tree_password": self.tree_password,
            "type": "download_flower",
            "path": path,
            "flower": flower,
        }
        response = requests.post(url, json=data)
        return response.json()

