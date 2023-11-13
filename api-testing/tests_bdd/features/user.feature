Feature: User Service Endpoint

    Scenario: It's possiblem to create an user with success
        Given I have a user to create
        When I call the endoint to create the user
        Then user should be created with success
        And the response schema should be the corresponding to the user creation

    Scenario: It's not possible to create an user that was already created
        Given I already created an user
        When I call the endoint to create the user
        Then user should not be created because aleady exist
        And the response schema should be the corresponding to the error

    Scenario Outline: It's not possible to create an user with name or surname with fewer characters limits
        Given I have an user with empty "<scenario>"
        When I call the endoint to create the user
        Then user should not be created because has fewer characters than limit
        And the response schema should be the corresponding to the error
        Examples:
            | scenario |
            | Name     |
            | Surname  |

    Scenario Outline: It's possible to create an user with minimum character constraint
        Given I have an user with minimum character for "<field>"
        When I call the endoint to create the user
        Then user should be created with success
        And the response schema should be the corresponding to the user creation
        Examples:
            | field   |
            | name    |
            | surname |

    Scenario Outline: It's not possible to create an user missing required field <excluded_field>
        Given I have an user with excluded field "<excluded_field>"
        When I call the endoint to create the user
        Then I should receive a validation error message "<expected_error_message>"

        Examples:
            | excluded_field | expected_error_message                |
            | email          | must have required property 'email'   |
            | name           | must have required property 'name'    |
            | surname        | must have required property 'surname' |
