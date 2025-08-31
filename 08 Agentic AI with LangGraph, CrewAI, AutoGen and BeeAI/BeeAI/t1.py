import os

########################
### Set the watsonx.ai project ID 
########################

# The following sets the watsonx.ai project ID for the 
# Skills Network labs environment. Do not modify this setting 
# unless you are running the code outside of the 
# Skills Network labs environment. In that case, you will 
# need to provide your own watsonx.ai project ID.

os.environ["WATSONX_PROJECT_ID"] = "skills-network"

########################
### Set up other watsonx.ai credentials 
########################

# The following watsonx.ai API credentials are already preset 
# for you in the Skills Network labs environment.
# Do not modify these settings unless you are running the code 
# outside of the Skills Network labs environment. In that case, 
# you will need to provide your own credentials.

# os.environ["WATSONX_API_KEY"] = "your-watsonx-api-key"

# If you are running this in your own environmment you would also need either:

# os.environ["WATSONX_URL"] = 

# or:

# os.environ["WATSONX_REGION"] =

########################
### OpenAI specific configuration
########################

# OpenAI API credentials are already preset 
# for you in the Skills Network labs environment.
# Do not modify these settings unless you are running the code 
# outside of the Skills Network labs environment. In that case, 
# you will need to provide your own credentials.

# OPENAI_API_KEY=your-openai-api-key
# OPENAI_API_HEADERS="secret-header=1234"

print("Environment configured successfully!")