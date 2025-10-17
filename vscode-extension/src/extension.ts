import * as vscode from 'vscode';
import axios from 'axios';

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
        this.statusBarItem.show();
    }

    update(text: string) {
        this.statusBarItem.text = `$(sync~spin) ${text}`;
    }

    dispose() {
        this.statusBarItem.dispose();
    }
}

export function activate(context: vscode.ExtensionContext) {
    const statusBar = new CoderToolStatusBar();
    const apiClient = axios.create({
        baseURL: 'http://localhost:8000'
    });

    // Create task command
    let createTask = vscode.commands.registerCommand('codertool.createTask', async () => {
        const taskTypes = ['code', 'review', 'fix', 'architecture'];
        const taskType = await vscode.window.showQuickPick(taskTypes, {
            placeHolder: 'Select task type'
        });

        if (!taskType) {
            return;
        }

        const description = await vscode.window.showInputBox({
            prompt: 'Enter task description'
        });

        if (!description) {
            return;
        }

        try {
            statusBar.update('Creating task...');
            const response = await apiClient.post('/tasks/', {
                type: taskType,
                description,
                context: []
            });

            vscode.window.showInformationMessage(`Task created: ${response.data.id}`);
            statusBar.update('Task created');
        } catch (error) {
            vscode.window.showErrorMessage('Failed to create task');
            statusBar.update('Error');
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