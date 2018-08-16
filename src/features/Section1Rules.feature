#@regressgion
#@smoke
Feature: schedule start and end date validation
  All the generated schedule shall follow the questionnaire section #1 part 1 rule.

  Background:
    Given Schedule is generated and schedule data is trans-formatted to pandas

#  Scenario: Test given fixture injection
#    Given I have injecting given
#    Then foo should be "injected foo"

  Scenario: schedule start and end date should match questionnaire
    Given I am a store manager and i want to check the schedule
    When I select the store id <storeid>
    Then The store schedule date shall begin at <begin_weekday> and end at <end_weekday>

    Examples:
    | storeid| begin_weekday| end_weekday|
    |  862   |  Sun           |  Sat        |

