"""
Contains functions and procedures that make changes to the Azure state.
"""
from azure.mgmt.managementgroups import ManagementGroupsAPI
from azure.core.exceptions import HttpResponseError
from operator import itemgetter
from operations.getters import get_subcriptions, get_subscription_pool, get_management_group, get_management_group_subscriptions
from time import sleep
import json

def reset_subscriptions(credentials, filter):
    """
    This procedure will assign all subscriptions to the subscription pool, effectively resetting all subscriptions.
    """
    mgmt_client = ManagementGroupsAPI(credentials)
    all_subscriptions = get_subcriptions(credentials, filter=filter)
    subscription_pool = get_subscription_pool(credentials)
    for subscription in all_subscriptions:
        mgmt_client.management_group_subscriptions.create(group_id=subscription_pool["name"], subscription_id=subscription["subscription_id"])

def assign_subscriptions(credentials, cohorts):
    """
    Assigns subscriptions to management groups based on the cohort configuration. Parameter cohorts expects a list of
    dicts containing cohort details, retrieved from the config.yaml.
    
    Cohorts are sorted by learners in ascending order. This allows subs from groups that are shrinking to be made 
    available for groups that are growing.
    
    This solution is incomplete. If group1 has 10 subscriptions and group 2 has 5, and group1 shrinks from 10 -> 9
    and group2 grows from 5 -> 6, group 2 will still be processed first. If there are no spare subscriptions in the
    pool, the script will break.
    
    A better solution would be to find the difference between the config and the current state to determine which
    groups are shrinking vs which are growing, and then process the shrinking groups first (ordered by desired count  
    in ascending order) followed by growing cohorts.

    Attempts to assign subscriptions to groups are retried after waiting 60 seconds if unsuccessful. This appears to be
    because Azure doesn't instantly update inherited permissions for management groups and/or subscriptions after a 
    reassignment takes place. 60 seconds appears to be plenty time to wait for a reattempt to be successful. Number
    of retries is currently set to 10 - this might be more than necessary.
    """
    cohorts = sorted(cohorts, key=itemgetter('learners'))
    retry_attempts = 10
    seconds_before_retry = 60

    mgmt_client = ManagementGroupsAPI(credentials)
    for cohort in cohorts:
        print(f"Checking subscriptions for cohort {cohort['name']}.")
        subscription_pool = get_subscription_pool(credentials)
        available_subscriptions = get_management_group_subscriptions(credentials, subscription_pool)
        cohort_management_group = get_management_group(credentials, cohort["name"])
        cohort_subscriptions = get_management_group_subscriptions(credentials, cohort_management_group)
        
        # This section needs refactoring
        if len(cohort_subscriptions) < cohort["learners"]:
            print(f"Number of subscriptions in cohort is less than desired.")
            for subscription in available_subscriptions[:cohort["learners"]]:
                print(f"Assigning {subscription['display_name']} to {cohort['name']}.")
                for attempt in range(retry_attempts):
                    try:
                        mgmt_client.management_group_subscriptions.create(group_id=cohort_management_group["name"], subscription_id=subscription["name"])
                    except HttpResponseError as error:
                        print(f"Attempt {attempt}/{retry_attempts} failed with the following message: '{error.message}'")
                        print("Waiting 60 seconds before retrying...")
                        sleep(seconds_before_retry)
                        continue
                    else:
                        break
                else:
                    raise Exception(f"Failed to assign desired number of subscriptions to {cohort['name']}.")
        
        elif len(cohort_subscriptions) > cohort["learners"]:
            print(f"Number of subscriptions in cohort is more than desired.")
            for subscription in cohort_subscriptions[cohort["learners"]:]:
                print(f"Reassigning {subscription['display_name']} to subscription pool.")
                for attempt in range(retry_attempts):
                    try:
                        mgmt_client.management_group_subscriptions.create(group_id=subscription_pool["name"], subscription_id=subscription["name"])
                    except HttpResponseError as error:
                        print(f"Attempt {attempt}/{retry_attempts} failed with the following message: '{error.message}'")
                        print("Waiting 60 seconds before retrying...")
                        sleep(seconds_before_retry)
                        continue
                    else:
                        break
                else:
                    raise Exception(f"Failed to assign desired number of subscriptions to subscription pool.")
        else:
            print(f"Cohort contains number of desired subscriptions.")
        
        print("Cohort details:")
        print(json.dumps(cohort_management_group, indent=4, sort_keys=True))
        print(json.dumps(get_management_group_subscriptions(credentials, cohort_management_group), indent=4, sort_keys=True))
        print()

    print("Subscription Pool details:")
    subscription_pool = get_subscription_pool(credentials)
    print(json.dumps(subscription_pool, indent=4, sort_keys=True))
    print(json.dumps(get_management_group_subscriptions(credentials, get_subscription_pool(credentials)), indent=4, sort_keys=True))
    