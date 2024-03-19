# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    branch_management.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 16:01:45 by Winshare To       #+#    #+#              #
#    Updated: 2023/09/29 16:01:46 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import git
import os
import uuid
import time

class KnowledgeGraphManager:
    def __init__(self, repo_path, username):
        self.repo_path = repo_path
        self.username = username
        self.repo = self._open_or_init_repo()

    def _open_or_init_repo(self):
        if not os.path.exists(self.repo_path):
            # 初始化一个新仓库
            repo = git.Repo.init(self.repo_path)
            repo.git.config("user.name", self.username)
            repo.git.config("user.email", f"{self.username}@example.com")
            return repo
        else:
            # 打开现有仓库
            return git.Repo(self.repo_path)

    def create_branch(self, version_id):
        timestamp = int(time.time())
        branch_name = f"{uuid.uuid4()}-{self.username}-{version_id}-{timestamp}"

        # 创建一个新分支
        new_branch = self.repo.create_head(branch_name)
        new_branch.checkout()

    def commit_changes(self, message):
        # 添加所有更改到暂存区
        self.repo.index.add('*')

        # 提交更改
        self.repo.index.commit(message)

    def switch_to_branch(self, branch_name):
        # 切换到指定分支
        if branch_name in self.repo.heads:
            branch = self.repo.heads[branch_name]
            branch.checkout()
        else:
            raise ValueError(f"Branch {branch_name} does not exist.")

    def list_branches(self):
        # 列出所有分支
        return [branch.name for branch in self.repo.branches]

    def pull_changes(self):
        # 拉取最新的更改
        origin = self.repo.remotes.origin
        origin.pull()

    def push_changes(self):
        # 推送更改到远程仓库
        origin = self.repo.remotes.origin
        origin.push()

# 示例用法
if __name__ == "__main__":
    repo_path = "/matrixcard/PythonPackageDev/workspace"
    username = "your_username"
    manager = KnowledgeGraphManager(repo_path, username)

    manager.create_branch("v1")
    manager.commit_changes("Initial version")

    manager.create_branch("v2")
    manager.commit_changes("Add new features")

    print("Branches:", manager.list_branches())
