# smartticket

This project aims at classify the lines of a receipt.
It works with AWS environment : s3, api gateway, lambda

## Code part
All the code has been made in Python 2.7

### classification
Two goals :
- load Open Facts data
- Create models (in pickle) for classification

### db_access
Access to Mysql database and to dynamodb.
The link to Mysql has been made to link this project to Bons plans

### lambdas
Methods with are the access points of lambda AWS

### raw_treatment
Methods for dealing with raw input (non GSA)

### Tests class
Contains:
- Unit tests
- Running tests

## Target
Files to be upload in the s3. This loadinf treatment is made automaticly with serverless

## data
Contains :
- the Open Food Facts csv
- the class names csv
- payload example

## models
Contains the pickles created in classification

## serverless file
Need for automatic loading
command line : serverless deploy --stage prod --region eu-west-1
The serverless method force us to modify the code, it doesn't run anymore in local environment


