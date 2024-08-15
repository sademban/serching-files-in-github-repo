from github import Github, RateLimitExceededException
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from the environment
token = os.getenv('GITHUB_TOKEN')

# Create a GitHub instance using the token
g = Github(token)

def search_files(query):
    try:
        result = g.search_code(query)
        return result
    except RateLimitExceededException:
        print("Rate limit exceeded, waiting for reset...")
        core_rate_limit = g.get_rate_limit().core
        reset_timestamp = core_rate_limit.reset.timestamp()
        current_timestamp = time.time()
        wait_time = reset_timestamp - current_timestamp
        time.sleep(wait_time + 1)  
        return search_files(query) 

# Query for the search
query = 'filename:Directory.Packages.props'
result = search_files(query)

# Print the total number of matches and their paths
print(f'Total files found: {result.totalCount}')
for file in result:
    print(f"File path: {file.path}")
    print(f"Repository: {file.repository.full_name}")
    print(f"URL: {file.html_url}")
    print("-" * 40)
