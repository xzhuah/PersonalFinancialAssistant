# PersonalFinancialAssistant

<a href="http://www.andrew.cmu.edu/user/xinyuzhu/pfa.html">Visit the website here</a>


## Description

This would be a web application aims at helping people recording their daily transactions so that they can review, analyze and plan their financial activity more easily. 

## Security

This is a secure program. It allows you to 

* use your own <a href="https://www.mongodb.com/cloud/atlas">mongodb database</a> with login information maintained by yourself
* encrypt all your database message with your own password
	* each if someone managed to get into your database, he won't read your data


This is a secure program based on

* <a href="https://www.djangoproject.com/">Django Python web framework</a>
	* We use the same framework as The National Aeronautics and Space Administration (NASA)
* Encryption module from <a href="https://github.com/xzhuah/SecPyRender">SecPyRender</a>
	* Build upon Advanced Encryption Standard (AES) with 256 bit hash and random generated initialization vector
	* ![](https://i.imgur.com/hHbOPZM.png)


## Usability

A pragmatic user infterface will guide you to manage your daily transaction

<a href="http://pyecharts.org/#/">pyecharts visualization libaray</a> will help you review your historical activity in a most intuitive way

## Visulization
[![](https://i.imgur.com/VjmvO58.png)](http://ec2-34-219-176-112.us-west-2.compute.amazonaws.com:8000/review/dynamic/)

[![](https://i.imgur.com/aMWWGKs.png)](http://ec2-34-219-176-112.us-west-2.compute.amazonaws.com:8000/review/week3D/)
## Scalability

More function will be added later