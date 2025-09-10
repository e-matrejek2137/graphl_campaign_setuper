query GetSubcampaign($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      ...Subcampaign
      __typename
    }
    __typename
  }
}

fragment Subcampaign on Subcampaign {
  subcampaignId
  basicInfo {
    name
    labels
    __typename
  }
  info {
    archivedAt
    hash
    type
    __typename
  }
  campaignStatus {
    pausePeriods {
      ...PausePeriod
      __typename
    }
    emergencyPause {
      combinedEmergencyPauseEnabled
      contextAI {
        comment
        __typename
      }
      __typename
    }
    status {
      value
      __typename
    }
    __typename
  }
  synchronizationErrors {
    count
    __typename
  }
  __typename
}

fragment PausePeriod on PausePeriod {
  start
  end
  __typename
}

query GetSubcampaignNavigationData($advertiserId: Int!, $subcampaignId: Int!, $paths: [String!]!) {
  subcampaignModifiedPaths(subcampaignId: $subcampaignId, paths: $paths) {
    path
    modified
    __typename
  }
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      campaignSettingsOverrides {
        overridesCount
        __typename
      }
      __typename
    }
    __typename
  }
}

query GetSubcampaignOverview($advertiserId: Int!, $subcampaignId: Int!) {
  dicts {
    ...DictsOverview
    __typename
  }
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    trafficQuality {
      ...AdvertiserTrafficQualityOverview
      __typename
    }
    modelsTrainingConfig {
      ...AdvertiserModelsTrainingConfig
      __typename
    }
    externalProperties {
      models {
        ...ExternalPropertiesModels
        __typename
      }
      __typename
    }
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      budgetSpend {
        ...BudgetSpendInfo
        __typename
      }
      budgetCustomPeriods {
        ...BudgetCustomPeriodInfo
        __typename
      }
      limitsSettings {
        ...LimitsSettings
        __typename
      }
      limits {
        ...SubcampaignLimitsOverview
        __typename
      }
      internalLimits {
        ...InternalLimits
        __typename
      }
      biddingModel {
        ...BiddingModel
        comment
        __typename
      }
      incomeMultiplier {
        ...SubcampaignIncomeMultiplier
        __typename
      }
      creatives {
        ...SubcampaignCreative
        __typename
      }
      invoiceRateCard {
        ...SubcampaignInvoiceRateCard
        __typename
      }
      tagsTargeting {
        ...TagsTargetingOverview
        __typename
      }
      targetingPolicy {
        ...SubcampaignTargetingPolicyOverview
        __typename
      }
      geotargeting {
        ...GeotargetingOverview
        __typename
      }
      trafficQuality {
        ...SubcampaignTrafficQualityOverview
        __typename
      }
      landingMacro {
        ...SubcampaignLandingMacro
        __typename
      }
      offersSample(limit: 1) {
        ...OffersSampleOffer
        __typename
      }
      campaignStatus {
        ...SubcampaignCampaignStatusOverview
        __typename
      }
      properties {
        ...SubcampaignPropertiesOverview
        __typename
      }
      groups {
        ...SubcampaignGroupsOverview
        __typename
      }
      impressionPolicies {
        ...SubcampaignImpressionPoliciesOverview
        __typename
      }
      offersChoosing {
        ...SubcampaignOffersChoosingBasic
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment DictsOverview on Dicts {
  sellerDefinedAudiences {
    description
    value
    version
    __typename
  }
  topicsApiTopics {
    description
    value
    version
    __typename
  }
  __typename
}

fragment AdvertiserTrafficQualityOverview on AdvertiserTrafficQuality {
  maxBr
  bounceBestTrafficFraction
  comment
  conversions {
    ...TrafficQualityConversionsOverview
    __typename
  }
  clicks {
    ...TrafficQualityClicksOverview
    __typename
  }
  viewability {
    ...TrafficQualityViewabilityOverview
    __typename
  }
  video {
    ...TrafficQualityVideoOverview
    __typename
  }
  fraudPreventionPolicy {
    ...FraudPreventionPolicyOverview
    __typename
  }
  __typename
}

fragment TrafficQualityConversionsOverview on TrafficQualityConversions {
  conversionClass
  conversionSubclass
  minCr
  maxCr
  minCv
  maxCv
  __typename
}

fragment TrafficQualityClicksOverview on TrafficQualityClicks {
  minCtr
  maxCtr
  __typename
}

fragment TrafficQualityViewabilityOverview on TrafficQualityViewability {
  minValue
  viewabilityPredictionMode
  allowUnknown
  __typename
}

fragment TrafficQualityVideoOverview on TrafficQualityVideo {
  minVcr
  allowedVideoPlacements
  notAllowedVideoPlacements
  allowedVideoPlaybackMethods
  notAllowedVideoPlaybackMethods
  skippable
  clickable
  __typename
}

fragment FraudPreventionPolicyOverview on FraudPreventionPolicy {
  fraudDetectionProviders {
    hosting
    internalBeta
    doubleVerify
    __typename
  }
  __typename
}

fragment AdvertiserModelsTrainingConfig on AdvertiserModelsTrainingConfig {
  supportedConversions {
    conversionClass
    conversionSubclass
    __typename
  }
  resetDay
  landedClickOptimizationEnabled
  __typename
}

fragment ExternalPropertiesModels on ExternalPropertiesModels {
  landedClickOptimizationEnabled
  __typename
}

fragment BudgetSpendInfo on BudgetSpend {
  currentDay {
    ...BudgetPeriodSpend
    __typename
  }
  currentMonth {
    ...BudgetPeriodSpend
    __typename
  }
  currentCustomPeriod {
    ...BudgetPeriodSpend
    __typename
  }
  currentFiscalPeriod {
    ...BudgetPeriodSpend
    __typename
  }
  __typename
}

fragment BudgetPeriodSpend on BudgetPeriodSpend {
  remainingHours
  totalHours
  spent
  spentUntilYesterday
  startDate
  endDate
  totalBudget
  __typename
}

fragment BudgetCustomPeriodInfo on BudgetCustomPeriod {
  periodId
  name
  budget
  startDate
  endDate
  __typename
}

fragment LimitsSettings on LimitsSettings {
  budgetAutoAdjuster {
    ...BudgetAutoAdjusterSettings
    __typename
  }
  syncMonthlyBudgetLimitWithPassport
  __typename
}

fragment BudgetAutoAdjusterSettings on BudgetAutoAdjusterSettings {
  enabled
  mode
  dailyBudgetMultiplier
  defaultDailyBudget
  __typename
}

fragment SubcampaignLimitsOverview on SubcampaignLimits {
  events {
    impressions {
      daily
      monthly
      lifetime
      __typename
    }
    clicks {
      daily
      monthly
      lifetime
      __typename
    }
    capping {
      userImpressionsDaily
      __typename
    }
    comment
    __typename
  }
  budget {
    lifetime
    __typename
  }
  __typename
}

fragment InternalLimits on SubcampaignInternalLimits {
  sspSpendDaily
  __typename
}

fragment BiddingModel on BiddingModel {
  cpc {
    ...SegmentValues
    __typename
  }
  cpaPostClick {
    ...SegmentValues
    __typename
  }
  cpsPostClick {
    ...SegmentValues
    __typename
  }
  cpm {
    ...SegmentValues
    __typename
  }
  cpcv {
    ...SegmentValues
    __typename
  }
  __typename
}

fragment SegmentValues on SegmentValues {
  visitors
  shoppers
  buyers
  new
  __typename
}

fragment SubcampaignIncomeMultiplier on SubcampaignIncomeMultiplier {
  manualFactor
  multiplierValue
  comment
  updatedAt
  updatedBy
  __typename
}

fragment SubcampaignCreative on Creative {
  creativeId
  __typename
}

fragment SubcampaignInvoiceRateCard on InvoiceRateCard {
  invoiceRateCardId
  info {
    name
    __typename
  }
  conversions {
    ...SubcampaignInvoiceRateCardConversions
    __typename
  }
  clicks {
    rates {
      ...Rates
      __typename
    }
    __typename
  }
  impressions {
    rates {
      ...Rates
      __typename
    }
    cpwpRates {
      ...Rates
      __typename
    }
    vcpmRates {
      ...Rates
      __typename
    }
    activeAudioGoal {
      rates {
        ...Rates
        __typename
      }
      __typename
    }
    activeVideoGoal {
      rates {
        ...Rates
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment SubcampaignInvoiceRateCardConversions on InvoiceRateCardConversions {
  conversionClasses {
    conversionClass
    conversionSubclass
    rates {
      cpa {
        postClick {
          ...Rates
          __typename
        }
        postView {
          ...Rates
          __typename
        }
        __typename
      }
      cps {
        postClick {
          ...Rates
          __typename
        }
        postView {
          ...Rates
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment Rates on InvoiceRateCardRates {
  buyers
  shoppers
  visitors
  newUsers
  __typename
}

fragment TagsTargetingOverview on TagsTargeting {
  description
  __typename
}

fragment SubcampaignTargetingPolicyOverview on SubcampaignTargetingPolicy {
  mobileEnvironmentPolicy
  adApiFrameworkPolicy {
    ...AdApiFrameworkPolicyOverview
    __typename
  }
  biddingProfilePolicy {
    identifiedTrafficBiddingMode
    cappingImpressionsLimit
    cappingFrequencyDays
    __typename
  }
  browserPolicy {
    ...BrowserPolicyOverview
    __typename
  }
  dealPolicy {
    ...DealPolicyOverview
    __typename
  }
  deviceTypePolicy {
    ...DeviceTypePolicyOverview
    __typename
  }
  inAppsPolicy {
    ...InAppsPolicyOverview
    __typename
  }
  operatingSystemPolicy {
    ...OperatingSystemPolicyOverview
    __typename
  }
  placementEnvironmentPolicy {
    ...PlacementEnvironmentPolicyOverview
    __typename
  }
  sellerDefinedAudiencesPolicy {
    ...SellerDefinedAudiencesPolicyOverview
    __typename
  }
  sspPolicy {
    ...SspPolicyOverview
    __typename
  }
  topicsApiPolicy {
    ...TopicsApiPolicyOverview
    __typename
  }
  userPolicy {
    ...UserPolicyOverview
    __typename
  }
  contextualUrlRelatedLabelsPolicy {
    ...ContextualUrlRelatedLabelsPolicyOverview
    __typename
  }
  userLabelsPolicy {
    ...UserLabelsPolicyOverview
    __typename
  }
  siteRankingPolicy {
    ...SiteRankingPolicyOverview
    __typename
  }
  inventoryTrafficTransparency {
    ...InventoryTrafficTransparencyOverview
    __typename
  }
  __typename
}

fragment AdApiFrameworkPolicyOverview on AdApiFrameworkPolicy {
  supportedAdApiFrameworks
  __typename
}

fragment BrowserPolicyOverview on BrowserPolicy {
  allowedBrowsers
  notAllowedBrowsers
  __typename
}

fragment DealPolicyOverview on DealPolicy {
  allowedDeals {
    ...PrivateDealOverview
    __typename
  }
  notAllowedDeals {
    ...PrivateDealOverview
    __typename
  }
  __typename
}

fragment PrivateDealOverview on PrivateDeal {
  id
  identifier
  ssp
  __typename
}

fragment DeviceTypePolicyOverview on DeviceTypePolicy {
  allowedDeviceTypes
  notAllowedDeviceTypes
  __typename
}

fragment InAppsPolicyOverview on InAppsPolicy {
  fullscreenMobilePlacement
  __typename
}

fragment OperatingSystemPolicyOverview on OperatingSystemPolicy {
  allowedOperatingSystems
  notAllowedOperatingSystems
  __typename
}

fragment PlacementEnvironmentPolicyOverview on PlacementEnvironmentPolicy {
  allowedPlacementEnvironments
  notAllowedPlacementEnvironments
  __typename
}

fragment SellerDefinedAudiencesPolicyOverview on SellerDefinedAudiencesPolicy {
  forbiddenSellerDefinedAudiences
  rejectBidsWithoutSda
  requiredSellerDefinedAudiences
  __typename
}

fragment SspPolicyOverview on SspPolicy {
  allowedSsps
  notAllowedSsps
  __typename
}

fragment TopicsApiPolicyOverview on TopicsApiPolicy {
  forbiddenPublisherTopics
  rejectBidsWithoutTopics
  requiredPublisherTopics
  __typename
}

fragment UserPolicyOverview on UserPolicy {
  allowOneTagBids
  userSegments
  ipRanges {
    allowedIpRanges
    notAllowedIpRanges
    __typename
  }
  profileIdentifiers {
    allowedProfileIdentifierTypes
    notAllowedProfileIdentifierTypes
    __typename
  }
  buckets {
    minGroupId
    maxGroupId
    __typename
  }
  __typename
}

fragment ContextualUrlRelatedLabelsPolicyOverview on ContextualUrlRelatedLabelsPolicy {
  labelsTargetings {
    ...UrlLabelsTargeting
    __typename
  }
  __typename
}

fragment UrlLabelsTargeting on LabelsTargeting {
  notAllowedLabels {
    ...TargetingLabel
    __typename
  }
  allowedLabels {
    ...TargetingLabel
    __typename
  }
  urlLabelType {
    ...TargetingLabelType
    __typename
  }
  __typename
}

fragment TargetingLabel on UrlLabel {
  id
  name
  status
  subtype
  __typename
}

fragment TargetingLabelType on UrlLabelType {
  id
  name
  __typename
}

fragment UserLabelsPolicyOverview on UserLabelsPolicy {
  userLabelsTargetings {
    ...UserLabelsTargeting
    __typename
  }
  __typename
}

fragment UserLabelsTargeting on UserLabelsTargeting {
  urlLabelType {
    ...TargetingLabelType
    __typename
  }
  conditions {
    ...UserLabelsCondition
    __typename
  }
  __typename
}

fragment UserLabelsCondition on UserLabelsCondition {
  labels {
    ...TargetingLabel
    __typename
  }
  period
  minimumLabelsCount
  matchMode
  includeGlobalLabels
  __typename
}

fragment SiteRankingPolicyOverview on SiteRankingPolicy {
  country
  version
  __typename
}

fragment InventoryTrafficTransparencyOverview on InventoryTrafficTransparency {
  authorizedInventory
  rejectAnonymousTraffic
  rejectSemiTransparentTraffic
  __typename
}

fragment GeotargetingOverview on Geotargeting {
  includedCountries {
    country
    includedRegions
    excludedRegions
    includedCities {
      city
      region
      __typename
    }
    excludedCities {
      city
      region
      __typename
    }
    __typename
  }
  excludedCountries
  __typename
}

fragment SubcampaignTrafficQualityOverview on TrafficQuality {
  maxBr
  bounceBestTrafficFraction
  comment
  conversions {
    ...TrafficQualityConversionsOverview
    __typename
  }
  clicks {
    ...TrafficQualityClicksOverview
    __typename
  }
  viewability {
    ...TrafficQualityViewabilityOverview
    __typename
  }
  video {
    ...TrafficQualityVideoOverview
    __typename
  }
  fraudPreventionPolicy {
    ...FraudPreventionPolicyOverview
    __typename
  }
  __typename
}

fragment SubcampaignLandingMacro on SubcampaignLandingMacro {
  landing
  externalAdLandingSuffix
  defaultUrl {
    url
    overrideLandingUrl
    __typename
  }
  __typename
}

fragment OffersSampleOffer on OffersSampleOffer {
  url
  customProperties {
    key
    value
    __typename
  }
  __typename
}

fragment SubcampaignCampaignStatusOverview on SubcampaignCampaignStatus {
  startDate
  endDate
  pausePeriods {
    ...PausePeriodOverview
    __typename
  }
  __typename
}

fragment PausePeriodOverview on PausePeriod {
  start
  end
  __typename
}

fragment SubcampaignPropertiesOverview on SubcampaignProperties {
  subcampaignType
  upperFunnelStage
  dataCenters
  sensitiveCategory
  product {
    displayName
    __typename
  }
  __typename
}

fragment SubcampaignGroupsOverview on SubcampaignGroups {
  client {
    groupHash
    displayName
    __typename
  }
  financial {
    groupHash
    displayName
    __typename
  }
  __typename
}

fragment SubcampaignImpressionPoliciesOverview on SubcampaignImpressionPolicies {
  policies {
    ...SubcampaignImpressionPolicyOverview
    __typename
  }
  __typename
}

fragment SubcampaignImpressionPolicyOverview on SubcampaignImpressionPolicy {
  description
  atLeastOccurrencesNumber
  atMostOccurrencesNumber
  matchMode
  matchConditions {
    ageMin
    ageMax
    limitImpressionsToAudcOnly
    includedSubcampaigns {
      ...SubcampaignImpressionPolicySubcampaignOverview
      __typename
    }
    excludedSubcampaigns {
      ...SubcampaignImpressionPolicySubcampaignOverview
      __typename
    }
    __typename
  }
  __typename
}

fragment SubcampaignImpressionPolicySubcampaignOverview on Subcampaign {
  advertiserId
  subcampaignId
  basicInfo {
    name
    __typename
  }
  campaignStatus {
    status {
      value
      __typename
    }
    __typename
  }
  info {
    archivedAt
    __typename
  }
  __typename
}

fragment SubcampaignOffersChoosingBasic on SubcampaignOffersChoosing {
  hints {
    avoidBoughtOffers
    __typename
  }
  constraints {
    whitelistedCategories {
      manualCategories {
        ... on OfferCategoryBasicData {
          id
          identifier
          name
          __typename
        }
        ... on UnknownOfferCategoryBasicData {
          id
          __typename
        }
        __typename
      }
      __typename
    }
    blacklistedCategories {
      manualCategories {
        ... on OfferCategoryBasicData {
          id
          identifier
          name
          __typename
        }
        ... on UnknownOfferCategoryBasicData {
          id
          __typename
        }
        __typename
      }
      __typename
    }
    greylistedCategories {
      manualCategories {
        ... on OfferCategoryBasicData {
          id
          identifier
          name
          __typename
        }
        ... on UnknownOfferCategoryBasicData {
          id
          __typename
        }
        __typename
      }
      __typename
    }
    greylistedCategoryDaysOfValidity
    blacklistedOffers {
      ... on OfferBasicData {
        id
        identifier
        name
        __typename
      }
      ... on UnknownOfferBasicData {
        id
        __typename
      }
      __typename
    }
    requiredOfferLabels
    rejectedOfferLabels
    offerCategoriesRegexps {
      whitelistedCategoryNameRegexp
      greylistedCategoryNameRegexp
      blacklistedCategoryNameRegexp
      __typename
    }
    __typename
  }
  obligatoryOffers {
    ... on OfferBasicData {
      id
      identifier
      name
      __typename
    }
    ... on UnknownOfferBasicData {
      id
      __typename
    }
    __typename
  }
  intentGptRequiredOffersRatio
  __typename
}

query GetSubcampaignSettingsStatusData($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    invoiceRateCards {
      ...SubcampaignInvoiceRateCard
      __typename
    }
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      campaignStatus {
        ...SubcampaignSettingsCampaignStatus
        __typename
      }
      invoiceRateCard {
        ...SubcampaignInvoiceRateCard
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignInvoiceRateCard on InvoiceRateCard {
  invoiceRateCardId
  info {
    name
    __typename
  }
  conversions {
    ...SubcampaignInvoiceRateCardConversions
    __typename
  }
  clicks {
    rates {
      ...Rates
      __typename
    }
    __typename
  }
  impressions {
    rates {
      ...Rates
      __typename
    }
    cpwpRates {
      ...Rates
      __typename
    }
    vcpmRates {
      ...Rates
      __typename
    }
    activeAudioGoal {
      rates {
        ...Rates
        __typename
      }
      __typename
    }
    activeVideoGoal {
      rates {
        ...Rates
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment SubcampaignInvoiceRateCardConversions on InvoiceRateCardConversions {
  conversionClasses {
    conversionClass
    conversionSubclass
    rates {
      cpa {
        postClick {
          ...Rates
          __typename
        }
        postView {
          ...Rates
          __typename
        }
        __typename
      }
      cps {
        postClick {
          ...Rates
          __typename
        }
        postView {
          ...Rates
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment Rates on InvoiceRateCardRates {
  buyers
  shoppers
  visitors
  newUsers
  __typename
}

fragment SubcampaignSettingsCampaignStatus on SubcampaignCampaignStatus {
  startDate
  endDate
  status {
    ...SubcampaignSettingsStatusInfo
    __typename
  }
  pausePeriods {
    ...PausePeriod
    __typename
  }
  __typename
}

fragment SubcampaignSettingsStatusInfo on SubcampaignCampaignStatusInfo {
  value
  comment
  updatedAt
  updatedBy
  __typename
}

fragment PausePeriod on PausePeriod {
  start
  end
  __typename
}

query SubcampaignLandingMacro($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      landingMacro {
        ...SubcampaignLandingMacro
        __typename
      }
      macrosTransformations {
        name
        __typename
      }
      offersSample(limit: 1) {
        ...OffersSampleOffer
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignLandingMacro on SubcampaignLandingMacro {
  landing
  externalAdLandingSuffix
  defaultUrl {
    url
    overrideLandingUrl
    __typename
  }
  __typename
}

fragment OffersSampleOffer on OffersSampleOffer {
  url
  customProperties {
    key
    value
    __typename
  }
  __typename
}

query GetSubcampaignImpressionTracking($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      tracking {
        ...ImpressionTracking
        __typename
      }
      __typename
    }
    __typename
  }
  dicts {
    eventTypes
    cookieTypes
    __typename
  }
}

fragment ImpressionTracking on SubcampaignTracking {
  impressionTracking {
    trackingCode
    trackingUrls
    __typename
  }
  streamingVideoImpressionTracking {
    omUrl
    vpaidUrl
    __typename
  }
  externalTrackers {
    trackingUrl
    targetedEventTypes
    targetedCookieTypes
    __typename
  }
  __typename
}

query GetSubcampaignTagsTargeting($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      tagsTargeting {
        description
        expression
        policies {
          ...TagsTargetingPolicy
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment TagsTargetingPolicy on TagsTargetingPolicy {
  identifier
  filterMode
  filterConditions {
    ...TagsTargetingConditions
    __typename
  }
  lookupMode
  matchMode
  atLeastOccurrencesNumber
  matchConditions {
    ...TagsTargetingConditions
    __typename
  }
  __typename
}

fragment TagsTargetingConditions on TagsTargetingConditions {
  allowedTypes
  offers {
    ... on OfferBasicData {
      id
      identifier
      name
      __typename
    }
    ... on SpecialOfferBasicData {
      id
      identifier
      name
      __typename
    }
    ... on UnknownOfferBasicData {
      id
      __typename
    }
    __typename
  }
  categories {
    ... on OfferCategoryBasicData {
      id
      identifier
      name
      __typename
    }
    ... on SpecialOfferCategoryBasicData {
      id
      identifier
      name
      __typename
    }
    ... on UnknownOfferCategoryBasicData {
      id
      __typename
    }
    __typename
  }
  customTagKeys
  customTagValues
  systemTagKeys
  systemTagValues
  otherTagValues
  minConversionValue
  maxConversionValue
  conversionSubclasses
  minAge
  maxAge
  minDate
  maxDate
  period
  __typename
}

query GetTagsTargetingSelectableData($advertiserId: Int!) {
  dicts {
    advertiserUserTags
    __typename
  }
  conversionSubclasses {
    conversionSubclass
    __typename
  }
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    specialOfferCategories {
      id
      name
      __typename
    }
    feed {
      identifier
      offerCategories {
        id
        name
        __typename
      }
      __typename
    }
    taggingConfig {
      ...TagsTargetingTaggingConfig
      __typename
    }
    __typename
  }
}

fragment TagsTargetingTaggingConfig on TaggingConfig {
  customTagConstraints {
    name
    __typename
  }
  __typename
}

query GetSubcampaignLimits($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      limits {
        ...SubcampaignLimits
        __typename
      }
      limitsSettings {
        ...LimitsSettings
        __typename
      }
      budgetCustomPeriods {
        ...BudgetCustomPeriodInfo
        __typename
      }
      budgetFiscalPeriods {
        ...BudgetFiscalPeriods
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignLimits on SubcampaignLimits {
  budget {
    daily
    monthly
    lifetime
    __typename
  }
  __typename
}

fragment LimitsSettings on LimitsSettings {
  budgetAutoAdjuster {
    ...BudgetAutoAdjusterSettings
    __typename
  }
  syncMonthlyBudgetLimitWithPassport
  __typename
}

fragment BudgetAutoAdjusterSettings on BudgetAutoAdjusterSettings {
  enabled
  mode
  dailyBudgetMultiplier
  defaultDailyBudget
  __typename
}

fragment BudgetCustomPeriodInfo on BudgetCustomPeriod {
  periodId
  name
  budget
  startDate
  endDate
  __typename
}

fragment BudgetFiscalPeriods on BudgetFiscalPeriods {
  current {
    ...BudgetFiscalPeriod
    __typename
  }
  upcoming {
    ...BudgetFiscalPeriod
    __typename
  }
  __typename
}

fragment BudgetFiscalPeriod on BudgetFiscalPeriod {
  periodId
  name
  budget
  startDate
  endDate
  __typename
}

query GetSubcampaignBudgetSpend($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      budgetSpend {
        ...BudgetSpendInfo
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment BudgetSpendInfo on BudgetSpend {
  currentDay {
    ...BudgetPeriodSpend
    __typename
  }
  currentMonth {
    ...BudgetPeriodSpend
    __typename
  }
  currentCustomPeriod {
    ...BudgetPeriodSpend
    __typename
  }
  currentFiscalPeriod {
    ...BudgetPeriodSpend
    __typename
  }
  __typename
}

fragment BudgetPeriodSpend on BudgetPeriodSpend {
  remainingHours
  totalHours
  spent
  spentUntilYesterday
  startDate
  endDate
  totalBudget
  __typename
}

query GetSubcampaignEventsLimits($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      limits {
        ...SubcampaignEventsLimits
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignEventsLimits on SubcampaignLimits {
  events {
    impressions {
      daily
      monthly
      lifetime
      __typename
    }
    clicks {
      daily
      monthly
      lifetime
      __typename
    }
    capping {
      userImpressionsDaily
      __typename
    }
    comment
    updatedAt
    updatedBy
    __typename
  }
  __typename
}

query GetSubcampaignGeneralTargetingPolicy($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    campaignTypeSettings {
      platformType
      __typename
    }
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      properties {
        sensitiveCategory
        __typename
      }
      targetingPolicy {
        ...SubcampaignGeneralTargetingPolicy
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignGeneralTargetingPolicy on SubcampaignTargetingPolicy {
  adApiFrameworkPolicy {
    ...AdApiFrameworkPolicy
    __typename
  }
  biddingProfilePolicy {
    ...BiddingProfilePolicy
    __typename
  }
  dealPolicy {
    ...DealPolicy
    __typename
  }
  deviceTypePolicy {
    ...DeviceTypePolicy
    __typename
  }
  placementEnvironmentPolicy {
    ...PlacementEnvironmentPolicy
    __typename
  }
  sspPolicy {
    ...SspPolicy
    __typename
  }
  userPolicy {
    ...UserPolicy
    __typename
  }
  inAppsPolicy {
    ...InAppsPolicy
    __typename
  }
  siteRankingPolicy {
    ...SiteRankingPolicy
    __typename
  }
  inventoryTrafficTransparency {
    ...InventoryTrafficTransparency
    __typename
  }
  __typename
}

fragment AdApiFrameworkPolicy on AdApiFrameworkPolicy {
  supportedAdApiFrameworks
  __typename
}

fragment BiddingProfilePolicy on BiddingProfilePolicy {
  cappingFrequencyDays
  cappingImpressionsLimit
  identifiedTrafficBiddingMode
  __typename
}

fragment DealPolicy on DealPolicy {
  allowedDeals {
    ...PrivateDeal
    __typename
  }
  notAllowedDeals {
    ...PrivateDeal
    __typename
  }
  __typename
}

fragment PrivateDeal on PrivateDeal {
  id
  identifier
  ssp
  __typename
}

fragment DeviceTypePolicy on DeviceTypePolicy {
  allowedDeviceTypes
  notAllowedDeviceTypes
  __typename
}

fragment PlacementEnvironmentPolicy on PlacementEnvironmentPolicy {
  allowedPlacementEnvironments
  notAllowedPlacementEnvironments
  __typename
}

fragment SspPolicy on SspPolicy {
  allowedSsps
  notAllowedSsps
  __typename
}

fragment UserPolicy on UserPolicy {
  allowOneTagBids
  buckets {
    minGroupId
    maxGroupId
    __typename
  }
  ipRanges {
    allowedIpRanges
    notAllowedIpRanges
    __typename
  }
  profileIdentifiers {
    allowedProfileIdentifierTypes
    notAllowedProfileIdentifierTypes
    __typename
  }
  userSegments
  __typename
}

fragment InAppsPolicy on InAppsPolicy {
  fullscreenMobilePlacement
  __typename
}

fragment SiteRankingPolicy on SiteRankingPolicy {
  country
  version
  __typename
}

fragment InventoryTrafficTransparency on InventoryTrafficTransparency {
  authorizedInventory
  rejectAnonymousTraffic
  rejectSemiTransparentTraffic
  __typename
}

query GetGeneralTargetingPolicyDicts {
  dicts {
    ...GeneralTargetingPolicyDicts
    __typename
  }
}

fragment GeneralTargetingPolicyDicts on Dicts {
  profileIdentifierTypes
  sensitiveCategorySspPolicies {
    category
    allowedSsps
    notAllowedSsps
    __typename
  }
  ssps
  siteRankingCountries
  __typename
}

query GetSubcampaignOSAndBrowserTargetingPolicy($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      targetingPolicy {
        ...SubcampaignOSAndBrowserTargetingPolicy
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignOSAndBrowserTargetingPolicy on SubcampaignTargetingPolicy {
  browserPolicy {
    ...BrowserPolicy
    __typename
  }
  operatingSystemPolicy {
    ...OperatingSystemPolicy
    __typename
  }
  mobileEnvironmentPolicy
  __typename
}

fragment BrowserPolicy on BrowserPolicy {
  allowedBrowsers
  notAllowedBrowsers
  __typename
}

fragment OperatingSystemPolicy on OperatingSystemPolicy {
  allowedOperatingSystems
  notAllowedOperatingSystems
  __typename
}

query GetSubcampaignGeotargeting($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      ...SubcampaignGeoratgetingPreview
      __typename
    }
    __typename
  }
}

fragment SubcampaignGeoratgetingPreview on Subcampaign {
  ...SubcampaignPreviewBasicInfo
  geotargeting {
    ...Geotargeting
    __typename
  }
  __typename
}

fragment SubcampaignPreviewBasicInfo on Subcampaign {
  advertiserId
  subcampaignId
  basicInfo {
    name
    __typename
  }
  campaignStatus {
    status {
      value
      __typename
    }
    __typename
  }
  info {
    hash
    __typename
  }
  __typename
}

fragment Geotargeting on Geotargeting {
  excludedCountries
  includedCountries {
    ...GeotargetingIncludedCountry
    __typename
  }
  hints {
    path
    message
    __typename
  }
  __typename
}

fragment GeotargetingIncludedCountry on GeotargetingIncludedCountry {
  country
  excludedRegions
  includedRegions
  excludedCities {
    ...GeotargetingCity
    __typename
  }
  includedCities {
    ...GeotargetingCity
    __typename
  }
  __typename
}

fragment GeotargetingCity on GeotargetingCity {
  region
  city
  __typename
}

query GetSubcampaignImpressionPolicies($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      impressionPolicies {
        policies {
          ...ImpressionPolicy
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment ImpressionPolicy on SubcampaignImpressionPolicy {
  description
  atLeastOccurrencesNumber
  atMostOccurrencesNumber
  matchConditions {
    ...ImpressionPolicyMatchConditions
    __typename
  }
  matchMode
  __typename
}

fragment ImpressionPolicyMatchConditions on SubcampaignImpressionPolicyMatchConditions {
  ageMin
  ageMax
  includedSubcampaigns {
    subcampaignId
    basicInfo {
      name
      __typename
    }
    __typename
  }
  excludedSubcampaigns {
    subcampaignId
    basicInfo {
      name
      __typename
    }
    __typename
  }
  limitImpressionsToAudcOnly
  __typename
}

query GetImpressionPoliciesSubcampaigns($advertiserId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaigns {
      ...SelectableSubcampaignImpressionPolicies
      __typename
    }
    __typename
  }
}

fragment SelectableSubcampaignImpressionPolicies on Subcampaign {
  subcampaignId
  basicInfo {
    name
    __typename
  }
  campaignStatus {
    status {
      value
      __typename
    }
    __typename
  }
  info {
    archivedAt
    __typename
  }
  __typename
}

query GetSubcampaignTrafficQualityBasic($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      trafficQuality {
        ...TrafficQualityBasicSection
        ...TrafficQualityConversionsSection
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment TrafficQualityBasicSection on ITrafficQuality {
  clicks {
    ...TrafficQualityClicks
    __typename
  }
  comment
  updatedBy
  updatedAt
  __typename
}

fragment TrafficQualityClicks on TrafficQualityClicks {
  minCtr
  maxCtr
  __typename
}

fragment TrafficQualityConversionsSection on ITrafficQuality {
  conversions {
    ...TrafficQualityConversions
    __typename
  }
  __typename
}

fragment TrafficQualityConversions on TrafficQualityConversions {
  conversionClass
  conversionSubclass
  ...TrafficQualityConversionRates
  __typename
}

fragment TrafficQualityConversionRates on TrafficQualityConversions {
  minCv
  maxCv
  minCr
  maxCr
  __typename
}

query GetDropdownConversionSubclasses {
  conversionSubclasses {
    conversionClass
    conversionSubclass
    description
    __typename
  }
}

query GetAdvertiserBiddingParametersPreview($advertiserId: Int!, $isArchived: Boolean = null) {
  advertiser(advertiserId: $advertiserId) {
    ...AdvertiserBiddingParametersPreview
    subcampaigns(filters: {isArchived: {is: $isArchived}}) {
      ...SubcampaignBiddingParametersPreview
      __typename
    }
    __typename
  }
}

fragment AdvertiserBiddingParametersPreview on Advertiser {
  advertiserId
  biddingModel {
    ...BiddingModel
    __typename
  }
  incomeMultiplier {
    ...AdvertiserIncomeMultiplier
    __typename
  }
  __typename
}

fragment BiddingModel on BiddingModel {
  cpc {
    ...SegmentValues
    __typename
  }
  cpaPostClick {
    ...SegmentValues
    __typename
  }
  cpsPostClick {
    ...SegmentValues
    __typename
  }
  cpm {
    ...SegmentValues
    __typename
  }
  cpcv {
    ...SegmentValues
    __typename
  }
  __typename
}

fragment SegmentValues on SegmentValues {
  visitors
  shoppers
  buyers
  new
  __typename
}

fragment AdvertiserIncomeMultiplier on AdvertiserIncomeMultiplier {
  manualFactor
  comment
  updatedAt
  updatedBy
  __typename
}

fragment SubcampaignBiddingParametersPreview on Subcampaign {
  subcampaignId
  basicInfo {
    name
    __typename
  }
  campaignStatus {
    status {
      value
      __typename
    }
    __typename
  }
  info {
    archivedAt
    __typename
  }
  biddingModel {
    ...BiddingModel
    __typename
  }
  incomeMultiplier {
    ...SubcampaignIncomeMultiplier
    __typename
  }
  invoiceRateCard {
    ...SubcampaignInvoiceRateCard
    __typename
  }
  bidAdjustments {
    ...SubcampaignBidAdjustments
    __typename
  }
  __typename
}

fragment SubcampaignIncomeMultiplier on SubcampaignIncomeMultiplier {
  manualFactor
  multiplierValue
  comment
  updatedAt
  updatedBy
  __typename
}

fragment SubcampaignInvoiceRateCard on InvoiceRateCard {
  invoiceRateCardId
  info {
    name
    __typename
  }
  conversions {
    ...SubcampaignInvoiceRateCardConversions
    __typename
  }
  clicks {
    rates {
      ...Rates
      __typename
    }
    __typename
  }
  impressions {
    rates {
      ...Rates
      __typename
    }
    cpwpRates {
      ...Rates
      __typename
    }
    vcpmRates {
      ...Rates
      __typename
    }
    activeAudioGoal {
      rates {
        ...Rates
        __typename
      }
      __typename
    }
    activeVideoGoal {
      rates {
        ...Rates
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment SubcampaignInvoiceRateCardConversions on InvoiceRateCardConversions {
  conversionClasses {
    conversionClass
    conversionSubclass
    rates {
      cpa {
        postClick {
          ...Rates
          __typename
        }
        postView {
          ...Rates
          __typename
        }
        __typename
      }
      cps {
        postClick {
          ...Rates
          __typename
        }
        postView {
          ...Rates
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment Rates on InvoiceRateCardRates {
  buyers
  shoppers
  visitors
  newUsers
  __typename
}

fragment SubcampaignBidAdjustments on SubcampaignBidAdjustments {
  ...BidAdjustmentsSspRule
  ...BidAdjustmentsDeviceTypeRule
  ...BidAdjustmentsCountryRule
  ...BidAdjustmentsUrlLabelRule
  ...BidAdjustmentsTimeWindowRule
  ...BidAdjustmentsAdInterstitialRule
  ...BidAdjustmentsAdRewardedRule
  ...BidAdjustmentsVideoPlacementRule
  ...BidAdjustmentsCreativeRule
  __typename
}

fragment BidAdjustmentsSspRule on SubcampaignBidAdjustments {
  sspRules {
    matchingValues
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsDeviceTypeRule on SubcampaignBidAdjustments {
  deviceTypeRules {
    matchingValues
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsCountryRule on SubcampaignBidAdjustments {
  countryRules {
    matchingValues
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsUrlLabelRule on SubcampaignBidAdjustments {
  urlLabelRules {
    multiplier
    matchingUrlLabels {
      id
      typeId
      name
      __typename
    }
    __typename
  }
  __typename
}

fragment BidAdjustmentsTimeWindowRule on SubcampaignBidAdjustments {
  timeWindowRules {
    hourOfWeekFrom
    hourOfWeekTo
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsAdInterstitialRule on SubcampaignBidAdjustments {
  adInterstitialRules {
    matchingValue
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsAdRewardedRule on SubcampaignBidAdjustments {
  adRewardedRules {
    matchingValue
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsVideoPlacementRule on SubcampaignBidAdjustments {
  videoPlacementRules {
    matchingValues
    multiplier
    __typename
  }
  __typename
}

fragment BidAdjustmentsCreativeRule on SubcampaignBidAdjustments {
  creativeRules {
    matchingCreatives {
      creativeId
      __typename
    }
    multiplier
    __typename
  }
  __typename
}

query GetSubcampaignBiddingParametersInfo($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      budgetSpend {
        ...BudgetSpendInfo
        __typename
      }
      budgetCustomPeriods {
        ...BudgetCustomPeriodInfo
        __typename
      }
      limitsSettings {
        ...LimitsSettings
        __typename
      }
      targetingPolicy {
        userPolicy {
          allowOneTagBids
          __typename
        }
        __typename
      }
      trafficQuality {
        ...TrafficQualityBasicSummary
        ...TrafficQualityBrandingSummary
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment BudgetSpendInfo on BudgetSpend {
  currentDay {
    ...BudgetPeriodSpend
    __typename
  }
  currentMonth {
    ...BudgetPeriodSpend
    __typename
  }
  currentCustomPeriod {
    ...BudgetPeriodSpend
    __typename
  }
  currentFiscalPeriod {
    ...BudgetPeriodSpend
    __typename
  }
  __typename
}

fragment BudgetPeriodSpend on BudgetPeriodSpend {
  remainingHours
  totalHours
  spent
  spentUntilYesterday
  startDate
  endDate
  totalBudget
  __typename
}

fragment BudgetCustomPeriodInfo on BudgetCustomPeriod {
  periodId
  name
  budget
  startDate
  endDate
  __typename
}

fragment LimitsSettings on LimitsSettings {
  budgetAutoAdjuster {
    ...BudgetAutoAdjusterSettings
    __typename
  }
  syncMonthlyBudgetLimitWithPassport
  __typename
}

fragment BudgetAutoAdjusterSettings on BudgetAutoAdjusterSettings {
  enabled
  mode
  dailyBudgetMultiplier
  defaultDailyBudget
  __typename
}

fragment TrafficQualityBasicSummary on ITrafficQuality {
  conversions {
    minCr
    maxCr
    minCv
    maxCv
    __typename
  }
  clicks {
    minCtr
    maxCtr
    __typename
  }
  __typename
}

fragment TrafficQualityBrandingSummary on ITrafficQuality {
  maxBr
  bounceBestTrafficFraction
  viewability {
    minValue
    viewabilityPredictionMode
    __typename
  }
  video {
    minVcr
    __typename
  }
  __typename
}

query GetSubcampaignBiddingModelPreview($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    biddingModel {
      ...BiddingModelPreview
      __typename
    }
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      biddingModel {
        ...BiddingModelPreview
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment BiddingModelPreview on BiddingModel {
  comment
  updatedAt
  updatedBy
  cpc {
    ...SegmentValues
    __typename
  }
  cpaPostClick {
    ...SegmentValues
    __typename
  }
  cpsPostClick {
    ...SegmentValues
    __typename
  }
  cpm {
    ...SegmentValues
    __typename
  }
  cpcv {
    ...SegmentValues
    __typename
  }
  __typename
}

fragment SegmentValues on SegmentValues {
  visitors
  shoppers
  buyers
  new
  __typename
}

query GetSubcampaignIncomeMultiplierPreview($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    incomeMultiplier {
      manualFactor
      __typename
    }
    subcampaign(subcampaignId: $subcampaignId) {
      ...SubcampaignIncomeMultiplierPreview
      __typename
    }
    __typename
  }
}

fragment SubcampaignIncomeMultiplierPreview on Subcampaign {
  subcampaignId
  incomeMultiplier {
    ...SubcampaignIncomeMultiplier
    __typename
  }
  __typename
}

fragment SubcampaignIncomeMultiplier on SubcampaignIncomeMultiplier {
  manualFactor
  multiplierValue
  comment
  updatedAt
  updatedBy
  __typename
}

query GetSubcampaignBiddingParametersLogs($advertiserId: Int!, $subcampaignId: Int!, $first: Int, $afterCursor: String, $filters: BiddingParamsLogFilters) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      biddingParamsLogs(filters: $filters) {
        page(first: $first, afterCursor: $afterCursor) {
          pageInfo {
            hasNextPage
            endCursor
            __typename
          }
          results {
            ...SubcampaignBiddingParamsLog
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignBiddingParamsLog on SubcampaignBiddingParamsLog {
  createdAt
  createdBy {
    login
    userType
    __typename
  }
  modifiedField
  modifiedEntityType
  advertiserOptimizationModelLog {
    ...OptimizationModelLog
    __typename
  }
  advertiserIncomeMultiplierLog {
    ...IncomeMultiplierLog
    __typename
  }
  subcampaignOptimizationModelLog {
    ...OptimizationModelLog
    __typename
  }
  subcampaignIncomeMultiplierLog {
    ...IncomeMultiplierLog
    __typename
  }
  __typename
}

fragment OptimizationModelLog on OptimizationModelLog {
  cpa {
    ...SegmentValues
    __typename
  }
  cpc {
    ...SegmentValues
    __typename
  }
  cpm {
    ...SegmentValues
    __typename
  }
  cps {
    ...SegmentValues
    __typename
  }
  cpcv {
    ...SegmentValues
    __typename
  }
  comment
  __typename
}

fragment SegmentValues on SegmentValues {
  visitors
  shoppers
  buyers
  new
  __typename
}

fragment IncomeMultiplierLog on IncomeMultiplierLog {
  manualFactor
  multiplierValue
  comment
  __typename
}

query GetScheduledIncomeMultiplierUpdates($advertiserId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    info {
      hash
      name
      status
      __typename
    }
    incomeMultiplier {
      manualFactor
      comment
      __typename
    }
    scheduledIncomeMultiplierUpdates {
      ...AdvertiserScheduledIncomeMultiplierUpdate
      __typename
    }
    subcampaigns {
      subcampaignId
      basicInfo {
        name
        __typename
      }
      campaignStatus {
        status {
          value
          __typename
        }
        __typename
      }
      info {
        hash
        archivedAt
        __typename
      }
      incomeMultiplier {
        comment
        __typename
      }
      scheduledIncomeMultiplierUpdates {
        ...SubcampaignScheduledIncomeMultiplierUpdate
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment AdvertiserScheduledIncomeMultiplierUpdate on AdvertiserScheduledIncomeMultiplierUpdate {
  updateId
  scheduledEffectiveDate
  manualFactor
  comment
  __typename
}

fragment SubcampaignScheduledIncomeMultiplierUpdate on SubcampaignScheduledIncomeMultiplierUpdate {
  updateId
  scheduledEffectiveDate
  manualFactor
  isFixedValue
  comment
  __typename
}

query GetSubcampaignsCreatives($advertiserId: Int!, $subcampaignId: Int!) {
  advertiser(advertiserId: $advertiserId) {
    advertiserId
    subcampaign(subcampaignId: $subcampaignId) {
      subcampaignId
      creatives {
        ...SubcampaignCreative
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SubcampaignCreative on Creative {
  creativeId
  __typename
}

