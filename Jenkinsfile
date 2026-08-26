pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning the git repo'
                git branch: 'main', credentialsId: 'github-ssh', url: 'git@github.com:scarface-0210/k8s-voting-app.git'
                echo 'Git repo has been cloned successfully.'
            }
        }
        stage('Test') {
            steps {
                echo 'Running Python syntax checks'

                sh 'python3 -m py_compile backend-voting/app.py'
                sh 'python3 -m py_compile worker-voting/worker.py'

                echo 'Python syntax checks passed.'
            }
       }
       stage('Code Quality') {
           steps {
               echo 'Running Python code quality checks'

               sh '''
               python3 -m venv .venv
               . .venv/bin/activate

               pip install --upgrade pip
               pip install ruff

               ruff check backend-voting worker-voting
               '''

              echo 'Code quality checks passed.'
    }
}
stage('Docker Build') {
            steps {
                echo 'Building frontend Docker image'

                sh '''
                    docker build \
                        -t voting-frontend:latest \
                        ./frontend-voting
                '''

                echo 'Building backend Docker image'

                sh '''
                    docker build \
                        -t voting-backend:latest \
                        ./backend-voting
                '''

                echo 'Building worker Docker image'

                sh '''
                    docker build \
                        -t voting-worker:latest \
                        ./worker-voting
                '''

                echo 'All Docker images built successfully.'
            }
        }
    }
}
