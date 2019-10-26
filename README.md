# gitlab-ci-env
Pulls GitLab CI/CD project and group variables

# Usage
```
git clone https://gitlab.corp.local/user/project
cd project
export GITLAB_TOKEN=1HgHveepxeniqpez-zxm # Personal Access Token
export $(gitlab-ci-env)
make
```
