pipeline {
    agent any
    environment {
        DOCKER_REPO = 'vinithdkumar/k8s-voting-app'
    }
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
                        -t voting-frontend:${BUILD_NUMBER} \
                        ./frontend-voting
                '''

                echo 'Building backend Docker image'

                sh '''
                    docker build \
                        -t voting-backend:${BUILD_NUMBER} \
                        ./backend-voting
                '''

                echo 'Building worker Docker image'

                sh '''
                    docker build \
                        -t voting-worker:${BUILD_NUMBER} \
                        ./worker-voting
                '''

                echo 'All Docker images built successfully.'
            }
        }
       stage('Docker Push') {
          steps {
            withCredentials([
              usernamePassword(
                credentialsId: 'dockerhub',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASSWORD'
            )
        ]) {
            sh '''
                echo "$DOCKER_PASSWORD" | docker login \
                    -u "$DOCKER_USER" \
                    --password-stdin

                docker push ${DOCKER_REPO}:frontend-${BUILD_NUMBER}
                docker push ${DOCKER_REPO}:backend-${BUILD_NUMBER}
                docker push ${DOCKER_REPO}:worker-${BUILD_NUMBER}
            '''
        }
    }
}
    }
}
