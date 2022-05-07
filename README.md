# Sign language tutor API

Python web-app made in Flask. This API communicates to an Expo app.

The job of the API is to recieve static images of ASL letters and using a model built in tensorflow, classify them.

GET /getScores
returns({name: string, score: number})

Hosted on Azure
