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
    }
}
