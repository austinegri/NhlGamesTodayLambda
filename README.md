# About 
Lambda function that will check NHL schedule api for games today and create an eventbridge schedule for 5 min before each game.

# Testing
## Local
1. Run `docker build --platform linux/amd64 -t docker-image:test .` to build
2. Run `docker run --platform linux/amd64 -p 9000:8080 docker-image:test` to run
3. In a separate window, run `curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'` to invoke

## Aws
1. Run above commands to build
2. Run `docker tag docker-image:test 111122223333.dkr.ecr.us-east-1.amazonaws.com/nhl-games-today:latest`
2. Run `docker push 111122223333.dkr.ecr.us-east-1.amazonaws.com/nhl-games-today:latest` (replace accountId)
3. Update the function code `aws lambda update-function-code --function-name nhl-games-today --image-uri 111122223333.dkr.ecr.us-east-1.amazonaws.com/nhl-games-today:latest`
   3. [If creating for the first time] Create the function from ECR image: ```aws lambda create-function \
     --function-name nhl-games-today \
     --package-type Image \
     --code ImageUri=111122223333.dkr.ecr.us-east-1.amazonaws.com/nhl-games-today:latest \```

https://docs.aws.amazon.com/lambda/latest/dg/python-image.html