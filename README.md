# Twitter Twin
ML project to find popular Twitter accounts similar to a given account

## Usage
Visit https://colinmarsch.me/TwiSimilar/ to try out the web app. After authenticating with Twitter the app will take your latest tweets and run them through the classification model developed, predicting one of the top 10 Twitter accounts for each tweet. The Twitter account that shows up the most frequently in the results is then returned as the closest match to your Twitter account.

## Model
The code used to create the model used in the classification can be found in the create_model.py file. A LinearSVC model was used as the classifier.

## Backend
The code for the Flask backend of the app can be found in the app.py file.

## Frontend
The code for the React frontend of the app can be found in the react-fronted folder. This was initally created using the create-react-app npm package.
