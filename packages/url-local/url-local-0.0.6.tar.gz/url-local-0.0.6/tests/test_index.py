import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import pytest
from src.index import *
# from src.index import UrlCirclez
# from src.action_name_enum import ActionName
# from src.brand_name_enum import BrandName
# from src.component_name_enum import ComponentName
# from src.entity_name_enum import EntityName
# from src.environment_name_enum import EnvironmentName



@pytest.mark.test
def test_user_registration_endpointUrl_without_parameter():
    url = UrlCirclez.endpoint_url(BrandName.CIRCLEZ.value, EnvironmentName.DVLP1.value, ComponentName.USER_REGISTRATION.value, EntityName.USER_REGISTRATION.value, 1, ActionName.CREATE_USER.value)

    assert url == 'https://lczo7l194b.execute-api.us-east-1.amazonaws.com/dvlp1/api/v1/user-registration/createUser'


@pytest.mark.test
def test_endpointUrl_without_parameters():
    url = UrlCirclez.endpoint_url(BrandName.CIRCLEZ.value, EnvironmentName.DVLP1.value, ComponentName.GROUP.value, EntityName.GROUP.value, 1, ActionName.GET_ALL_GROUPS.value)

    assert url == 'https://t91y4nxsye.execute-api.us-east-1.amazonaws.com/dvlp1/api/v1/group/getAllGroups'


@pytest.mark.test
def test_group_ndpointUrl_with_many_parameter():
    url = UrlCirclez.endpoint_url(BrandName.CIRCLEZ.value, EnvironmentName.DVLP1.value, ComponentName.GROUP.value, EntityName.GROUP.value, 1, ActionName.GET_ALL_GROUPS.value, path_parameters={'id': 1, 'lang_code': 'en'})

    assert url == 'https://t91y4nxsye.execute-api.us-east-1.amazonaws.com/dvlp1/api/v1/group/getAllGroups/1/en'


@pytest.mark.test
def test_group_endpointUrl_with_query_path_parameter_and_query_parameter():
    url = UrlCirclez.endpoint_url(BrandName.CIRCLEZ.value, EnvironmentName.DVLP1.value, ComponentName.GROUP.value, EntityName.GROUP.value, 1, ActionName.GET_ALL_GROUPS.value, path_parameters={"lang_code": 'en' }, query_parameters={ "name": 'spo', 'other': 'other' })

    assert url == "https://t91y4nxsye.execute-api.us-east-1.amazonaws.com/dvlp1/api/v1/group/getAllGroups/en?name=spo&other=other"


@pytest.mark.test
def test_auth_endpointUrl_without_parameters():
    url = UrlCirclez.endpoint_url(BrandName.CIRCLEZ.value, EnvironmentName.DVLP1.value, ComponentName.AUTH_LOGIN.value, EntityName.AUTH_LOGIN.value, 1, ActionName.LOGIN.value)

    assert url == "https://i4wp5o2381.execute-api.us-east-1.amazonaws.com/dvlp1/api/v1/auth/login"