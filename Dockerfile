# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ./requirements.txt

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY scheduleHandler.py ./scheduleHandler.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "scheduleHandler.lambda_handler" ]