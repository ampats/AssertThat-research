# language: en
@smoke    @wip    
Feature: Easily manage and maintain my scenarios in AssertThat

    As a business user or tester. I want to easily update feature details and add new scenarios to describe how I want my functionality to behave.

    Background: AssertThat plugin is enabled
        Given I have installed the plugin
        And I access my development project in Cloud Jira

    @AUTOMATED @add-scenarios 
    Scenario: I can add and manage tags and background steps to my Feature
        Given an existing feature with multiple scenarios
        When I access an existing feature

    @MANUAL @KAN-1 
    Scenario: Add new scenario from user story
        Given the AssertThat plugin is installed
        When I add new scenarios from the user story

