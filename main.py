# GitHub Actions Workflow

name: Create Issue on Causas

on:
  schedule:
    - cron: '0 * * * *' # runs every hour

jobs:
  create_issue:
    runs-on: ubuntu-latest
    steps:
      - name: Check for Causas
        id: check_causas
        run: |
          # Here you'd include logic to check for causas
          # For example, you might call an API that returns the status
          # If causas are found, exit with a specific status code

          if [some condition identifying causas]; then
            echo "Found causas - creating issue"
            echo "::set-output name=found::true"
          else
            echo "No causas found"
            echo "::set-output name=found::false"
          fi

      - name: Create Issue
        if: steps.check_causas.outputs.found == 'true'
        uses: octokit/request-action@v2.0.0
        with:
          route: POST /repos/{owner}/{repo}/issues
          title: Issue alert: Causas detected
          body: 'Causas have been detected by the GitHub Action.'

