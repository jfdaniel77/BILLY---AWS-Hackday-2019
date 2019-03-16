# BILLY (Bin It Happily) - AWS Hackday 2019
This is repository for Billy. Billy is a prototype that we build for our participation in AWS Hackday 2019.

Billy is an mobile or IoT application that is used in waste management. This application can do object classification so that user is able to know which correct recycle bin to throw it.  In this prototype, we do classification for 6 different type of objects. Those are metal, paper, cardboard, plastic, glass and trash. 

We build this application on AWS infrastructure and the main service we use are AWS Rekognition and AWS SageMaker. In this case, AWS Rekognition does object detections and returns possible labels (and its confident levels). Those labels are inputted into AWS SageMaker to predict type of object.

For training purpose in AWS SageMaker, we are use trash images dataset from https://github.com/garythung/trashnet

Folder description:<br>
a. backend<br>
It contains our code for managing and orchestrating request(s) from mobile application/IoT devices.<br>
<br>

b. dataset<br>
It contains trash images dataset for training and testing purposes.<br>
<br>

c. documents<br>
It contains our documentations including our executive summary and demo video.<br>
<br>

d. frontend<br>
It contains our code for our prototype of mobile application.<br>
<br>

e. lambda<br>
It contains our code in AWS Lambda to orchestrator process to Amazon Rekognition and Amazon SageMaker.<br>
<br>

f. training<br>
It contains our code in Jupiter Notebook to build and train our model in Amazon SageMaker<br>
