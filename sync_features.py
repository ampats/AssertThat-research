import requests
import os
import zipfile
from github import Github

# AssertThat credentials
at_access_key = '5ab8ba97cb69a63ebf14d6dd52f7b3f5bd68abe73ab362ad1182078d49f34bc5'
at_secret_key = '5ddd058df5b5f265798693de06ff4c36ca9a4857cf5f9dc219f35bd7be0ba14f'
at_project_id = '10000'
at_path = 'https://bdd.assertthat.app/rest/api/1/project/' + at_project_id + '/features'

# GitHub credentials
github_token = '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'
github_repo = 'ampats/AssertThat-research'

# Directory to store feature files
feature_directory = 'feature_files'

# Create a GitHub repository object
g = Github(github_token)
repo = g.get_repo(github_repo)

# Create a directory to store feature files if it doesn't exist
if not os.path.exists(feature_directory):
    os.makedirs(feature_directory)

# Fetch feature files from AssertThat
response = requests.get(at_path,
    auth=(at_access_key, at_secret_key)
) 
# NOTE: The example above is for Jira Data Center. In case you use cloud version the following URL should be used for downloading features: https://bdd.assertthat.app/rest/api/1/project/YOUR_ASSERT_THAT_PROJECT_ID/features

if response.status_code == 200:
    # Save the feature files ZIP to the local directory
    zip_file_path = os.path.join(feature_directory, 'features.zip')
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(feature_directory)

    # Commit and push each extracted .feature file
    for root, _, files in os.walk(feature_directory):
        for file in files:
            if file.endswith(".feature"):
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Specify the file path within the repository
                    file_path_within_repo = os.path.relpath(file_path, feature_directory)
                    print(file_path_within_repo)
                    repo.create_file(
                        path=f"{feature_directory}/{file_path.split('/')[-1]}", #file_path_within_repo,
                        message=f'Update feature file: {file}',
                        content=content,
                        branch='main'
                    )

    # Clean up (delete the local files)
    os.remove(zip_file_path)
    for root, _, files in os.walk(feature_directory):
        for file in files:
            os.remove(os.path.join(root, file))
else:
    print(f'Failed to fetch feature files from AssertThat. Status code: {response.status_code}')
