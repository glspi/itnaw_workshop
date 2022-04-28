node('jenkins-python') {
    stage('build') {
        container('python') {
            checkout scm
            sh 'cat hello.py'
        }
    }
}
