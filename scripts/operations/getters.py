"""
Contains functions used to retrieve information from the current Azure state.
"""
from azure.mgmt.managementgroups import ManagementGroupsAPI
from azure.mgmt.resource import SubscriptionClient

def get_subcriptions(credentials, filter: str=None) -> list:
    """
    Retrieves all subscriptions under the current tenant and returns them as a `list` of `dict`.
    
    The `filter` parameter can be used to retrieve subscriptions that start with a particular prefix.
    The subscription_prefix from the config can be used here to retrieve all learner subscriptions, for example.
    """
    subscription_client = SubscriptionClient(credentials)
    subscriptions = []
    for subscription in subscription_client.subscriptions.list():
        subscription = subscription.as_dict()
        if filter != None:
            if subscription["display_name"].startswith(filter):
                subscriptions.append(subscription)
        else:
            subscriptions.append(subscription)
    return subscriptions

def get_management_groups(credentials) -> list:
    """
    Retrieves all management groups under the current tenant and returns them as a `list` of `dict`s.
    """
    management_client = ManagementGroupsAPI(credentials)
    management_groups = []
    for group in management_client.management_groups.list():
        management_groups.append(group.as_dict())
    return management_groups

def get_management_group(credentials, display_name: str) -> dict:
    """
    Retrieves a single management group based on the group's display name and returns it as a `dict`.
    
    Parameter `display_name` is required and its value should be derived from a given cohort's name in the `config.yaml`.
    """
    management_client = ManagementGroupsAPI(credentials)
    for group in management_client.management_groups.list():
        if group.display_name == display_name:
            return group.as_dict()
    else:
        return None

def get_management_group_subscriptions(credentials, management_group: dict) -> list:
    """
    Retrieves all subscriptions assigned to a management group and returns their details as a `list` of `dict`s.

    `management_group` expects a `dict` containing the details for a management group retrieved from the client.
    """
    mgmt_client = ManagementGroupsAPI(credentials)
    subscriptions = []
    for subscription in mgmt_client.management_group_subscriptions.get_subscriptions_under_management_group(group_id=management_group["name"]):
        subscriptions.append(
            {
                "display_name": subscription.display_name,
                "id": subscription.id,
                "name": subscription.name
            }
        )
    return subscriptions

def get_subscription_pool(credentials) -> dict:
    """
    Retrieves the details for the subscription pool and returns them as a `dict`.
    """
    management_groups = get_management_groups(credentials)
    for group in management_groups:
        if group["display_name"] == "Subscription Pool":
            subscription_pool = group
    return subscription_pool
