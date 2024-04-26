Feature: checking products

Scenario: add a product
    Given we want to add a product
    When we fill in the form
    Then it succeeds

Scenario: adding products
    Given we have specific products to add
    | name          | price  |
    | new computer  | 2000   | 
    | nice computer | 3333  |
    When we visit the listing page
    Then we will find 'nice computer'