Ostree configuration

Deploy the OSTtree branch to a disk.

ostree:
  repository: repository name
  remote_repository: URL
  branch: branch name

Mandatory properties:

- repository -- path to repositoryt OSTRee structure.

- remote_repository: URL to remote OSTRree repository for pulling stateroot
  branch.

- branch -- branch of the repository to use for populating the disk. If using
  a remote repository the branch must be prefixed with the name of the remote.

  Ex: "pablo.org:pablo/1.0"
