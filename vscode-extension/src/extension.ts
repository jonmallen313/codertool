import * as vscode from 'vscode';
import axios, { AxiosError } from 'axios';

interface Task {
    id: string;
    type: string;
    description: string;
    status: string;
}

export class CoderToolStatusBar {
    private statusBarItem: vscode.StatusBarItem;

    constructor() {
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        this.statusBarItem.command = 'codertool.viewStatus';
        this.statusBarItem.text = "$(tools) CoderTool";
        this.statusBarItem.show();
    }

    update(text: string, error: boolean = false) {
        this.statusBarItem.text = error 
            ? `$(error) CoderTool: ${text}`
            : `$(sync~spin) CoderTool: ${text}`;
    }

    dispose() {
        this.statusBarItem.dispose();
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('CoderTool extension is now active');
    
    const statusBar = new CoderToolStatusBar();
    const apiClient = axios.create({
        baseURL: 'http://127.0.0.1:8000',
        timeout: 5000
    });

    // Create task command
    let createTask = vscode.commands.registerCommand('codertool.createTask', async () => {
        try {
            const taskTypes = ['code', 'review', 'fix', 'architecture'];
            const taskType = await vscode.window.showQuickPick(taskTypes, {
                placeHolder: 'Select task type'
            });

            if (!taskType) {
                return;
            }

            const description = await vscode.window.showInputBox({
                prompt: 'Enter task description',
                placeHolder: 'Describe what you want the AI to do'
            });

            if (!description) {
                return;
            }

            statusBar.update('Creating task...');
            
            // Generate a unique ID
            const taskId = `task_${Date.now()}`;
            
            const response = await apiClient.post('/tasks/', {
                id: taskId,
                type: taskType,
                description,
                context: []
            });

            vscode.window.showInformationMessage(`Task created: ${response.data.id}`);
            statusBar.update('Task created');
        } catch (error) {
            console.error('Error creating task:', error);
            
            if (error instanceof AxiosError) {
                if (error.code === 'ECONNREFUSED') {
                    vscode.window.showErrorMessage(
                        'Could not connect to CoderTool server. Please make sure the server is running on http://127.0.0.1:8000'
                    );
                } else {
                    vscode.window.showErrorMessage(
                        `Server error: ${error.response?.data?.detail || error.message}`
                    );
                }
            } else {
                vscode.window.showErrorMessage(`Failed to create task: ${error}`);
            }
            
            statusBar.update('Error', true);
        }
    });

    // View status command
    let viewStatus = vscode.commands.registerCommand('codertool.viewStatus', async () => {
        try {
            statusBar.update('Fetching status...');
            const response = await apiClient.get('/tasks/');
            const tasks: Task[] = response.data;

            const statusMessage = tasks
                .map(task => `${task.type}: ${task.status}`)
                .join('\n');

            vscode.window.showInformationMessage(statusMessage);
            statusBar.update('Ready');
        } catch (error) {
            vscode.window.showErrorMessage('Failed to fetch status');
            statusBar.update('Error');
        }
    });

    context.subscriptions.push(createTask, viewStatus, statusBar);
}