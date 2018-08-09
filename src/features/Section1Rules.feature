
Feature: schedule start and end date validation
  All the generated schedule shall follow the questionnaire section #1 part 1 rule.

  Background:
    Given Schedule is generated and schedule data is trans-formatted to pandas

#  Scenario: Test given fixture injection
#    Given I have injecting given
#    Then foo should be "injected foo"

  Scenario: schedule start and end date should match questionnaire
    Given All the
    When The schedule is generated
    Then All the store schedule begin and end date shall be 'Sun' and 'Sat'

