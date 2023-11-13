# API TESTING USING PYTHON AND K6 FOR PERFORMANCE TESTING

To understand how to execute each of the API Tests or Performance Test projects, follow the links below:

# API TESTS

You can find more detailed information in the [API-TESTING-README](/api-testing/README.md).

# PERFPORMANCE TEST

For detailed information, refer to the [PERFORMANCE-TESTING-README](/performance-testing/README.md).

<br>

# About Test Projects

These were some of the validated scenarios. Due to the simplicity of the APIs, I didn't find it necessary to test other scenarios because the main idea it was setuping a basic project to use in some project that helps some QA at the beginning of their automations.

In the example project, we have two APIs.

## User

- User creation (validation for first-time or existing users)
- Validation of mandatory fields for user creation
- Validation of field limits during user creation
- Retrieval of all users, including specific users (whether they exist or not)

## Booking

- Booking creation for a user
- Validation when the user does not exist
- Validation of date format during booking creation
- Validation of user identification in the wrong format
- Validation of destination and origin field limits, as well as their types
- Validation of mandatory fields
- Search for specific bookings or non-existent bookings
- Retrieval of all bookings for all users
- Retrieval of bookings for a user with no bookings
- Retrieval of bookings for a user on a specific date
- Retrieval of all bookings for a specific date

## Testing Strategy

Regarding the implemented tests, I understand that best testing practices lead us to implement some tests, not at the API level, but at the unit level. For example, it doesn't make much sense to wait until the API test to validate character limits for each field. For a **good testing strategy**, we can apply the **Test Pyramid** to distribute each test to the most appropriate layer of the application, ensuring safety throughout the product and testing speed.

A **Schema Validation** was added to the API tests to check whether the response contract is being respected, related to the fields and their types.

**Performance tests** serve as a basis for the concern we should have to ensure the application continues to function even when many users are accessing it or when unexpected or expected spikes occur (such as during certain times of the year when users make more reservations).

The tests can be conducted for the team to discover the limits of their application. In this case, **thresholds** are not necessary; the **performance test planning** is meant to find these limits. However, if the team already knows the limits, it's a good idea to add **thresholds** so that when the tests are executed, we can determine when they no longer correspond to the defined limits.

For the Performance Testing was indicated two ways to see the results, locally or in the cloud (Using **k6 Grafana Cloud**)

## Use of Gherkin

In the API Test Project, I added two examples that can be followed for test implementation. One example is without Gherkin (**Pytest**), and the other is with Gherkin(**Behave**). This way, you can see the differences between the two patterns when used.

I know that in some places it becomes necessary to use Gherkin in the API, I disagree for some reasons that make it more complicated, but I left an example in case you need it, because I know that the real world is different from what we want.

## CI

It was implemented also a GithubAction to run the API Tests in each push or pull request to the main branch.
The job is also triggered by a cron job (Commented) to run from Monday to Friday at 12 noon.
To give more autonomy, there is also an Action to manually run the api testing job.
