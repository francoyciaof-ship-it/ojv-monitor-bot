# SETUP Instructions for OJV Monitor Bot

## Configuration Instructions

### Adding RIT/ROL Numbers
1. Access the configuration file located at `config/rit_rol.json`.
2. Open the file in a text editor.
3. Add the following format:
   ```json
   {
     "RIT": "your_rit_number",
     "ROL": "your_rol_number"
   }
   ```
4. Save the changes.

### Configuring GitHub Tokens
1. Navigate to the GitHub settings for the repository.
2. Select **Developer settings** > **Personal access tokens**.
3. Click on **Generate new token**.
4. Choose the scopes or permissions you'd like to grant this token.
5. Copy the generated token and add it to your environment variables under `GITHUB_TOKEN`.

### Understanding Data Structure
- The main data structure used by the OJV Monitor Bot consists of:
  - **Alerts**: JSON objects that trigger notifications.
  - **Configurations**: Settings that define how the bot behaves.
- See `data/structure.md` for detailed documentation on fields.

### Running Manual Tests
1. Ensure you have the necessary testing framework set up (e.g., Jest, Mocha).
2. Use the command below to run tests manually:
   ```bash
   npm run test
   ```
3. Review the output for any reported errors.

### Troubleshooting Issues
- If you encounter issues:
  - Check the logs in `logs/error.log` for detailed error messages.
  - Ensure your configurations are correctly set according to the guidelines above.
  - If problems persist, reach out to the support team with the log file and description of the issue.

## Examples
To illustrate how to add RIT/ROL numbers, here’s an example JSON configuration:
```json
{
  "RIT": "123456",
  "ROL": "654321"
}
```

For troubleshooting, say you see an error in the logs about missing a token; ensure your GitHub token is configured correctly as shown above. 

Following these instructions will help you successfully configure the OJV Monitor Bot and utilize its full potential.

Happy Monitoring!