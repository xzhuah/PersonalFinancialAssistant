# PersonalFinancialAssistant


## Description

This would be a web application aims at helping people recording their daily transactions so that they can review, analyze and plan their financial activity more easily. 

## Security

This is a secure program. It allows you to 

* use your own mongodb database with login information maintained by yourself
* encrypt all your database message with your own password
	* each if someone managed to get into your database, he won't read your data


This is a secure program based on

* <a href="https://www.djangoproject.com/">Django Python web framework</a>
	* We use the same framework as The National Aeronautics and Space Administration (NASA)
* Encryption module from SecPyRender
	* Build upon Advanced Encryption Standard (AES) with 256 bit hash and random generated initialization vector


## Usability

A pragmatic user infterface will guide you to manage your daily transaction

<a href="http://pyecharts.org/#/">pyecharts visualization libaray</a> will help you review your historical activity in a most intuitive way

## Scalability

More function will be added later