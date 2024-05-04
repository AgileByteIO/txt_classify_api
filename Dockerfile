# Define custom function directory
ARG FUNCTION_DIR="/function"
ARG OPENAI_API_KEY

FROM python:3.12 as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG OPENAI_API_KEY

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
RUN mkdir -p ${FUNCTION_DIR}/app
COPY app/ ${FUNCTION_DIR}/app/
COPY requirements.txt .

# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
        -r requirements.txt
# Cooy local files into 
#COPY ./entry_script.sh /entry_script.sh
#ADD  aws-lambda-rie /aws-lambda-rie

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.12-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG OPENAI_API_KEY

# SET the ENV for the OPEN AI API KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

COPY ./entry_script.sh /entry_script.sh
RUN chmod +x /entry_script.sh
# Add runtime for local use
COPY ./aws-lambda-rie /usr/local/bin/aws-lambda-rie
# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/entry_script.sh","app.app.handler" ]
