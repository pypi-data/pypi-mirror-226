import logging
import sys
import requests

from rc.utils import RC_BASE_URL

logger = logging.getLogger(__name__)

class RctlValidRequestError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def valid_response(response):
    if not isinstance(response, dict):
        raise RctlValidRequestError("HTTP response is not a dict type.")

    if 'success' not in response.keys():
        raise RctlValidRequestError("HTTP response `success` keyword not found.")

    if response['success']:
        if 'data' not in response.keys():
            raise RctlValidRequestError("HTTP response `data` keyword not found.")
        return response
    
    else:
        if 'message' not in response.keys():
            raise RctlValidRequestError("HTTP response `message` keyword not found.")
        raise RctlValidRequestError("HTTP response {0}".format(response["message"]))


def make_request(url, method, data = None, auth_token=None):
    headers = {'Content-Type': 'application/json'}
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    logger.debug("URL: {}".format(url))
    logger.debug("PAYLOAD: {}".format(data))
    try:
        response = requests.request(method, url, headers=headers, data=data)
        logger.debug("RESPONSE: {}".format(response.json()))
        response.raise_for_status()
        if response.content:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        logger.error('Error occurred during HTTP request: {}'.format(e))
        raise RctlValidRequestError('Error occurred during HTTP request: {}'.format(e))
    except ValueError as e:
        logger.error('Error occurred while parsing response JSON: {}'.format(e))
        raise RctlValidRequestError('Error occurred while parsing response JSON: {}'.format(e))

def get_config_value_by_key(key):

    # Validate key parameter
    if not key:
        raise ValueError("Key parameter must be provided.")
    
    url = f"{RC_BASE_URL}/configs?key={key}"

    try:
        response = valid_response(make_request(url, "GET"))
        key_value = response['data']['conf_value']
        logger.debug("KEY VALUE FROM URL: {0} --- VALUE : {1}".format(url, key_value))
        return key_value
    except (KeyError, TypeError) as e:
        logger.error("Error retrieving configuration value for key '{0}': {1}".format(key, e))
        sys.exit(1)
    except Exception as e:
        logger.error("An error occurred while retrieving configuration value: {0}".format(e))
        sys.exit(1)

def get_all_config():
    url = f"{RC_BASE_URL}/configs"
    response = valid_response(make_request(url, "GET"))
    key_value = response['data']
    return key_value


def create_repository(obj):
    url = f"{RC_BASE_URL}/repos"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def create_repo_lock(obj):
    url = f"{RC_BASE_URL}/repolock"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def is_repo_lock(repo):
    url = f"{RC_BASE_URL}/repolock?key={repo}"
    response = valid_response(make_request(url, "GET"))
    value = response['data']['locked']
    logger.debug("REPO LOCK VALUE : {0}".format( value))
    if value:
        msg = "Someone is uploading. Please try after some time."
        raise RctlValidRequestError(msg)
    return value


def update_repo_lock(repo, lock):
    url = f"{RC_BASE_URL}/repolock/{repo}"
    response = valid_response(make_request(url, "PUT", lock))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def update_repo_commit_id(data):
    url = f"{RC_BASE_URL}/repocommit/update/commitid"
    response = valid_response(make_request(url, "POST", data))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def insert_repo_commit(obj):
    url = f"{RC_BASE_URL}/repocommit"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data

def get_repo_commit_id(obj):
    url = f"{RC_BASE_URL}/repocommit/data"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data

def get_repo_commit(repo):
    url = f"{RC_BASE_URL}/repocommit/repo/{repo}"
    response = valid_response(make_request(url, "GET"))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data

def get_repo_version(repo):
    url = f"{RC_BASE_URL}/repocommit/repo/{repo}"
    response = make_request(url, "GET")
    if not isinstance(response, dict):
        raise RctlValidRequestError("HTTP response is not a dict type.")

    if 'success' not in response.keys():
        raise RctlValidRequestError("HTTP response `success` keyword not found.")

    if response['success']:
        if 'data' not in response.keys():
            raise RctlValidRequestError("HTTP response `data` keyword not found.")
    if not response['data']:
        return False
    else:
        logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, response['data']))
        return response['data']["version"]       
        
def get_commit_version(commit_id):
    url = f"{RC_BASE_URL}/repocommit/commitId/{commit_id}"
    response = make_request(url, "GET")
    if not isinstance(response, dict):
        raise RctlValidRequestError("HTTP response is not a dict type.")

    if 'success' not in response.keys():
        raise RctlValidRequestError("HTTP response `success` keyword not found.")

    if response['success']:
        if 'data' not in response.keys():
            raise RctlValidRequestError("HTTP response `data` keyword not found.")
    if not response['data']:
        return False
    else:
        logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, response['data']))
        return response['data']["version"] 

def get_repository(obj):
    url = f"{RC_BASE_URL}/repos-name?repoName={obj}"
    response = valid_response(make_request(url, "GET"))
    data = response['data']
    if not data:
        return False, False
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data['repo_name'], data['tag']

def get_version(obj):
    url = f"{RC_BASE_URL}/version-list/{obj}"
    response = valid_response(make_request(url, "GET"))
    data = response["data"]
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data

def get_commit_repo(id):
    url = f"{RC_BASE_URL}/repocommit?key={id}"
    response = valid_response(make_request(url, "GET"))
    data = response["data"]
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data



    