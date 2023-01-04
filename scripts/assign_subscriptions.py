from azure.identity import AzureCliCredential

from operations import open_config
from operations.setters import assign_subscriptions

def main():
    # config contains the desired state
    config = open_config("../config.yaml")
    # should probably authenticate using a service account rather than using CLI credentials
    credentials = AzureCliCredential()

    assign_subscriptions(credentials, config["cohorts"])

if __name__ == "__main__":
    main()
