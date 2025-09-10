mutation ($subcampaignId: Int!, $input: SubcampaignIncomeMultiplierInput!) {
  updateSubcampaignIncomeMultiplier(subcampaignId: $subcampaignId, input: $input) {
    incomeMultiplier {
      manualFactor
      multiplierValue
      comment
    }
  }
}

variables (default):
{
  "subcampaignId": input,
  "input": {
    "manualFactor": 0.5,
    "comment": "initial setup"
  }
}

mutation UpdateSubcampaignCampaignStatus($subcampaignId: Int!, $input: UpdateSubcampaignCampaignStatusInput!) {
  updateSubcampaignCampaignStatus(subcampaignId: $subcampaignId, input: $input) {
    campaignStatus {
      status {
        value
      }
    }
  }
}}

{  "subcampaignId": null,
  "input": {
    "value": input [NEW, ACTIVE, READY, PAUSED]
    }
}

mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
  updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
    campaignStatus {
      startDate
      endDate
    }
  }
}

{
  "advertiserId": input,
  "subcampaignId": input,
  "input": {
    "startDate": input,
    "endDate": input
  }
}

mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
  updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
    basicInfo {
      name
    }
  }
}

{  "subcampaignId": input,
  "input": {
    "name": input
  }
}

mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
  updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
    properties {
      dataCenters
    }
  }
}

{  "subcampaignId": input,
  "input": {
    "dataCenters": input
  }
}

mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
  updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
    properties {
      forceEnableGdprMacros
    }
  }
}

{  "subcampaignId": input,
  "input": {
    "forceEnableGdprMacros": FALSE
  }
}

mutation updateSubcampaignLimits($subcampaignId: Int!, $input: SubcampaignLimitsInput!) {
  updateSubcampaignLimits(subcampaignId: $subcampaignId, input: $input) {
    limits {
      budget {
        daily
        monthly
        comment
        updatedAt
        updatedBy
      },
      events {
        impressions {
          daily
          monthly
          lifetime
        }
        clicks {
          daily
          monthly
          lifetime
        }
        capping {
          userImpressionsDaily
        }
        updatedAt
        updatedBy
      }
    }
  }
}

{
  "subcampaignId": input,
  "input": {
    "budget": {
      "daily": input,
      "monthly": input,
      "comment": "initial setup"
    },
    "events": {
      "impressions": {
        "daily": input,
        "monthly": input,
        "lifetime": input
      },
      "clicks": {
        "daily": input,
        "monthly": input,
        "lifetime": input
      },
      "capping": {
        "userImpressionsDaily": input
      },
      "comment": "initial setup"
    }
  }
}


mutation ($subcampaignId: Int!, $input: GeotargetingInput!) {
  updateSubcampaignGeotargeting(subcampaignId: $subcampaignId, input: $input) {
    subcampaignId
    geotargeting {
      includedCountries {
        country
        includedRegions
        excludedRegions
        includedCities {
          region
          city
        }
        excludedCities {
          region
          city
        }
      }
      excludedCountries
    }
  }
}

{
  "subcampaignId": input,
  "input": {
    "includedCountries": [
      {
        "country": input,
        "includedRegions": [
          input
        ],
        "includedCities": [
          {
            "region": input,
            "city": input
          }
        ],
        "excludedRegions": [
          input
        ],
        "excludedCities": [
          {
            "region": input,
            "city": input
          }
        ]
      }
    ]
  }
}

mutation UpdateSubcampaignTargetingPolicy(
  $subcampaignId: Int!
  $input: SubcampaignTargetingPolicyInput!
) {
  updateSubcampaignTargetingPolicy(
    subcampaignId: $subcampaignId
    input: $input
  ) {
    subcampaignId
    targetingPolicy {
      adApiFrameworkPolicy {
        supportedAdApiFrameworks
      }
      dealPolicy {
        allowedDeals {
          id
          identifier
          ssp
        }
        notAllowedDeals {
          id
          identifier
          ssp
        }
      }
      deviceTypePolicy {
        allowedDeviceTypes
        notAllowedDeviceTypes
      }
      placementEnvironmentPolicy {
        allowedPlacementEnvironments
        notAllowedPlacementEnvironments
      }
      sspPolicy {
        allowedSsps
        notAllowedSsps
      }
      userPolicy {
        allowOneTagBids
        buckets {
          minGroupId
          maxGroupId
        }
        ipRanges {
          allowedIpRanges
          notAllowedIpRanges
        }
        profileIdentifiers {
          allowedProfileIdentifierTypes
          notAllowedProfileIdentifierTypes
        }
        userSegments
      }
    }
  }
}


{
  "subcampaignId": input,
  "input": {
    "adApiFrameworkPolicy": {
      "supportedAdApiFrameworks": [
        input
      ]
    },
    "dealPolicy": {
      "allowedDeals": [
        input
      ],
      "notAllowedDeals": [
        input
      ]
    },
    "deviceTypePolicy": {
      "allowedDeviceTypes": [
        input
      ],
      "notAllowedDeviceTypes": [
        input
      ]
    },
    "placementEnvironmentPolicy": {
      "allowedPlacementEnvironments": [
        input
      ],
      "notAllowedPlacementEnvironments": [
        input
      ]
    },
    "sspPolicy": {
      "allowedSsps": [
        input
      ]
    },
    "userPolicy": {
      "allowOneTagBids": true,
      "ipRanges": {
        "allowedIpRanges": [
          input
        ],
        "notAllowedIpRanges": [
          input
        ]
      },
      "profileIdentifiers": {
        "allowedProfileIdentifierTypes": [
          input
        ],
        "notAllowedProfileIdentifierTypes": [
          input
        ]
      },
      "userSegments": [
        "BUYERS",
        "NEW",
        "VISITORS",
        "SHOPPERS"
      ]
    }
  }
}

mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
  updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
    properties {
      subcampaignType
    }
  }
}

{
  "subcampaignId": input,
  "input": {
    "subcampaignType": "performance-retargeting"
  }
}

mutation UpdateSubcampaignInfo($subcampaignId: Int!, $input: UpdateSubcampaignInfoInput!) {
  updateSubcampaignInfo(subcampaignId: $subcampaignId, input: $input) {
    landingMacro {
      defaultUrl {
        url
      }
    }
  }
}

{
  "subcampaignId": input,
  "input": {
    "url": "https://www.rtbhouse.com/blog?utm_source=rtbhouse&utm_medium=performance&utm_campaign=NAZWA_KAMPANII&rtbhc={RTBHC}"
  }
}

mutation UpdateSubcampaignTargetingPolicy($subcampaignId: Int!, $input: SubcampaignTargetingPolicyInput!) {
  updateSubcampaignTargetingPolicy(subcampaignId: $subcampaignId, input: $input) {
    targetingPolicy {
      inAppsPolicy {
        fullscreenMobilePlacement
      }
    }
  }
}

{
  "subcampaignId": input,
  "input": {
    "fullscreenMobilePlacement": input [ONLY_REWARDED, ONLY_INTERSTITIAL, ONLY_REWARDED_AND_INTERSTITIAL, REWARDED_AND_INTERSTITIAL_NOT_ALLOWED]
  }
}