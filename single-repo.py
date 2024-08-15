from github import Github, RateLimitExceededException
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from the environment
token = os.getenv('GITHUB_TOKEN')

# Create a GitHub instance using the token
g = Github(token, timeout=10)  # Set a timeout for the GitHub API requests

def search_files(query):
    try:
        print(f"Searching with query: {query}")
        result = g.search_code(query)
        print("Search completed.")
        return result
    except RateLimitExceededException:
        print("Rate limit exceeded, waiting for reset...")
        core_rate_limit = g.get_rate_limit().core
        reset_timestamp = core_rate_limit.reset.timestamp()
        current_timestamp = time.time()
        wait_time = reset_timestamp - current_timestamp
        print(f"Waiting for {wait_time + 1} seconds for rate limit reset...")
        time.sleep(wait_time + 1)
        return search_files(query)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Specify the repository name (owner/repo)
repo_name = 'owner/repository'

# Search for the Directory.Packages.props file in the specified repository
query = f'filename:README.md repo:{repo_name}'

# Perform the search
result = search_files(query)

# Print the total number of matches and their paths
if result:
    print(f'Total files found: {result.totalCount}')
    for file in result:
        print(f"File path: {file.path}")
        print(f"Repository: {file.repository.full_name}")
        print(f"URL: {file.html_url}")
        print("-" * 40)
else:
    print("No results found or an error occurred.")

# Check the rate limit
rate_limit = g.get_rate_limit()
print(f"Core rate limit remaining: {rate_limit.core.remaining}")
