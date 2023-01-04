#!/bin/bash

cohorts=$(cat ../terraform/config.yaml | yq -M ".cohorts")
subscription_pool_name=$(az account management-group list -o json | jq -r '.[] | select(.displayName=="Subscription Pool") | .name')

for cohort in $cohorts
do
    available_subscriptions_ids=$(az account management-group subscription show-sub-under-mg --name $subscription_pool_name -o json | jq -r ".[].name")
    count=
    while
done


echo $available_subscriptions

az account management-group subscription add --name $cohort_name --subscription $subscription_name