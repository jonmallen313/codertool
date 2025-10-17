# CoderTool: Claude-Powered Multi-Agent Development System

A VS Code-integrated development system that uses Claude AI agents to automate coding, debugging, and deployment tasks.

## Features

- **VS Code Integration**: Inline AI completions and task management
- **Multiple AI Agents**: Architecture, coding, review, and DevOps automation
- **Automated Bug Fixing**: Detects build failures and generates fixes
- **GitHub Integration**: Automated commits and PR management
- **Railway Integration**: Build log monitoring and error handling

## Setup

1. Install Dependencies:
   ```bash
   # Install Poetry for Python dependency management
   curl -sSL https://install.python-poetry.org | python3 -

   # Install project dependencies
   poetry install
   ```

2. Configure Environment:
   Create a `.env` file with your API keys:
   ```
   CLAUDE_API_KEY=your_claude_api_key
   GITHUB_TOKEN=your_github_token
   RAILWAY_API_KEY=your_railway_api_key
   REPO_OWNER=your_github_username
   REPO_NAME=your_repo_name
   ```

3. Install VS Code Extension:
   ```bash
   cd vscode-extension
   npm install
   npm run compile
   ```

4. Start the Backend:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

## Usage

1. **Create Tasks**
   - Use the Command Palette (`Ctrl+Shift+P`) and search for "CoderTool: Create Task"
   - Select task type and enter description
   - Agents will automatically process the task

2. **Monitor Status**
   - Click the CoderTool status bar item
   - View current tasks and their status

3. **Automated Bug Fixing**
   - Push changes to GitHub
   - Railway will trigger a build
   - On failure, agents will analyze logs and suggest fixes
   - Approved fixes are automatically committed

## Architecture

### Components

1. **Orchestrator** (FastAPI)
   - Task management and queuing
   - Agent coordination
   - API endpoints for VS Code extension

2. **Agents**
   - **Architect**: Task breakdown and planning
   - **Coder**: Code generation and modification
   - **Reviewer**: Code review and analysis
   - **DevOps**: Build and deployment monitoring

3. **Integrations**
   - GitHub API for source control
   - Railway API for deployment monitoring
   - Claude API for AI reasoning

4. **VS Code Extension**
   - Task creation and management
   - Status monitoring
   - Build/deploy notifications

### Flow

1. User creates task via VS Code
2. Architect agent breaks down complex tasks
3. Coder agent implements changes
4. Changes are pushed to GitHub
5. Railway builds the changes
6. DevOps agent monitors build status
7. On failure, Reviewer agent analyzes logs
8. Coder agent implements fixes
9. Process repeats until build succeeds

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT