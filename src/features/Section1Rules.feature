
Feature: schedule start and end date validation
#  All the generated schedule shall follow the questionnaire section #1 part 1 rule.
#  Scenario: schedule start and end date validation
#    Given I am a store manager and i check the schedule
#    When The schedule is generated
#    Then All the store schedule begin and end date shall be 'Sun' and 'Sat'

  Scenario: Test given fixture injection
    Given I have injecting given
    Then foo should be "injected foo"